from instagram_private_api import Client, ClientCompatPatch
from instagram_private_api.utils import InstagramID

import inspect
from functools import lru_cache, wraps
from typing import Dict, List, Any, Union, Callable, Tuple, Optional


def canonicalize_args(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        sig = inspect.getfullargspec(f.__wrapped__)
        newargs = [None] * len(sig.args)
        newargs[-len(sig.defaults) :] = sig.defaults
        newargs[: len(args)] = args
        for name, value in kwargs.items():
            newargs[sig.args.index(name)] = value

        return f(*newargs)

    return wrapper


class Pervertgram:
    def __init__(self, username: str, password: str):
        self.client = Client(username, password)
        self.rank_token = Client.generate_uuid()

    @lru_cache
    def __user(self, username: str) -> Dict[str, Any]:
        return self.client.username_info(username).get("user")

    @lru_cache
    def userid(self, username: str) -> int:
        return self.__user(username).get("pk")

    def __collect_pages(
        self,
        param_id: int,
        callback: Callable[..., Dict[str, Any]],
        key: str = "users",
        **kwargs,
    ):
        first_page = callback(param_id, **kwargs)
        items = first_page.get(key)
        next_max_id = first_page.get("next_max_id")

        while next_max_id and (
            _items := callback(param_id, **kwargs, max_id=next_max_id)
        ):
            next_max_id = _items.get("next_max_id")
            items.extend(_items.get(key))
        return items

    def hd_pfp(self, username: str) -> str:
        user = self.__user(username)
        return user.get("hd_profile_pic_url_info").get("url")

    @lru_cache
    def __all_followers(self, user_id: int):
        return self.__collect_pages(
            user_id, self.client.user_followers, rank_token=self.rank_token
        )

    def all_followers(self, user: Union[int, str]):
        if isinstance(user_id := user, str):
            user_id = self.userid(user)
        return self.__all_followers(user_id)

    @lru_cache
    def __all_followings(self, user_id: int) -> List[Dict[str, Any]]:
        return self.__collect_pages(
            user_id, self.client.user_following, rank_token=self.rank_token
        )

    def all_followings(self, user: Union[int, str]):
        if isinstance(user_id := user, str):
            user_id = self.userid(user)
        return self.__all_followings(user_id)

    @lru_cache
    def __all_images(self, user_id: int) -> List[Dict[str, Any]]:
        return self.__collect_pages(user_id, self.client.user_feed, key="items")

    def all_images(self, user: Union[int, str]):
        if isinstance(user_id := user, str):
            user_id = self.userid(user)
        return self.__all_images(user_id)

    @lru_cache
    def __followed_back(self, user_id: int) -> List[Dict[str, Any]]:
        followers = set(map(lambda user: user.get("pk"), self.__all_followers(user_id)))
        followings = self.__all_followings(user_id)
        fb_ids = followers.intersection(map(lambda user: user.get("pk"), followings))

        return [user for user in followings if user.get("pk") in fb_ids]

    def followed_back(self, user: Union[int, str]) -> List[Dict[str, Any]]:
        if isinstance(user_id := user, str):
            user_id = self.userid(user)
        return self.__followed_back(user_id)

    def pagen(self, callback, param_id, next_max_id=None, **kwargs):
        if next_max_id:
            return callback(param_id, max_id=next_max_id, **kwargs)
        return callback(param_id, **kwargs)

    def pagen_getter(self, callback, param, next_max_id, key, **kwargs):
        if isinstance((param_id := param), str):
            param_id = self.userid(param)
        data = self.pagen(callback, param_id, next_max_id=next_max_id, **kwargs)
        return data.get(key), data.get("next_max_id")

    @lru_cache
    def images(
        self, username: str, next_max_id: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        return self.pagen_getter(self.client.user_feed, username, next_max_id, "items")

    @canonicalize_args
    @lru_cache
    def followings(
        self, username: str, next_max_id: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        return self.pagen_getter(
            self.client.user_following,
            username,
            next_max_id,
            "users",
            rank_token=self.rank_token,
        )

    @canonicalize_args
    @lru_cache
    def followers(
        self, username: str, next_max_id: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        return self.pagen_getter(
            self.client.user_followers,
            username,
            next_max_id,
            "users",
            rank_token=self.rank_token,
        )

    @canonicalize_args
    @lru_cache
    def location_images(self, location_id: int, next_max_id: Optional[str] = None):
        return self.pagen_getter(
            self.client.feed_location, location_id, next_max_id, "items"
        )

    @lru_cache
    def location_ppl(self, location_id: int):
        return [
            *filter(
                None,
                (
                    item.get("user")
                    for item in self.__collect_pages(
                        location_id, self.client.feed_location, key="items"
                    )
                ),
            )
        ]

    def image_location(self, item: Dict[str, Any]):
        if item.get("location"):
            data = dict()
            if item.get("image_versions2"):
                data["source"] = item["image_versions2"]["candidates"][0]["url"]
            else:
                data["source"] = item["carousel_media"][0]["image_versions2"][
                    "candidates"
                ][0]["url"]
            data["link"] = item["code"]
            data["location"] = (
                item["location"]["short_name"]
                if item["location"].get("short_name")
                else item["location"]["name"]
            )
            data["latitude"] = item["location"]["lat"]
            data["longitude"] = item["location"]["lng"]
            return data

    @lru_cache
    def __profile_locations(self, userid: int):
        return [
            *filter(
                None, (self.image_location(item) for item in self.__all_images(userid)),
            )
        ]

    def profile_locations(
        self, user: Union[int, str]
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        if isinstance(user_id := user, str):
            user_id = self.userid(user)
        return self.__profile_locations(user_id)

    @lru_cache
    def liker(self, picture_code: str) -> Dict[str, Any]:
        media_id = InstagramID.expand_code(picture_code)
        return self.client.media_likers(media_id).get("users")

    def bulk_userid2user(self, ids: List[int]) -> List[Dict[str, Any]]:
        return [self.client.user_info(_id).get("user") for _id in ids]
