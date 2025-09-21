"use strict";
var KTAppEcommerceProducts = function() {
    var t, e, o = () => {
        t.querySelectorAll('[data-kt-ecommerce-product-filter="delete_row"]').forEach((t => {
            t.addEventListener("click", (function(t) {
                t.preventDefault();
                const o = t.target.closest("tr"),
                    n = o.querySelector('[data-ic-filter="filter_content"]').innerText;
            }))
        }))
    };
    return {
        init: function() {
            (t = document.querySelector("#kt_ecommerce_products_table")) && ((e = $(t).DataTable({
                info: !1,
                order: [],
                pageLength: 10,
                columnDefs: [{
                    orderable: !1,
                    targets: 0
                }, {
                    orderable: !1,
                    targets: 6
                }]
            })).on("draw", (function() {
                o()
            })), document.querySelector('[data-ic-filter="search"]').addEventListener("keyup", (function(t) {
                e.search(t.target.value).draw()
            })), (() => {
                const t = document.querySelector('[data-ic-filter="status"]');
                $(t).on("change", (t => {
                    let o = t.target.value;
                    "all" === o && (o = ""), e.column(6).search(o).draw()
                }))
            })(), o())
        }
    }
}();

$(document).ready(function () {
    KTAppEcommerceProducts.init()
});
