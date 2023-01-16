$(document).ready(function setFilters() {

         // On document ready, set cursos at the end of input textbox
         var search_category = document.getElementById("searchCategory");
         if (search_category.value){
            var endtext = search_category.value.length;
            search_category.setSelectionRange(endtext, endtext)
         }
         search_category.focus();

         // On input, search authors
         $('#searchCategory').on("input", function (e) {
            // Reload page
            var search_category = document.getElementById("searchCategory").value;
            var categories_url = $(this).attr("data-url")
            if (search_category){;
               document.location.href = categories_url + "?search_category=" + search_category;
               $(this).focus(); 
            }else{
               document.location.href = categories_url;
               $(this).focus(); 
            }

     });
});

