from odoo import models
from odoo.orm.commands import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        for record in self:
            self.env["account.move"].create([
                {
                    "partner_id":record.buyer_id.id,
                    "move_type":"out_invoice",
                    "invoice_line_ids": [
                        Command.create({
                            "name":record.name,
                            "quantity":1,
                            "price_unit":0.6*record.selling_price,
                        }),
                        Command.create({
                            "name":"administrative fees",
                            "quantity":1,
                            "price_unit":100,
                        }),
                    ]
                }])
        return super().sell_property()
