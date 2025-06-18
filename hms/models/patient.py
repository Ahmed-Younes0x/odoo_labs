from odoo import models, fields


class Patient(models.Model):
    _name = "hms.patient"
    first_name = fields.Char(string='f_name')
    last_name = fields.Char(string='l_name')
    age = fields.Integer(string='age')
    history=fields.Char(string='history')
    CR_ratio=fields.Float('CR ratio')
    status = fields.Selection(selection=[('Undefined','Undefined'),('good','good'),('fair','fair'),('serious','serious')]
        ,string="status")
    address = fields.Text()
    PCR=fields.Boolean(string="PCR Test Done")
    blood_type = fields.Selection(selection=[('A','A'),('B','B'),('AB','AB'),('O','O')]
        ,string="Blood Tupe")
    birth_date = fields.Date()
    image = fields.Binary()
    department_id = fields.Many2one('department', string='Department')
    doctor_id = fields.Many2one('doctor', string='Doctor')
    department_capacity = fields.Integer(
        string='Department Capacity',
        related='department_id.capacity',
        readonly=True,
        store=False  # Don't store in database, compute on demand
    )
    
    def __str__(self):
        return self.first_name
    