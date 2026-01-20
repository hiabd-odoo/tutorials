from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "estate_property"
    _postcode = "estate_property"
    _date_availability = "estate_property"
    _expected_price = "estate_property"
    _selling_price = "estate_property"
    _bedrooms = "estate_property"
    _living_area = "estate_property"
    _facades = "estate_property"
    _garage = "estate_property"
    _garden = "estate_property"
    _garden_area = "estate_property"
    _garden_orientation = "estate_property"
    

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden Orientation',selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    