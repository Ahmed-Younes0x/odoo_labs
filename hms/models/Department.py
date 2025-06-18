from odoo import models, fields

class Department(models.Model):
    _name='department'
    name=fields.Char()
    capacity=fields.Integer()
    is_open=fields.Boolean()
    patient_ids = fields.One2many('hms.patient', 'department_id', string='Patients')