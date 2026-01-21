from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"


    name = fields.Char(required=True,string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=fields.Date.today()+relativedelta(months=3),string='Available From')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    hasGarage = fields.Boolean(string="Garage")
    hasGarden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(selection=[
            ('new','New'),
            ('offerReceived','Offer Received'),
            ('offerAccepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')], 
        default='new',
        required=True,
        copy=False)
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner",copy=False)
    salesperson_id = fields.Many2one("res.users",default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer","property_id")

    