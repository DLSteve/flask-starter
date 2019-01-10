from flask_restplus import Resource, reqparse
from app.auth_utilities import permission_required
from .models.resets import named_reset, role_reset, RoleBasedAccountResetsDAO, NamedBasedAccountResetsDAO
from . import api_v1

reset = api_v1.namespace('resets', description='Resets API')

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, help='Entries to return per page (Default 1,000, Max 2,000)', location='args')


@reset.doc(responses={
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal Server Error'
})
class RoleResets(Resource):
    @reset.doc('list_role_resets')
    @reset.marshal_with(role_reset)
    @reset.expect(parser)
    @permission_required('api_pwr_read')
    def get(self, page=1):
        """Lists all role based account resets"""
        args = parser.parse_args()
        db_limit = args.get('limit')
        reset_list = RoleBasedAccountResetsDAO()
        if db_limit:
            reset_list.get_resets(page, db_limit)
        else:
            reset_list.get_resets(page)
        return reset_list


reset.add_resource(RoleResets, '/role', endpoint='role_resets')
reset.add_resource(RoleResets, '/role/<int:page>', endpoint='role_resets_paged')


@reset.doc(responses={
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal Server Error'
})
class NamedResets(Resource):
    @reset.doc('list_named_resets')
    @reset.marshal_with(named_reset)
    @reset.expect(parser)
    @permission_required('api_pwr_read')
    def get(self, page=1):
        """Lists all named based account resets"""
        args = parser.parse_args()
        db_limit = args.get('limit')
        reset_list = NamedBasedAccountResetsDAO()
        if db_limit:
            reset_list.get_resets(page, db_limit)
        else:
            reset_list.get_resets(page)
        return reset_list


reset.add_resource(NamedResets, '/named', endpoint='named_resets')
reset.add_resource(NamedResets, '/named/<int:page>', endpoint='named_resets_paged')
