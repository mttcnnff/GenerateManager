from flask_restful import Resource, abort
from . import api
from ..models import MemberModel
from .. import db

@api.route('/members/<int:id>')
class Member(Resource):
    def member_does_not_exist(self, todo_id):
        abort(404, message="Member {} does not exist".format(todo_id))

    def get(self, id):
        member = MemberModel.query.filter_by(id=id).first()
        if member is None:
            self.member_does_not_exist(id)
        return MemberModel.query.filter_by(id=id).first().to_json()

    def delete(self, id):
        member = MemberModel.query.filter_by(id=id).first()
        if member is None:
            self.member_does_not_exist(id)
        db.session.delete(member)
        return member.to_json()