$(document).ready(function(){

    // Event listener for the change event of the select element
    $('#search-results').on('click', 'li', function() {
        var selectedOptionId = $(this).data('value'); // Retrieve the value (ID) from the data attribute of the clicked li element

        $.ajax({
            url: '/add-search-stock/',  // Replace with the URL of your backend endpoint
            method: 'GET',
            data: {
                'selected_option': selectedOptionId
            },
            success: function(response) {
                window.location.reload();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);  // Log any errors
            }
        });
    });

    // Event listener for the input event of the search input field
    $('#search-input').on('input', function() {
        var query = $(this).val();
        $.ajax({
            url: "/search-stock/",
            data: {
                'query': query
            },
            dataType: 'json',
            success: function(data) {
                $('#search-results').empty();
                for (var i = 0; i < data.length; i++) {
                    var optionText = '<img src="' + data[i].image + '" class="option-image" style="height:50px;width:50px;"> ' +
                                     '<strong>' + data[i].drug_name + '</strong> - ' +
                                     data[i].generic_name + ' (' +
                                     data[i].manufacure_name + ') - $' +
                                     data[i].price;
                    // Change appending option to li
                    $('#search-results').append('<li data-value="' + data[i].id + '">' + optionText + '</li>');
                }
                $('#search-results').show();
            }
        });
    });
});


// Assuming you have a unique identifier for each row, e.g., data-id attribute
$('body').on('change', '.changePerUnitPrice', function() {
    var newValue = $(this).val();
    var purchaseId = $(this).data('id');
    var dataTypeValue = $(this).data('type-value');

    $.ajax({
        url: '/update-added-stock/',
        method: 'POST',
        data: {
            'purchase_id': purchaseId,
            'new_value': newValue,
            'data_type': dataTypeValue
        },
        success: function(response) {
            console.log('Updated successfully');
            window.location.reload();
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});

