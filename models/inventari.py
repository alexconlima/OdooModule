from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Item(models.Model):
    _name = 'inventari.item'
    _description = 'Item del inventari'

    product_id = fields.Char(string="Id Producte", required=True, unique=True)
    name = fields.Text(string="Nom item", required=True, unique=True)

    # Selecciona si la quantitat es mesura com unitats senceres o com, per exemple, kg que seria float
    unit_type = fields.Selection([
        ('unitat', 'Unitats'),
        ('decimal', 'Decimals')
    ], string='Mesura en', required=True, default='unit')

    quantity = fields.Float(string="Quantitat item", required=True, default=0.0)
    price = fields.Float(string="Price item", required=True, default=0.0, digits=(16, 2))
    value = fields.Float(string="Valor item", digits=(999999999, 2), compute='_compute_value', store=True)

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

    @api.constrains('quantity', 'price')
    def _check_positive_values(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError("La cantidad debe ser un valor positivo.")
            if record.price < 0:
                raise ValidationError("El precio debe ser un valor positivo.")