from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component

from ..pydantic_models.bank_account import BankAccountOut
from ..pydantic_models.info import Country, PersonType, State
from ..pydantic_models.user import UserIn, UserOut, UserShort


class UserService(Component):
    _inherit = 'base.rest.service'
    _name = 'user.service'
    _usage = 'user'
    _collection = 'photovoltaic_api.services'


    @restapi.method(
        [(['/'], 'GET')],
        output_param=restapi.PydanticModel(UserOut)
    )
    def get(self):
        return self._to_pydantic(self.env.user.partner_id)

    @restapi.method(
        [(['/'], 'PUT')],
        input_param=restapi.PydanticModel(UserIn),
        output_param=restapi.PydanticModel(UserOut)
    )
    def update(self, user_in):
        user_dict = user_in.dict(exclude_unset=True, exclude={'representative'})

        partner = self.env.user.partner_id
        partner.write(user_dict)

        if (partner.company_type == 'company' and partner.child_ids and user_in.representative):
            representative = partner.child_ids[0]
            representative.write(user_in.representative.dict(exclude_unset=True))

        self.env.user.sudo().write({'login': partner.vat})

        return self._to_pydantic(partner)

    #Private methods
    def _to_pydantic(self, user):

        representative = None
        if (user.company_type == 'company' and user.child_ids):
            representative = UserShort.from_orm(user.child_ids[0])
        
        return UserOut.parse_obj({
            'id': user.id,
            'person_type': user.company_type,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'street': user.street,
            'additional_street': user.street2,
            'zip': user.zip,
            'city': user.city,
            'state': State.from_orm(user.state_id),
            'country': Country.from_orm(user.country_id),
            'email': user.email,
            'phone': user.phone,
            'alias': user.alias,
            'vat': user.vat,
            'gender': user.gender_partner,
            'birthday': user.birthday,
            'bank_accounts': user.bank_ids.mapped(lambda b: BankAccountOut.from_orm(b)),
            'representative': representative
        })
