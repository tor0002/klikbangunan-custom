from odoo import api, fields, models


class ParretoWizard(models.TransientModel):
    _name = 'parreto.wizard'

    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    company_id = fields.Many2one('res.company', string='Company')

    def data_pos_order_line(self):
        order_line_model = self.env['pos.order.line']
        domain = [
            ('create_date', '>=', self.date_start),
            ('create_date', '<=', self.date_end),
            ('product_id.company_id', '=', self.company_id.id)
        ]
        order_lines = order_line_model.search(domain)
        # print('dito check order_lines >>>>>>>>>>>>>>>>>>>>>>>', order_lines)
        for record in order_lines:
            name = record.name
            product = record.product_id.name
            subtotal = record.price_subtotal_incl
            # print('dito check name >>>>>>>>>>>>>>>>>', name)
            # print('dito check product >>>>>>>>>>>>>>>>>', product)
            # print('dito check subtotal >>>>>>>>>>>>>>>>>', subtotal)
        # product_ids = order_lines.mapped('product_id')
        # price_subtotals = order_lines.mapped('price_subtotal_incl')

        pos_order_line_wizard = self.env['pos.order.line.wizard']
        pos_order_line_wizard.search([]).unlink()
        for order_line in order_lines:
            values = {
                'name': order_line.name,
                'product_id': order_line.product_id.id,
                'subtotal': order_line.price_subtotal_incl
            }
            pos_order_line_wizard.create(values)
        # return order_lines
        return {
            'name': 'POS Order Lines Wizard',
            'view_mode': 'tree',
            'res_model': 'pos.order.line.wizard',
            'type': 'ir.actions.act_window',
            # 'domain': domain,
            'target': 'current',
        }

class PosOrderLineWizard(models.TransientModel):
    _name = 'pos.order.line.wizard'

    name = fields.Char('Name')
    # nama_product = fields.Char('Nama Product')
    product_id = fields.Many2one('product.product', string='Product')
    subtotal = fields.Float('Subtotal')
    percentage = fields.Float('Percentage', compute='_compute_percentage')
    total_percentage = fields.Float('Total Percentage', compute='_compute_total_percentage')
    akumulasi_percentage = fields.Float('Akumulasi Percentage', compute='_compute_akumulasi_percentage')
    evaluation = fields.Selection([
        ('very_fast', 'Very Fast'),
        ('fast', 'Fast'),
        ('slow', 'Slow')
    ], 'Evaluation', compute='_compute_evaluation')

    @api.depends('subtotal')
    def _compute_percentage(self):
        for rec in self:
            total = sum(rec.search([]).mapped('subtotal'))
            # print('dito check total>>>>>>>>>>>>>>>>>', total)
            if total != 0:
                percent = rec.subtotal/total * 100
                rec.percentage = percent
            else:
                rec.percentage = 0

    @api.depends('percentage')
    def _compute_total_percentage(self):
        for record in self:
            same_product_records = self.filtered(
                lambda r: r.product_id == record.product_id)
            total_percentage = sum(same_product_records.mapped('percentage'))
            same_product_records.update({'total_percentage': total_percentage})

    @api.depends('total_percentage')
    def _compute_akumulasi_percentage(self):
        # domain = self._get_filter_domain()
        # all_records = self.search(domain)
        all_records = self.search([])
        # print('dito check all records >>>>>>>>>>>>>>>>>>>>>>', all_records)
        sorted_records = sorted(
            all_records, key=lambda r: r.total_percentage, reverse=True)
        # sorted_records = all_records.sorted(key=lambda r: r.total_percentage, reverse=True)
        # print('dito check sorted record >>>>>>>>>>>>>>>>>>>>>>', sorted_records)
        akumulasi = []
        total = 0.0
        previous_percentage = None
        for record in sorted_records:
            if record.total_percentage == previous_percentage:
                total += 0  # Jika nilai total_percentage sama, tambahkan dengan 0
            else:
                total += record.total_percentage

            akumulasi.append(total)
            # print('dito check total >>>>>>>>>>>>>>>>>>>>>>', total)

            previous_percentage = record.total_percentage

        # print('dito check akumulasi >>>>>>>>>>>>>>>>>>>>>>', akumulasi)

        for index, record in enumerate(sorted_records):
            record.akumulasi_percentage = akumulasi[index]

    @api.depends('akumulasi_percentage')
    def _compute_evaluation(self):
        for rec in self:
            if rec.akumulasi_percentage < 50.0:
                rec.evaluation = 'very_fast'
            elif rec.akumulasi_percentage > 50.0 and rec.akumulasi_percentage < 70.0:
                rec.evaluation = 'fast'
            elif rec.akumulasi_percentage > 70.0 and rec.akumulasi_percentage < 100.0:
                rec.evaluation = 'slow'
            else:
                rec.evaluation = 'slow'

    def action_change_all(self):
        all_records = self.search([])

        product_model = self.env['product.product']
        for record in all_records:
            product = product_model.search(
                [('id', '=', record.product_id.id)], limit=1)
            if product:
                product.parreto = record.evaluation
    

#     def _data_pos_order_line(self):
#         return self.env['pos.order.line'].browse(self._context.get('active_ids'))
