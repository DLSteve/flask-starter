from flask_restplus import fields
from app.models import RoleAccountPasswordReset, NamedAccountPasswordReset
from app.api.v1 import api_v1


reset_base = api_v1.model('ResetBase', {
    'id': fields.String(description='Reset ID.'),
    'agent': fields.String(description='Account that reset the password.'),
    'acct': fields.String(description='The Account that had its password reset.'),
    'acct_location': fields.String(description='Warehouse location of the account reset.'),
    'reset_date': fields.DateTime(description='Date of the reset.'),
    'reset_day': fields.String(description='Day of the week.'),
    'reset_type': fields.String(description='If the reset was self-service or not.')
})


reset_ext = api_v1.inherit('ResetExt', reset_base, {
    'employee_type': fields.String(description='Employee type.')
})


role_reset = api_v1.model('RoleBasedAccountResets', {
    'has_next': fields.Boolean(description='Query has more records.'),
    'next_num': fields.Integer(description='Number for the next page.'),
    'resets': fields.Nested(reset_base)
})


named_reset = api_v1.model('NamedBasedAccountResets', {
    'has_next': fields.Boolean(description='Query has more records.'),
    'next_num': fields.Integer(description='Number for the next page.'),
    'resets': fields.Nested(reset_ext)
})


class RoleBasedAccountResetsDAO:
    def __init__(self):
        self.has_next = False
        self.next_num = None
        self.resets = []

    def get_resets(self, page=1, per_page=1000):
        # Cap results at 2000 per page.
        if per_page > 2000 or per_page < 1:
            per_page = 2000

        # Prevent negative page numbers.
        if page < 1:
            page = 1
        resets = RoleAccountPasswordReset.query.order_by(
            RoleAccountPasswordReset.reset_date.asc()).paginate(page, per_page, False)
        if resets:
            if resets.has_next:
                self.has_next = True
                self.next_num = resets.next_num
            for r in resets.items:
                rst = {
                    'id': r.id,
                    'agent': r.agent,
                    'acct': r.acct,
                    'acct_location': r.acct_location,
                    'reset_date': r.reset_date,
                    'reset_day': r.reset_day,
                    'reset_type': r.reset_type
                }
                self.resets.append(rst)


class NamedBasedAccountResetsDAO:
    def __init__(self):
        self.has_next = False
        self.next_num = None
        self.resets = []

    def get_resets(self, page=1, per_page=1000):
        # Cap results at 2000 per page.
        if per_page > 2000 or per_page < 1:
            per_page = 2000

        # Prevent negative page numbers.
        if page < 1:
            page = 1
        resets = NamedAccountPasswordReset.query.order_by(
            NamedAccountPasswordReset.reset_date.asc()).paginate(page, per_page, False)
        if resets:
            if resets.has_next:
                self.has_next = True
                self.next_num = resets.next_num
            for r in resets.items:
                rst = {
                    'id': r.id,
                    'agent': r.agent,
                    'acct': r.acct,
                    'acct_location': r.acct_location,
                    'reset_date': r.reset_date,
                    'reset_day': r.reset_day,
                    'reset_type': r.reset_type,
                    'employee_type': r.type
                }
                self.resets.append(rst)
