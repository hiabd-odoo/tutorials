from odoo import _, models
from odoo.orm.commands import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        super().sell_property()

        vals_list = []

        for record in self:
            vals_list.append(
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
                })
        if vals_list:
            invoices = self.env["account.move"].create(vals_list)
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "name": _("Invoices"),
                "views": [[False, 'form']] if len(invoices) == 1 else [[False, "list"], [False, "form"]],
                "context": {"create": False},
                "domain": [('id', 'in', invoices.ids)],
                "res_id": invoices.id if len(invoices) == 1 else False,
            }
        return True
