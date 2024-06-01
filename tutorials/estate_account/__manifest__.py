{
    'name': "Invoicing Property",
    'description': """
                    Link module for creating invoice for estate properties
                    """,
      'data':[
        'views/inherit_view.xml',
        'views/inherit_estate_property_views.xml',

        'security/ir.model.access.csv'
    ],
    'depends': ['estate', 'account'],
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
