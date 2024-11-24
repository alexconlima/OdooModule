from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Item(models.Model):
    _name = 'inventari.item'
    _description = 'Item del inventari'

    product_id = fields.Text(string="Referencia producte", readonly=True)
    name = fields.Text(string="Nom producte", required=True)
    category = fields.Many2one('inventari.category', string="Categoria Producte")

    quantity = fields.Float(string="Quantitat", required=True, default=0.0)
    min_stock = fields.Float(string="Estoc de seguretat", required=True, default=0.0)
    price = fields.Float(string="Preu", required=True, default=0.0, digits=(16, 2))
    value = fields.Float(string="Valor existències", digits=(999999999, 2), compute='_compute_value', store=True)
    active = fields.Boolean(string="Actiu", required=True, default=True)

    low_stock = fields.Boolean(string="Baix d'estoc", compute='_compute_lowstock', store=True)
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

    @api.model
    def create(self, valors):
        item = super(Item, self).create(valors)
        
        p_id = self.search_count([])
        category = item.category

        if not category:
            item.product_id = ("000-"+str(p_id))
        else:
            item.product_id = (category.sigla + "-" +str(p_id))
        return item
