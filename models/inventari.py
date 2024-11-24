from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Item(models.Model):
    _name = 'inventari.item'
    _description = 'Item del inventari'

    product_id = fields.Integer(string="Id Producte", required=True)
    name = fields.Text(string="Nom item", required=True)

    quantity = fields.Float(string="Quantitat item", required=True, default=0.0)
    min_stock = fields.Float(string="Estoc de seguretat", required=True, default=0.0)
    price = fields.Float(string="Preu item", required=True, default=0.0, digits=(16, 2))
    value = fields.Float(string="Valor existències", digits=(999999999, 2), compute='_compute_value', store=True)

    low_stock = fields.Boolean(string="Baix d'estoc", compute='_compute_lowstock')
    transactions = fields.One2many('inventari.transaction', 'item_id', string="Transaccions")


    # Té dependencia de quantity i price
    @api.depends('quantity', 'price')
    def _compute_value(self):
        for record in self:
            record.value = record.price * record.quantity

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
            if record.quantity >= record.min_stock:
                record.low_stock = False
            else:
                record.low_stock = True
