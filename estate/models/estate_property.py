from odoo import fields, models
from dateutil.relativedelta import relativedelta

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
    date_availability = fields.Date(copy=False,default=fields.Date.today()+relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden Orientation',selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(selection=[
            ('new','New'),
            ('offer received','Offer Received'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')], 
        default='new',
        required=True,
        copy=False)
    