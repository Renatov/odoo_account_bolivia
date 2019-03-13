{
    'name': 'Comprueba el cambio diario de moneda ',
    'version': '1.0',
    'category': 'Accounting Management',
    'description': """
Use las caracteristicas contables en bolivia.
============================================

Carcteristicas:
-----------
- Actualice diariamiente el tipode cambio en Bolivianos, dolares, euros, UFVs
- Abre un formulario automaticamente para que se pueda actualizar si no se ha realizado el registro del cambio del dia

""",
    'author': 'Prosebol',
    'website': 'https://www.prosebol.com/',
    'images': [],
    'license': 'AGPL-3',
    'depends': ['account'],
    'data': [
        'views/account_updatechangemoney_template.xml',
    ],
    'demo': [],
    'test': [],
    'qweb': ['static/src/xml/account_money_change_popup.xml'],
    'active': True,
    'installable': True,
    'auto_install': False,
}
