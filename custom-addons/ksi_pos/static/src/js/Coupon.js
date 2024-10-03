odoo.define('ksi_pos.Coupon', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    const rpc = require('web.rpc');
    const session = require('web.session');
    const concurrency = require('web.concurrency');
    const { Gui } = require('point_of_sale.Gui');
    const { float_is_zero,round_decimals } = require('web.utils');

    models.Order = models.Order.extend({
        
        // activateCode: async function (code) {
        //     const promoProgram = this.pos.promo_programs.find(
        //         (program) => program.promo_barcode == code || program.promo_code == code
        //     );
            
        //     console.log("PROMO PROGRAM :: ", promoProgram);
        //     console.log("THISS :: ", this);

        //     if (promoProgram) {
        //         this.activePromoProgramIds.push(promoProgram.id);
        //         this.trigger('update-rewards');
        //     } else if (code in this.bookedCouponCodes) {
        //         Gui.showNotification('That coupon code has already been scanned and activated.');
        //     } else {
        //         const programIdsWithScannedCoupon = Object.values(this.bookedCouponCodes).map(
        //             (couponCode) => couponCode.program_id
        //         );
        //         const customer = this.get_client();
        //         const { successful, payload } = await rpc.query({
        //             model: 'pos.config',
        //             method: 'use_coupon_code',
        //             args: [
        //                 [this.pos.config.id],
        //                 code,
        //                 this.creation_date,
        //                 customer ? customer.id : false,
        //                 programIdsWithScannedCoupon,
        //             ],
        //             kwargs: { context: session.user_context },
        //         });
        //         if (successful) {
        //             this.bookedCouponCodes[code] = new CouponCode(code, payload.coupon_id, payload.program_id);
        //             this.trigger('update-rewards');
        //         } else {
        //             Gui.showNotification(payload.error_message);
        //         }
        //     }
        // },
        
        _getProductRewards: function (program, coupon_id) {
            const totalQuantity = this._getRegularOrderlines()
                .filter((line) => {
                    return program.valid_product_ids.has(line.product.id);
                })
                .reduce((quantity, line) => quantity + line.quantity, 0);

            const freeQuantity = computeFreeQuantity(
                totalQuantity,
                program.rule_min_quantity,
                program.reward_product_quantity
            );
            console.log("freeQuantity ::: ", freeQuantity);
            if (freeQuantity === 0) {
                return [[], 'Zero free product quantity.'];
            } else {
                const rewardProduct = this.pos.db.get_product_by_id(program.reward_product_id[0]);
                const discountLineProduct = this.pos.db.get_product_by_id(program.discount_line_product_id[0]);
                return [
                    [
                        new Reward({
                            product: discountLineProduct,
                            unit_price: -rewardProduct.lst_price,
                            quantity: freeQuantity,
                            program: program,
                            tax_ids: rewardProduct.taxes_id,
                            coupon_id: coupon_id,
                        }),
                    ],
                    null,
                ];
            }
        },
    })

});