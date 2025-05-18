# -*- coding: utf-8 -*-
# from odoo import http


# class ElearningAnalytics(http.Controller):
#     @http.route('/elearning_analytics/elearning_analytics', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/elearning_analytics/elearning_analytics/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('elearning_analytics.listing', {
#             'root': '/elearning_analytics/elearning_analytics',
#             'objects': http.request.env['elearning_analytics.elearning_analytics'].search([]),
#         })

#     @http.route('/elearning_analytics/elearning_analytics/objects/<model("elearning_analytics.elearning_analytics"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('elearning_analytics.object', {
#             'object': obj
#         })
