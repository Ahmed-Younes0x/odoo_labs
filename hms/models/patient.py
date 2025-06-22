from datetime import date
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = "hms.patient"
    first_name = fields.Char(string='f_name')
    last_name = fields.Char(string='l_name')
    email=fields.Char(string='email')
    age = fields.Integer(compute="compute_age", store=True)
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
        store=False  
    )
    logs=fields.One2many('hms.patient.log',inverse_name='patient')
    customer=fields.One2many('res.partner',inverse_name='patientIdd')
    
    def __str__(self):
        return self.first_name
    
    def create_stat_log(self):
        vals={
            'description':"Changed state to {self.status}",
            'patient': self.id
        }
        self.env['hms.patient.log'].create(vals)
    
    def create(self,vals):
        res = super(Patient,self).write(vals)
        for rec in self:
            rec.env['hms.patient.log'].create({'description':'Created','patient': rec.id})
        return res
    
    def write(self,vals):
        res = super(Patient,self).write(vals)
        print('here1')
        if 'status' in vals:
            print('here2')
            for rec in self:
                rec.create_stat_log()
        return res
    

    @api.depends('age', 'birth_date')
    def compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                print('here')
                rec.age = today.year - rec.birth_date.year - (
                        (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
                rec.PCR = True if rec.age < 30 else False
                print(f"Computed age for {rec.first_name}: {rec.age}")
            else:
                rec.age = 0

    @api.constrains('email')
    def validate_email(self):
        for rec in self:
            print(f"Validating email: {rec.email}")
            if rec.email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', rec.email):
                raise ValidationError("Please enter a valid email address.")
    
    def action_print_report(self):
        return self.env.ref('hms.statusreport').report_action(self)
