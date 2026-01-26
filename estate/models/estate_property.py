from odoo import _, api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.orm.decorators import ondelete
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3),
                                    string='Available From')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    has_garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')],
        default='new',
        required=True,
        copy=False)
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Integer(compute='_compute_best_price', string="Best Offer")

    # Constraints
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The Expected Price should be strictly positive.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The Selling Price should be a positive value.'
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and float_compare(record.selling_price,
                                                                            0.9 * record.expected_price, 2) <= 0:
                raise ValidationError(
                    _("Selling price cannot be less than 90% of the expected price.\nIf you have already accepted offers, please refuse them before updating your property's expected price"))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        result = self.env['estate.property.offer']._read_group([('property_id', '=', self.ids)], ["property_id"],
                                                               ["price:max"])
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
                raise UserError(_('A sold property cannot be cancelled.'))
        return True

    def sell_property(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise UserError(_('A cancelled property cannot be sold.'))
        return True

    @ondelete(at_uninstall=False)
    def _check_deletion_state(self):
        for record in self:
            if record.state not in ('new','cancelled'):
                raise ValidationError(_('Only New or Cancelled properties can be deleted.'))
