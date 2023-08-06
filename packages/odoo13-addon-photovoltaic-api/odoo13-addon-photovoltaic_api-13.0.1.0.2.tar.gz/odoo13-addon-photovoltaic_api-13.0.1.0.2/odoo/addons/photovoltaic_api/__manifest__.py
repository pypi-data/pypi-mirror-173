{
    'name': 'Photovoltaic API',
    'version': '13.0.1.0.2',
    'depends': [
        'base_rest',
        'auth_api_key',
        'auth_jwt',
        'base_rest_pydantic',
        'pydantic',
        'photovoltaic_mgmt',
        'photovoltaic_mgmt_extended',
        'photovoltaic_participant_liquidations',
        'photovoltaic_participant_activities',
        'portal',
        'base_vat'
    ],
    "external_dependencies": {
        "python": [
            "pydantic[email]",
            "pyjwt"
        ]
    },
    'author': 'Librecoop',
    'category': 'Sales',
    'description': '''
    This module provides a REST API to interact with various modules of the photovoltaic suite developed by Domatix and Librecoop
    ''',
    'installable': True,
    'auto_install': True,
    'data': [
        'data/data.xml'
    ]
}
