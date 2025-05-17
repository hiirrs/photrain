{
    'name': 'eLearning Analytics',
    'version': '1.0',
    'summary': 'Dashboard analitik untuk eLearning',
    'description': 'Melacak metrik siswa dan course untuk modul eLearning',
    'category': 'eLearning',
    'author': 'Your Name',
    'depends': ['website_slides'],
    'data': [
        'security/ir.model.access.csv',
        'views/analytics_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
