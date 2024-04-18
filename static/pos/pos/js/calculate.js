
// Calculate grand total
function calculateGrandTotal() {
    let subtotal = $('#subtotal').val();
    let subTotalField = $('#grandTotal');
    let invoice_discount_type = $('#invoice__discount__type').find("option:selected").val();
    let amount = $('#invoice_discount').val();

    const inputAmount = amount == '' ? 0 : amount;

    if (invoice_discount_type === 'percent'){
        var invoiceDiscountAmount = (parseInt(subtotal) * inputAmount / 100);
    }else{
        var invoiceDiscountAmount = (inputAmount);
    }
    $('#total_discount_ammount').val(invoiceDiscountAmount);
    var dicounted_sub_total = subtotal-invoiceDiscountAmount;


    let taxInputAmount =  $('#tax_amount').val();
    let taxValue = taxInputAmount == '' ? 0 : taxInputAmount;
    const tax = (dicounted_sub_total * parseInt(taxValue)) / 100;
    // const totatVatTax = !isNaN(tax) ? tax : 0;
    const total = dicounted_sub_total + tax;

    subTotalField.val(amountFormatted(total));
    subTotalField.data('grandtotal', amountFormatted(total));
    $('#net_total_text').text(amountFormatted(total));
    $('#n_total').val(amountFormatted(total));
}


function amountFormatted(amount) {
    return amount.toFixed(2)
}

function showError(message){
    toastr.error(message, {
        CloseButton: true,
        ProgressBar: true,
        "positionClass": "toast-top-right",
    });
}
