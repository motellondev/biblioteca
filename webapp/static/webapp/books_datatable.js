// Set DataTable
function loadTable(dataURL, data_arguments) {
    $('#dataTableBooks').DataTable( {
        "serverSide": true,
        "searching": true,
        "processing": true,
        "ajax": {
            "url": dataURL,
            "data": function ( d ) {
                d.categories = $('#filterBooks').val();
            },
        },
        "order": [[ 1, "desc" ]],
        "pagingType": 'full_numbers',
        "dom": "<'row'<'col'tr>><'row'<'col-md-4'i><'col-md-4'p>>", // Setting DOM places
        //"dom": 'rtip', // Setting options: l - length changing, f - filtering, t - The table!, i - Table information, p - pagination, r - processing display element
    });


    // Hide default search box
    $("#dataTableBooks_search").addClass("hidden");

    // Set custom search box
    $("#searchBooks").on("input", function (e) {
        e.preventDefault();
        // Get selected categories
        var selected_categories = $('#filterBooks').val();

        if (selected_categories.length > 0){
            // Set message 'Can not search with category filter setted'
            $(this).val('');
            document.getElementById("searchBooks").placeholder = "Elimina los filtros por categoría para realizar una búsqueda";
        }else{
            // Set search
            $('#dataTableBooks').DataTable().search($(this).val()).draw();
        }
    });
}


// Filter books change event handler
$('#filterBooks').change( function () {
    // Get data URL
    var dataURL = document.getElementById("dataURL").value;

    // Get selected categories and able/disable search value
    var selected_categories = $('#filterBooks').val();
    search_box = document.getElementById("searchBooks")
    if (selected_categories.length == 0){
        // Clean message 'Can not search with category filter setted'
        search_box.placeholder = "Búsqueda";
    }else{
        // Set message 'Can not search with category filter setted'
        search_box.value = "";
        search_box.placeholder = "Elimina los filtros por categoría para realizar una búsqueda";
    }

    // Reload datatable
    $('#dataTableBooks').DataTable().search("").draw();
    //$('#dataTableBooks').DataTable().ajax.reload();
});


// Load document
$(document).ready(function () {

    // Get data URL
    var dataURL = document.getElementById("dataURL").value;

    // Custom filter select
    var multipleCancelButton = new Choices('#filterBooks', {
        removeItemButton: true
    });
    // Get selected categories
    var selected_categories = $('#filterBooks').val();

    // Call DataTable function
    loadTable(dataURL, selected_categories);
});
