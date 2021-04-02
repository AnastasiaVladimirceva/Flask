from flask import jsonify
from flask_restful import reqparse, Resource, abort
from data.users import *
from data import db_session


def set_password(password):
    return generate_password_hash(password)


def abort_if_user_not_found(id):
    session = db_session.create_session()
    user = session.query(User).get(id)
    if not user:
        abort(404, message=f"News {id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'about', 'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('hashed_password', required=True, type=int)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('name', 'about', 'email', 'hashed_password')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            about=args['about'],
            email=args['email'],
            is_published=args['is_published'],
            hashed_password=set_password(['hashed_password'])
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
