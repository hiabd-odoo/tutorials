from odoo import models
from odoo.orm.fields_relational import One2many


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = One2many('estate.property','salesperson_id', domain="['|',('state', '=', 'new'),('state', '=', 'offer_received')]")