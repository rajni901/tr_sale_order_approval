from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('not_required', 'Not Required'),
        ('pending', 'Waiting Approval'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], string='Approval Status',
        default='not_required',
        copy=False,
        tracking=True,
    )
    approval_required = fields.Boolean(
        string='Approval Required',
        compute='_compute_approval_required',
        store=True,
    )
    approved_by = fields.Many2one(
        'res.users',
        string='Approved By',
        readonly=True,
        copy=False,
    )
    approved_date = fields.Datetime(
        string='Approved On',
        readonly=True,
        copy=False,
    )
    refused_by = fields.Many2one(
        'res.users',
        string='Refused By',
        readonly=True,
        copy=False,
    )
    refused_reason = fields.Text(
        string='Refusal Reason',
        readonly=True,
        copy=False,
    )

    @api.depends('amount_total', 'company_id')
    def _compute_approval_required(self):
        param = self.env['ir.config_parameter'].sudo()
        required = param.get_param('tr_sale_approval.required', False)
        min_amount = float(param.get_param('tr_sale_approval.min_amount', 0))
        for order in self:
            if required:
                order.approval_required = order.amount_total >= min_amount
            else:
                order.approval_required = False

    def action_confirm(self):
        for order in self:
            if order.approval_required and order.approval_state not in ('approved',):
                order.approval_state = 'pending'
                order._send_approval_request_email()
                raise UserError(_(
                    'Order "%s" requires manager approval before confirmation.\n'
                    'An email has been sent to the approver.', order.name
                ))
        return super().action_confirm()

    def action_approve(self):
        self.ensure_one()
        if not self.env.user.has_group('sale.group_sale_manager'):
            raise UserError(_('Only Sales Managers can approve sale orders.'))
        self.write({
            'approval_state': 'approved',
            'approved_by': self.env.user.id,
            'approved_date': fields.Datetime.now(),
        })
        self.message_post(
            body=_('Order approved by %s.', self.env.user.name),
            subtype_xmlid='mail.mt_note',
        )
        self._send_approval_result_email(approved=True)
        return super(SaleOrder, self).action_confirm()

    def action_refuse(self):
        self.ensure_one()
        if not self.env.user.has_group('sale.group_sale_manager'):
            raise UserError(_('Only Sales Managers can refuse sale orders.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Refuse Reason'),
            'res_model': 'sale.approval.refuse.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }

    def action_reset_approval(self):
        self.write({
            'approval_state': 'not_required',
            'approved_by': False,
            'approved_date': False,
            'refused_by': False,
            'refused_reason': False,
        })

    def _send_approval_request_email(self):
        template = self.env.ref(
            'tr_sale_order_approval.mail_template_sale_approval_request',
            raise_if_not_found=False,
        )
        if template:
            template.send_mail(self.id, force_send=True)

    def _send_approval_result_email(self, approved=True):
        xmlid = (
            'tr_sale_order_approval.mail_template_sale_approval_approved'
            if approved else
            'tr_sale_order_approval.mail_template_sale_approval_refused'
        )
        template = self.env.ref(xmlid, raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)
