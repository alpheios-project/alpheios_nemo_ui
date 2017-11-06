'use strict';

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
});