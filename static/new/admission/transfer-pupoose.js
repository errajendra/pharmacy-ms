$(document).ready(function() {
    $('.purpose_transfer').change(function() {
        var confirmMsg = 'Are you sure you want to transfer this admission?';
        if (confirm(confirmMsg)) {
            var transferValue = $(this).val();
            var admissionId = $(this).data('admission-id');
            var url = '/ajax/transfer-admission-purpose/';

            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'transfer': transferValue,
                    'admission_id': admissionId,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    if(response.status == 200) {
                        window.location.reload();
                    } else {
                        alert('Admission transferred successfully!');
                    }
                },
                error: function(xhr, textStatus, errorThrown) {
                    alert('Error transferring admission: ' + xhr.responseText);
                }
            });
        }
    });
});