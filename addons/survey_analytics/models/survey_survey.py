from odoo import models, fields, api

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    total_responses = fields.Integer(string="Total Responses", compute='_compute_total_responses')
    avg_rating = fields.Float(string="Average Rating", compute='_compute_avg_rating')

    @api.depends('user_input_ids')
    def _compute_total_responses(self):
        for record in self:
            record.total_responses = self.env['survey.user_input'].search_count([
                ('survey_id', '=', record.id),
                ('state', '=', 'done')
            ])

    @api.depends('user_input_ids.user_input_line_ids')
    def _compute_avg_rating(self):
        for record in self:
            rating_total = 0
            rating_count = 0
            for user_input in record.user_input_ids.filtered(lambda x: x.state == 'done'):
                for line in user_input.user_input_line_ids:
                    if line.question_id.question_type == 'simple_choice' and line.value_suggested:
                        val = line.value_suggested.value
                        if val.isdigit():
                            rating_total += int(val)
                            rating_count += 1
            record.avg_rating = rating_total / rating_count if rating_count > 0 else 0.0
