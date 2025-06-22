from odoo import models, fields, api
from odoo.exceptions import ValidationError


class customerss(models.Model):
    _inherit='res.partner'
    
    patientIdd = fields.Many2one('hms.patient', string='related patient')
    # patientIdd = fields.Char()
    
    @api.constrains('patientIdd')
    def _check_unique_patient_email(self):
        for rec in self:
            if rec.patientIdd and rec.patientIdd.email:
                other = self.search([
                    ('id', '!=', rec.id),
                    ('patientId', '!=', False),
                    ('patientId.email', '=', rec.patientIdd.email)
                ])
                if other:
                    raise ValidationError(
                        f"Patient that has email '{rec.patientIdd.email}' is already linked to a customer."
                    )