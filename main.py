from flask import Flask
from flask.views import MethodView

app = Flask('app')

class SellerView(MethodView):
    def get(self, post_id):
        pass

    def post(self, post_id):
        pass

    def patch(self, post_id):
        pass

    def delete(self, post_id):
        pass


if __name__ == '__main__':
    app.run()