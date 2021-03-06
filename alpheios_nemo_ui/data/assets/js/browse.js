function showOnlyBook (currentBook, $parentThis) {
    // for now, since we don't have a meaningful grouping of passages we want to just go to
    // the first reference rather than letting the user choose from a somewhat arbitrary
    // list of passage chunks
    let singleRefs = $('.reference-browse-cards .'+currentBook).children('.single-refs')
    if (singleRefs.length > 0) {
      $('a',singleRefs)[0].click()
    } else {
      $('.browse-header > div').hide();
      $('.browse-header .' + currentBook).show();
      $parentThis.children('.browse-list-item').hide()
      $parentThis.parent().children('.browse-list-item').hide()
      $('.reference-browse-cards .' + currentBook).show();
    }
}

function showPrevLevel ($browseLevel) {
    var browseClasses = $browseLevel.attr('class').split(' ');
    var levelNumber = jQuery.grep(browseClasses, function( a ) {
        return a.indexOf('browse-level') === 0 && a!=='browse-level';
    })[0].split('-')[2];
    levelNumber = parseInt(levelNumber);

    if (levelNumber === 1) {
        return;
    }

    $('.browse-header > div').hide();
    var addClass = '';

    if (levelNumber > 2) {
        var levelClass = jQuery.grep(browseClasses, function( a ) {
            return a.indexOf('browse-level') !== 0 ;
        })[0];

        var levelClassArr = levelClass.split('-');

        if (levelClassArr.length > levelNumber) {
            addClass = '.' + levelClassArr[levelClassArr.length-levelNumber-1] + '-' + levelClassArr[levelClassArr.length-levelNumber];
        }
    }

    $('.browse-header .browse-level-' + (levelNumber-1) + addClass).show();
    $('.reference-browse-cards '.repeat(levelNumber)).hide();
    $('.reference-browse-cards '.repeat(levelNumber-1) + ' > .browse-list-item').show();

}

$(document).ready(function() {
    if ( $('#reference-article').length > 0 ) {
        $('.browse-list-item .list-item-link').not('.list-item-link-direct').click(function(event){
            event.preventDefault();
            var currentBook = $(this).data('book-title');
            showOnlyBook(currentBook, $(this).parent());
        })

        $('.browse-header .book-level-prev').click(function(event){
            event.preventDefault();
            showPrevLevel($(this).closest('.browse-level'));
        })

    }
})