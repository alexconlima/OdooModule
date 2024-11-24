from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Categoria(models.Model):
    _name = 'inventari.category'
    _description = 'Categoria de productes'

    name = fields.Text(string="Nom categoria", required=True)
    sigla = fields.Char(string="Sigles de la categoria", required=True, size=3)
    products = fields.One2many('inventari.item', 'category', readonly=True)

    _sql_constraints = [('unique_sigla', 'unique(sigla)', 'Aquestes sigles ja existeixen.'), 
            ('sigla_not_000', "CHECK(sigla != '000')", "Les sigles '000' estan reservades.")]


