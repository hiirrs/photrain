from odoo import models, fields, api

class SurveyFeedback(models.Model):
    _name = 'survey.feedback'
    _description = 'Feedback for E-Learning'
    _inherit = ['mail.thread']

    name = fields.Char(string="Responder Name", required=True)
    email = fields.Char(string="Email")
    feedback_text = fields.Text(string="Feedback", required=True)
    rating = fields.Selection([
        ('1', 'Very Poor'),
        ('2', 'Poor'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Excellent'),
    ], string="Rating", required=True)
    submitted_on = fields.Datetime(string="Submitted On", default=fields.Datetime.now)

    # Tambahan analitik
    total_feedback = fields.Integer(string="Total Feedback", compute='_compute_total_feedback')
    avg_rating = fields.Float(string="Average Rating", compute='_compute_avg_rating')

    @api.depends('rating')
    def _compute_total_feedback(self):
        for record in self:
            record.total_feedback = self.env['survey.feedback'].search_count([])

    @api.depends('rating')
    def _compute_avg_rating(self):
        for record in self:
            feedbacks = self.env['survey.feedback'].search([])
            ratings = [int(f.rating) for f in feedbacks if f.rating]
            record.avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
