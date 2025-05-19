{
    "name": "Survey Analytics for E-Learning",
    "version": "1.0",
    "category": "Tools",
    "summary": "Feedback and survey analytics for e-learning materials",
    "depends": ["base", "mail", "survey"],
    "data": [
        "security/ir.model.access.csv",
        "views/survey_feedback_views.xml",
        "views/survey_survey_views.xml",
    ],
    "installable": True,
    "application": True,
    'license': 'LGPL-3',
}
