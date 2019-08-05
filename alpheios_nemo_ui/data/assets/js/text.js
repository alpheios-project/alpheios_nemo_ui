$(document).ready(function(){
  $("[data-toggle=popover]").each(showNotes)
});

function showNotes() {
  
  $(this).addClass('popover-on-mobile-bigger')
  $(this).popover({
    html: true,
    content: function() {
      return $(this).next('.popover-content').html();
    },
    placement: 'bottom'
  });
}
