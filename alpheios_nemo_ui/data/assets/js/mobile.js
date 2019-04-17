let queue = [];
$(document).ready(function() {
  window.addEventListener('scroll', function(e) {
    let lastPassage = $('.passage-end').last();
    if (lastPassage.length > 0 && isOnScreen(lastPassage)) {
      showNext();
    }
  });
  preloadNext();
});

function preloadNext() {
  let next = $('.next').attr('href');
  if (next) {
    console.log(`preload ${next}`)
    let nextUrl = `${document.location.href.replace(document.location.pathname,next)}/json`
    $.getJSON(nextUrl,function(data) {
      queue.push(data)
    })
  }
}

function updateNext(next) {
  if (next) {
    let nextLink = $('.next');
    let oldPassage = nextLink.attr('data-next');
    let nextUrl = nextLink.attr('href').replace(oldPassage,next)
    nextLink.attr('href',nextUrl);
    nextLink.attr('data-next',next)
    nextLink.removeClass('d-none')
  } else {
    $('.next').addClass('d-none')
  }
}

function updatePrev(prev) {
  if (prev) {
    let prevLink = $('.prev');
    let oldPassage = prevLink.attr('data-prev');
    let prevUrl = prevLink.attr('href').replace(oldPassage,prev);
    prevLink.attr('href',prevUrl);
    prevLink.attr('data-prev',prev);
    prevLink.removeClass('d-none')
  } else {
    $('.prev').addClass('d-none');
  }
}

function showNext() {
  let data = queue.pop();
  if (data) {
    let oldref = $('.subreference').text().split(/-/);
    let oldstart= oldref[0]
    let newref = data.subreference.split(/-/);
    let newend
    // the subreference of the new passages might be a single passage
    if (newref.length == 1) {
        newend = newref[0]
    } else {
        newend = newref[1]
    }
    $('.subreference-all').text(`${oldstart}-${newend}`)
    $('.entry-content').append(`<div class="subreference text-center">${data.subreference}</div>${data.text_passage}`);
    updateNext(data.next);
    updatePrev(data.prev);
    preloadNext();
  }
}

function isOnScreen(elem) {
	// if the element doesn't exist, abort
	if( elem.length == 0 ) {
		return;
	}
	var $window = jQuery(window);
	var viewport_top = $window.scrollTop();
	var viewport_height = window.innerHeight;
	var viewport_bottom = viewport_top + viewport_height;
	var $elem = jQuery(elem);
	var top = $elem.offset().top;
	var height = $elem.height();
	var bottom = top + height;

	return (bottom <= viewport_bottom && top >= viewport_top);
}
