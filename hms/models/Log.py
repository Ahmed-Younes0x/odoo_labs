from odoo import models, fields


class Log(models.Model):
    _name='hms.patient.log'
    description=fields.Text()
    patient=fields.Many2one(comodel_name='hms.patient')
    