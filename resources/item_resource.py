import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price should be passed"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="store_id should be passed"
                        )

    @jwt_required()
    def get(self, name):
        row = ItemModel.find_by_name(name)
        if row:
            return {'item': row.json()}
        else:
            return {"message": "item not found"}, 404

    def post(self, name):
        row = ItemModel.find_by_name(name)

        if row:
            return {'message': "item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        # data = request.get_json()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            # internal server error
            return {"message": "An error occured"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": " item has been deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemsList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
