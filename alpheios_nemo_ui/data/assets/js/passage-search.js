/**
 * this function does an ajax prefetch of a requested passage identifier
 * for the jump_passage input form which contains an input box for the user
 * to enter the passage they want to go to. Preloading all of the possible
 * passage identifiers is too performance intensive so we can't validate the
 * user's input before loading the new page other than to try to load the passage
 * itself. If the passage is found, we can go ahead and submit the form to load
 * the requested page
 */
function tryPassage(e) {
  e.preventDefault();
  const el = document.querySelector("#find_subreference")
  let ref = el.value
  if (!ref || !ref.match(/^\d+(\.\d*)*$/)) {
    console.warn('It is not a valid passage format! Try to use numbers and points.')
    showError(`It is not a valid passage format - ${ref}! Try to use numbers and points.`);
    return false
  }
  let findUrl = el.dataset.route.replace('REPLACE_REF',ref)

  let $iconContainer = $(el).parent();
  $iconContainer.addClass('loader-active');
  $.getJSON(findUrl)
    .done(function(data) {
      let form = document.querySelector("#jump_passage")
      let action = form.getAttribute('action')
      form.setAttribute('action',action.replace('REPLACE_REF',ref))
      form.submit()
    })
    .fail(function(error) {
      console.warn(`Invalid passage ${ref}`)
      showError(`Invalid passage ${ref}`)
    })
    .always(function() {
      $iconContainer.removeClass('loader-active');
    });
  return false
}

function showError(message) {
  $('#find-passage-popup-body-text').text(message)
  $('#findPassagePopup').modal()
}

$(document).ready(function() {
    /**
     * intercept the submit of the jump passage form to do a prefetch
     * of the requested passage identifier to be sure it exists before
     * we actually submit the page
     */
    $("#jump_passage").submit(tryPassage)
});