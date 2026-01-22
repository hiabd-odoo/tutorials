from odoo import _, fields, models, api, exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

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
    has_garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
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
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Integer(compute='_compute_best_price',string="Best Offer")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        result = self.env['estate.property.offer']._read_group([('property_id','=',self.ids)],["property_id"],["price:max"])
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise UserError(_('A sold property cannot be cancelled!'))
        return True

    def sell_property(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise UserError('A cancelled property cannot be sold!')
        return True
