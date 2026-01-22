from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    #Constraints
    _check_unique = models.Constraint(
        'unique(name)',
        'Tag name should be unique.'
    )