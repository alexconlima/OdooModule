{
    'name': 'Inventari Simple',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Mòdul simple per gestionar l\'inventari',
    'description': """
        Mòdul simple per gestionar l\'inventari.
    """,
    'author': 'Claudia Palacio, Marco Muñoz, Marc Sarrias, Alex Bes',
    'depends': ['base'],
    'data': [
        'views/item.xml',
        'views/transaction.xml',
        'views/category.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
        ],
	"application": True,
	"installable": True,
    "website": "https://github.com/alexconlima/OdooModule",
}
