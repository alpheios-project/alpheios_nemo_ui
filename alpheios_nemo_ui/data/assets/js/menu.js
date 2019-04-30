'use strict';

function fixedNavbar() {
  let scrollTopCheck = 0
  if ($('.navlogin:visible').length > 0) {
    scrollTopCheck = $('.navlogin:first').height();
  }

  if ($(window).scrollTop() > scrollTopCheck) {
      $('.article-wrap').addClass('fixed-navbar');
  } else {
     $('.article-wrap').removeClass('fixed-navbar');
  }
}

function openSideMenu() {
  if (!Boolean($('#dropdownMenuButton').prop('aria-expanded'))) {
    if ($('.modal-backdrop').length === 0) {
      $('body').append($('<div class="modal-backdrop fade show"></div>'));
    } else {
      $('.modal-backdrop').addClass('show');
    }
    $('#maindropdown').addClass('show');
  }
}

function closeSideMenu() {
  $('#maindropdown').removeClass('show');
  $('.modal-backdrop').removeClass('show');
}

$(document).ready(function($) {
    var texts_authors = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: $("#fullsearch").attr("data-target")
    });

    $("#fullsearch").autocomplete(
      {
        minLength: 3,
        highlight: true,
        hint: false
      },
      {
        name: 'collections',
        source: function (query, callback) {
              return texts_authors.search(
                  query,
                  function(datum) { callback(datum); },
                  function (datum) { callback([]); }
              );
        },
        displayKey: function(suggestion) { return suggestion.title; },
        templates: {
            empty: '<div class="empty-message">'+$("#fullsearch").attr("data-noresult")+'</div>',
            suggestion: function(s) {
                return '<div><strong><a href="'+s.uri+'">'+s.title+'</a></strong><div>'+s.parents+'</small></div></div>';
            }
        }
      }
    ).on('autocomplete:selected', function(event, suggestion, dataset) {
       event.preventDefault();
       window.location = suggestion.uri;
    });

    $('#dropdownMenuButton').click(function(event){
      openSideMenu();
    });
    $('#dropdownMenuButtonClose').click(function(event){
      closeSideMenu();
    });
    $('.dropdown-menu').click(function(event){
      closeSideMenu();
    });
    $( "body" ).on( "click", ".modal-backdrop", function() {
      closeSideMenu();
    });

    $(window).bind('scroll', function() {
      fixedNavbar();
    });
});