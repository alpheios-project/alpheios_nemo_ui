function showOnlyBook ($theBookTitle, currentBook) {
    $('.browse-header > div').hide();
    $('.browse-header .' + currentBook).show();
    $('.browse-list-item').hide()
    $theBookTitle.next().show();
}

function showFirstLevel () {
    $('.browse-header > div').hide();
    $('.browse-header .browse-level-1').show();

    $('.reference-browse-cards .reference-browse-cards').hide()
    $('.browse-list-item').show()
}

$(document).ready(function() {
    if ( $('#reference-article').length > 0 ) {
        $('.browse-list-item .list-item-link').click(function(event){
            event.preventDefault();
            var currentBook = $(this).data('book-title');
            showOnlyBook($(this).parent(), currentBook);
        })
        $('.browse-header .browse-level-2 a').click(function(event){
            event.preventDefault();
            showFirstLevel();
        })
    }
})