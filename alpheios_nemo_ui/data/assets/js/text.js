$(document).ready(function(){
  $("[data-toggle=popover]").each(showNotes)
});

function showNotes() {
  $(this).popover({
    html: true,
    content: function() {
      return $(this).next('.popover-content').html();
    }
  });
}
