function showOnlyBook (currentBook, $parentThis) {
    $('.browse-header > div').hide();
    $('.browse-header .' + currentBook).show();
    $parentThis.children('.reference-browse-cards').hide();
    $parentThis.parent().children('.browse-list-item').hide()
    
    $('.reference-browse-cards .' + currentBook).show();
}

function showPrevLevel ($browseLevel) {
    var browseClasses = $browseLevel.attr('class').split(' ');
    var levelNumber = jQuery.grep(browseClasses, function( a ) {
        return a.indexOf('browse-level') === 0 && a!=='browse-level';
    })[0].split('-')[2];

    $('.browse-header > div').hide();

    if ($browseLevel.hasClass('browse-level-2')) {
        $('.browse-header .browse-level-' + (levelNumber - 1)).show();
        $('.reference-browse-cards '.repeat(levelNumber)).hide();
        $('.reference-browse-cards '.repeat(levelNumber-1) + ' > .browse-list-item').show();
    }
    if ($browseLevel.hasClass('browse-level-3')) {
        var levelClass = jQuery.grep(browseClasses, function( a ) {
            return a.indexOf('browse-level') !== 0 ;
        })[0];
        
        var levelClassArr = levelClass.split('-');
        var addClass = '';
        if (levelClassArr.length > levelNumber) {
            addClass = '.' + levelClassArr[levelClassArr.length-levelNumber-1] + '-' + levelClassArr[levelClassArr.length-levelNumber];
        } 
        $('.browse-header .browse-level-' + (levelNumber-1) + addClass).show();
        $('.reference-browse-cards '.repeat(levelNumber)).hide();
        $('.reference-browse-cards '.repeat(levelNumber-1) + ' > .browse-list-item').show();
    }
}

$(document).ready(function() {
    if ( $('#reference-article').length > 0 ) {
        $('.browse-list-item .list-item-link').click(function(event){
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