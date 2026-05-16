{
    'name': 'Sale Order Approval',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Require manager approval for sale orders above a configured amount',
    'description': """
Sale Order Approval — by Technical Rajni
=========================================
Add an approval workflow to sale orders.

Features:
- Configurable approval threshold amount per company
- Orders above threshold require manager approval
- Approve / Refuse buttons for managers
- Email notification to manager on submission
- Email notification to salesperson on approval/refusal
- Reason for refusal
- Approval history log
- Works with multi-company
    """,
    'author': 'Technical Rajni',
    'website': 'https://www.technicalrajni.com',
    'license': 'OPL-1',
    'depends': ['sale', 'mail'],
    'data': [
        'security/sale_approval_security.xml',
        'security/ir.model.access.csv',
        'data/mail_templates.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 15.00,
    'currency': 'USD',
}
