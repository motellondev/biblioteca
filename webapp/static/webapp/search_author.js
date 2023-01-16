$(document).ready(function () {

         // On document ready, set cursos at the end of input textbox
         var search_author = document.getElementById("searchAuthor");
         if (search_author.value){
            var endtext = search_author.value.length;
            search_author.setSelectionRange(endtext, endtext)
         }
         search_author.focus();

         // On input, search authors
         $('#searchAuthor').on("input", function (e) {
            // Reload page
            var search_author = document.getElementById("searchAuthor").value;
            var authors_url = $(this).attr("data-url")
            if (search_author){
               document.location.href = authors_url + "?search_author=" + search_author;
            }else{
               document.location.href = authors_url;
            }
     });
});
