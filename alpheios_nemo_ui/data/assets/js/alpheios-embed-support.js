/**
 * Executes and additional Nemo UI specific initialization after an Embedded object has been activated.
 *
 * @param {object} embedded - An activated instance of the `Embedded` class from the embedded library.
 */
let embedPostActivation = function (embedded) {
  if (embedded.platform.isMobile) {
    let lookupPanelIsVisible = false
    let toolsPanelIsVisible = false
    let lookupEl = document.querySelector('#alph-lookup-ctrl')
    if (lookupEl) {
      lookupEl.addEventListener('click', function () {
        if (toolsPanelIsVisible) {
          embedded.closeActionPanel()
          toolsPanelIsVisible = false
        }
        if (!lookupPanelIsVisible) {
          embedded.openActionPanelLookup()
          lookupPanelIsVisible = true
        } else {
          embedded.closeActionPanel()
          lookupPanelIsVisible = false
        }
      }, { passive: true })
    }
    let toolsEl = document.querySelector('#alph-tools-ctrl')
    if (toolsEl) {
      toolsEl.addEventListener('click', function () {
        if (lookupPanelIsVisible) {
          embedded.closeActionPanel()
          lookupPanelIsVisible = false
        }
        if (!toolsPanelIsVisible) {
          embedded.openActionPanelToolbar()
          toolsPanelIsVisible = true
        } else {
          embedded.closeActionPanel()
          toolsPanelIsVisible = false
        }
      }, { passive: true })
    }
  }
}

export { embedPostActivation }