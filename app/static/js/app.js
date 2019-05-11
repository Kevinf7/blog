//copy text to clipboard for the manage image page
$(".clipboard").click(function() {
    try {
        //get id of element that was clicked
        $id = $(this).attr('id');
        //select text inside element
        $txt = $("#filepath-"+$id).text();
        //we need to create a dummy input variable and select it
        $dummy = $('<input>').val($txt).appendTo('body').select();
        //we then issue the copy command which is like a CTRL-C
        document.execCommand("copy");
    } catch(err) {
        console.log(err)
    }
})

//so it doesnt jump to the top when you click the clipboard
$('a.cliplink').click(function(e) {
    // Cancel the default action
    e.preventDefault();
});

// For tooltip
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})
