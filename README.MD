# PervertGram

A weekend project from a cyber-pervert.

## Get followers/Followings/Matches
![](images/0.png)

```
http://localhost:5002/followings/<victim> or
http://localhost:5002/followings/api/<victim>/
```
```
http://localhost:5002/followers/<victim> or
http://localhost:5002/api/followers/<victim>/
```
```
http://localhost:5002/match/<victim> or
http://localhost:5002/api/match/<victim>/
```

## Get HD Profile Picture

![](images/1.png)
```
http://localhost:5002/dp/<victim>
http://localhost:5002/api/dp/<victim>
```

## Draw heatmap from users location 

![](images/2.gif)

```
http://localhost:5002/dp/heatmap/<victim>
```

## Others

### Get photos from the given location

```
http://localhost:5002/location/<int:location>
http://localhost:5002/api/location/<int:location>
```

### Get people from the given location
```
http://localhost:5002/location-people/<int:location>
http://localhost:5002/api/location-people/<int:location>
```
## Routes

### API

```
'/api/followings/<victim>/'
'/api/followers/<victim>/'
'/api/match/<victim>/'
'/api/location/<victim>/'
'/api/dp/<victim>/'
'/api/user-locations/<victim>/'
'/api/location-people/<int:location>'
```

### View

```
'/followings/<victim>'
'/followers/<victim>'
'/match/<victim>'
'/location-people/<int:location>'
'/heatmap/<victim>'
'/location/<int:location>'
'/dp/<victim>'
'/location-people/<int:location>'
```
### config.json

```json
{
    "username": "exampleUser",
    "pwd": "examplePassword"
}

```