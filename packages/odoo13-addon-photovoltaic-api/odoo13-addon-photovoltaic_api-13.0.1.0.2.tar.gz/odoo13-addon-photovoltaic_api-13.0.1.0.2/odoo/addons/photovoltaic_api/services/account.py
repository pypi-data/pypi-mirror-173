from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
from odoo.exceptions import MissingError, UserError
import secrets
from datetime import datetime, timedelta
import jwt


class AccountService(Component):
    _inherit = 'base.rest.service'
    _name = 'account.service'
    _usage = 'account'
    _collection = 'photovoltaic_api.services'


    @restapi.method(
        [(['/signup_request'], 'POST')],
        input_param=restapi.CerberusValidator('_validator_signup_request'),
        auth='api_key'
    )
    def signup_request(self, **params):
        '''
        Request to create a user from a partner
        :param vat: VAT
        :return: Signup token
        '''
        partner = self.env['res.partner'].search([('vat', '=', params.get('vat'))])
        if len(partner) < 1:
            raise MissingError('Missing error')
        elif len(partner) > 1:
            raise UserError('Bad request')

        expiration = datetime.now() + timedelta(hours=1)
        partner.signup_prepare(expiration=expiration)
        return {
            'token': partner.signup_token,
            'email': partner.email,
            'name':  partner.name
        }

    @restapi.method(
        [(['/signup'], 'POST')],
        input_param=restapi.CerberusValidator('_validator_signup'),
        auth='api_key'
    )
    def signup(self, **params):
        '''
        Confirm signup with a signup token
        :param token: Signup token from signup_request
        :param password: Password
        :return: {VAT, JWT Token}
        '''
        token = params.get('token')
        password = params.get('password')

        partner = self.env['res.partner'].search([('signup_token', '=', token)])

        if len(partner) != 1:
            raise MissingError('Missing error')

        self.env['res.users'].signup({
            'login': partner.vat,
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
            'password': password
        }, token)

        user = self.env['res.users'].search([('login', '=', partner.vat)])

        return {
            'login': partner.vat,
            'jwt_token': self._get_token(user),
            'email': partner.email,
            'name':  partner.name
        }

    @restapi.method(
        [(['/login'], 'POST')],
        input_param=restapi.CerberusValidator('_validator_login'),
        auth='api_key'
    )
    def login(self, **params):
        '''
        Get JWT Token with login credentials
        :param vat: VAT
        :param password: Password
        :return: JWT Token
        '''
        user_id = self.env['res.users'].authenticate(
            '',
            params.get('vat'),
            params.get('password'),
            {'interactive': False})

        return self._get_token(self.env['res.users'].browse(user_id))


    # Private methods
    def _get_token(self, user):
        validator = self.env['auth.jwt.validator'].search([('name', '=', 'validator')])
        jwt_token = jwt.encode(
            {
                'aud': validator.audience,
                'iss': validator.issuer,
                'exp': datetime.now() + timedelta(weeks=4),
                'user_id': user.id
            },
            key=validator.secret_key,
            algorithm=validator.secret_algorithm,
        )
        return jwt_token

    def _validator_signup_request(self):
        return {
            'vat':      {'type': 'string'}
        }

    def _validator_signup(self):
        return {
            'token':    {'type': 'string'},
            'password': {'type': 'string'}
        }

    def _validator_login(self):
        return {
            'vat':      {'type': 'string'},
            'password': {'type': 'string'}
        }
