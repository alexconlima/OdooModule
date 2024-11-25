from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Transaction(models.Model):
    _name = 'inventari.transaction'
    _description = 'Transaccio inventari'

    item_id = fields.Many2one('inventari.item', string="Item", required=True)

    transaction_type = fields.Selection([
            ('entrada', 'Entrada'),
            ('sortida', 'Sortida')
        ], string="Tipus de transaccio", required=True)

    quantity=fields.Float(string="Quantitat", required=True)
    date=fields.Datetime(string="Data de transaccio", default=fields.Datetime.now, required=True)
    total=fields.Float(string="Total", compute="_compute_total", store=True)

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("La quantitat ha de ser un valor positiu.")
    @api.depends('quantity')
    def _compute_total(self):
        for record in self:
            record.total = record.quantity*record.item_id.price

    @api.model
    def create(self, valors):
        transaction = super(Transaction, self).create(valors)
        item = transaction.item_id

        if transaction.transaction_type == 'entrada':
            item.quantity += transaction.quantity
        # Sortida
        else:
            if item.quantity < transaction.quantity:
                raise ValidationError("No hi ha suficient estoc per aquesta sortida")
            else:
                item.quantity -= transaction.quantity

        return transaction

