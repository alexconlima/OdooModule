from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Item(models.Model):
    _name = 'inventari.item'
    _description = 'Item del inventari'

    product_id = fields.Integer(string="Id Producte", required=True)
    name = fields.Text(string="Nom item", required=True)

    # Selecciona si la quantitat es mesura com unitats senceres o com, per exemple, kg que seria float
    unit_type = fields.Selection([
        ('unitat', 'Unitats'),
        ('decimal', 'Decimals')
    ], string='Mesura en', required=True, default='unitat')

    quantity = fields.Float(string="Quantitat item", required=True, default=0.0)
    min_stock = fields.Float(string="Estoc minim", required=True, default=0.0)
    price = fields.Float(string="Preu item", required=True, default=0.0, digits=(16, 2))
    value = fields.Float(string="Valor existències", digits=(999999999, 2), compute='_compute_value', store=True)

    low_stock = fields.Boolean(string="Baix d'estoc", compute='_compute_lowstock')

    # Té dependencia de quantity i price
    @api.depends('quantity', 'price')
    def _compute_value(self):
        for record in self:
            record.value = record.price * record.quantity

    # Si detecta canvi de tipus de mesura (en la creació tmb s'executa)
    @api.onchange('unit_type')
    def _compute_unit_type(self):
        for record in self:
            if record.unit_type == 'unitat':
                record.quantity = int(record.quantity)
                record.min_stock = int(record.min_stock)

    @api.constrains('quantity', 'price')
    def _check_positive_values(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError("La quantitat ha de ser un valor positiu.")
            if record.price < 0:
                raise ValidationError("El preu ha de ser un valor positiu.")

    @api.depends('quantity', 'min_stock')
    def _compute_lowstock(self):
        for record in self:
            if record.min_stock <= record.quantity:
                record.low_stock = True
