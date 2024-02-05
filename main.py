from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Product, Session
from schema import CreateProduct, UpdateProduct

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


def validate_json(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


def get_product_by_id(product_id: int):
    product = request.session.get(Product, product_id)
    if product is None:
        raise HttpError(404, "product not found")
    return product


def add_product(product: Product):
    try:
        request.session.add(product)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "product already exists")


class SellerView(MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, post_id):
        product = get_product_by_id(post_id)
        return jsonify(product.dict)

    def post(self):
        json_data = validate_json(CreateProduct, request.json)
        product = Product(**json_data)
        add_product(product)
        return jsonify({"id": product.id})

    def patch(self, post_id):
        json_data = validate_json(UpdateProduct, request.json)
        product = get_product_by_id(post_id)
        for field, value in json_data.items():
            setattr(product, field, value)
        add_product(product)
        return jsonify(product.dict)

    def delete(self, post_id):
        product = get_product_by_id(post_id)
        self.session.delete(product)
        self.session.commit()
        return jsonify({"status": "deleted"})


product_view = SellerView.as_view("product_view")


app.add_url_rule("/products/", view_func=product_view, methods=["POST"])
app.add_url_rule(
    "/products/<int:post_id>/",
    view_func=product_view,
    methods=["PATCH", "GET", "DELETE"],
)


if __name__ == "__main__":
    app.run()
