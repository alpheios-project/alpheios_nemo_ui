function preloadNext() {
    let next = $('.next').attr('href');
    if (next) {
        console.log(`preload ${next}`);
    }
}

$(document).ready(function() {
    preloadNext();
});