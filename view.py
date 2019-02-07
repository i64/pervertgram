from flask import render_template
class render:
    @staticmethod
    def image(data):
        return render_template('imageship.html')
    @staticmethod
    def folow(data):
        return render_template('followship.html')
    @staticmethod
    def heatmap(data):
        return render_template('heatmap.html')
