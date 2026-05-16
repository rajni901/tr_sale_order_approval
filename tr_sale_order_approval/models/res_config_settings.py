from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_approval_required = fields.Boolean(
        string='Require Approval for Sale Orders',
        config_parameter='tr_sale_approval.required',
    )
    sale_approval_min_amount = fields.Float(
        string='Minimum Amount for Approval',
        config_parameter='tr_sale_approval.min_amount',
        help='Orders above this amount will require manager approval. Set 0 to require approval for all orders.',
    )
    sale_approval_group = fields.Selection([
        ('sale.group_sale_manager', 'Sales Manager'),
        ('base.group_system', 'Administrator'),
    ], string='Approval Group',
        config_parameter='tr_sale_approval.group',
        default='sale.group_sale_manager',
    )
