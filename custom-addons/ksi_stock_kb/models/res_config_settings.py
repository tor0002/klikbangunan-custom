from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """
      This class inherits from the `res.config.settings` model in Odoo and adds
       two boolean fields to the
      configuration settings page: `create_invoice_delivery_validate` and
      `auto_send_invoice`.
      """
    _inherit = "res.config.settings"

    is_create_invoice_delivery_validate = fields.Boolean(
        string="Auto Draft Invoice and Bill", config_parameter=
        'automatic_invoice_and_post.is_create_invoice_delivery_validate')
    is_create_post_invoice_delivery_validate = fields.Boolean(
        string="Auto Posted Invoice and Bill", config_parameter=
        'automatic_invoice_and_post.is_create_post_invoice_delivery_validate')

    is_auto_send_invoice = fields.Boolean(string="Auto Send Invoice",
                                          config_parameter=
                                          'automatic_invoice_and_post.is_auto_send_invoice')
