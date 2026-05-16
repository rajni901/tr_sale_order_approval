from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleApprovalRefuseWizard(models.TransientModel):
    _name = 'sale.approval.refuse.wizard'
    _description = 'Sale Order Refusal Reason'

    order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    reason = fields.Text(string='Reason for Refusal', required=True)

    def action_refuse(self):
        self.order_id.write({
            'approval_state': 'refused',
            'refused_by': self.env.user.id,
            'refused_reason': self.reason,
        })
        self.order_id.message_post(
            body=_('Order refused by %s. Reason: %s', self.env.user.name, self.reason),
            subtype_xmlid='mail.mt_note',
        )
        self.order_id._send_approval_result_email(approved=False)
