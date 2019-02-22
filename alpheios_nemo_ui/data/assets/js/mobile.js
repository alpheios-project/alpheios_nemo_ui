$(document).ready(function() {

  let hammertime = new Hammer(document.querySelector('.entry'))

  hammertime.on('swipeleft', navNext);
  hammertime.on('swiperight', navPrev);
});

function navNext(event) {
  let next = $('.next').attr('href');
  if (next) {
    let nextUrl = document.location.href.replace(/\/text.*$/,next)
    document.location = nextUrl;

  }
}

function navPrev(event) {
  let prev = $('.prev').attr('href');
  if (prev) {
    let prevUrl = document.location.href.replace(/\/text.*$/,prev)
    document.location = prevUrl;
  }
}

