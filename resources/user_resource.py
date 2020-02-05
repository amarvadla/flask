import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="should be passed")
    parser.add_argument('password', type=str, required=True,
                        help="should be passed")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "username already taken"}, 400

        user = User(**data)
        user.save_to_db()

        return {"message": "user created"}, 201
