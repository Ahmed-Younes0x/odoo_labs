from odoo import models, fields

class Doctor(models.Model):
    _name='doctor'
    first_name=fields.Char()
    last_name=fields.Char()
    image=fields.Binary()
    patient_ids = fields.One2many('hms.patient', 'doctor_id', string='Patients')