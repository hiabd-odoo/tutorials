from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _default_validity = 7

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity_days = fields.Integer(string="Validity (Days)", default=_default_validity)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline",
                           default=fields.Date.today() + relativedelta(days=_default_validity))
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    # Constraints
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The Offer Prices should be strictly positive.'
    )

    @api.depends("validity_days")
    def _compute_deadline(self):
        for record in self:
            _from_date = record.create_date if record.create_date else fields.Date.today()
            record.deadline = _from_date + relativedelta(days=record.validity_days)

    def _inverse_deadline(self):
        for record in self:
            _from_date = record.create_date if record.create_date else fields.Date.today()
            record.validity_days = (record.deadline - _from_date.date()).days

    def accept_offer(self):
        refused = self.property_ids.offer_ids - self
        refused.status = "refused"
        self.status = "accepted"

        for record in self:
            record.property_id.update({
                "selling_price": record.price,
                "buyer_id": record.partner_id,
                "state": "offer_accepted"
            })
        return True

    def refuse_offer(self):
        self.property_id.update({
            "selling_price": 0,
            "state": "offer_received"
        })
        self.status = "refused"
        return True

