from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _default_validity = 7

    price = fields.Float()
    status = fields.Selection([("accepted","Accepted"),("refused","Refused")],copy=False)
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one("estate.property",required=True)
    validity_days = fields.Integer(string="Validity (Days)",default=_default_validity)
    deadline = fields.Date(compute="_getDeadline",inverse="_inverseDeadline",default=fields.Date.today()+relativedelta(days=_default_validity))

    @api.depends("validity_days")
    def _getDeadline(self):
        for record in self:
            _from_date = record.create_date if record.create_date else fields.Date.today()
            record.deadline = _from_date + relativedelta(days=record.validity_days)

    def _inverseDeadline(self):
        for record in self:
            _from_date = record.create_date if record.create_date else fields.Date.today()
            record.validity_days = (record.deadline - _from_date.date()).days