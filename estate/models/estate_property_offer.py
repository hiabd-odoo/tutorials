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
    deadline = fields.Date(compute="_get_deadline",inverse="_inverse_deadline",default=fields.Date.today()+relativedelta(days=_default_validity))

    @api.depends("validity_days")
    def _get_deadline(self):
        for record in self:
            _from_date = record.create_date if record.create_date else fields.Date.today()
            record.deadline = _from_date + relativedelta(days=record.validity_days)

    def _inverse_deadline(self):
        for record in self:
            _from_date = record.create_date if record.create_date else fields.Date.today()
            record.validity_days = (record.deadline - _from_date.date()).days

    def accept_offer(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                offer.status = "accepted" if offer.id == record.id else "refused"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True
    def refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0
            record.status = 'refused'
        return True

    #Constraints
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The Offer Prices should be strictly positive.'
    )
