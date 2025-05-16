# -*- coding: utf-8 -*-
from odoo import fields, models


class ChannelExtension(models.Model):
    _inherit = "slide.channel"

    instructor_id = fields.Many2one("res.users", string="Main Instructor")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")


class SlideExtension(models.Model):
    _inherit = "slide.slide"

    evaluation_required = fields.Boolean(string="Evaluation Required", default=False)


class ChannelPartnerExtension(models.Model):
    _inherit = "slide.channel.partner"

    attendance = fields.Float(string="Attendance Percentage", default=0.0)
    hr_notes = fields.Text(string="HR Notes")


class FeedbackForm(models.Model):
    _name = "photrain.feedback"
    _description = "Feedback Form"

    user_id = fields.Many2one("res.users", string="User")
    course_id = fields.Many2one("slide.channel", string="Course")
    category = fields.Selection(
        [
            ("course", "Course Content"),
            ("instructor", "Instructor"),
            ("platform", "Learning Platform"),
            ("general", "General"),
        ],
        string="Category",
    )
    comment = fields.Text(string="Comment")
    rating = fields.Selection(
        [
            ("1", "Poor"),
            ("2", "Fair"),
            ("3", "Average"),
            ("4", "Good"),
            ("5", "Excellent"),
        ],
        string="Rating",
    )
    submission_date = fields.Datetime(
        string="Submission Date", default=fields.Datetime.now
    )
