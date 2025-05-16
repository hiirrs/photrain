# -*- coding: utf-8 -*-
{
    'name': "Photrain Extension",
    'summary': "Extensions for PT. Piktura Lensa Nusa E-Learning",
    'description': """
        Extended e-learning functionality for PT. Piktura Lensa Nusa (Jonas Photo)
        
        This module extends the standard Odoo eLearning to add:
        - Custom instructor assignment
        - Course scheduling
        - Attendance tracking
        - Enhanced evaluation features
        - Feedback and tracer study collection
    """,
    'author': "Development Team",
    'category': 'Education',
    'version': '1.0',
    'depends': [
        'base', 
        'mail', 
        'website_slides', 
        'survey',
        'hr'
    ],
    
    'data': [
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/evaluation_views.xml',
        'views/feedback_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
