$.fn.createBannerCookie = function (options) {
    var defaults = {
      buttonText: 'Got it!',
      message: 'Alpheios may not work with your browser. Please use Chrome, Firefox or Safari to access this site.',
      idBanner: 'browser-supported-banner',
      expiresDays: 10,
      cookieName: 'unsupportedAlreadyChecked'
    }

    var finalOptions = $.extend(defaults, options);

    var $parent = this;

    function getCookie(name) {
      var value = "; " + document.cookie;
      var parts = value.split("; " + name + "=");
      if (parts.length == 2) return parts.pop().split(";").shift();
    }
      
    function createBanner(opts) {
      console.error(opts.message);
      
      var $spanMessage = $('<span class="cc-message"></span').text(opts.message);
      var $spanGotItButton = $('<a class="cc-btn cc-dismiss" role="button"></a>').addClass('cc-btn cc-dismiss').text(opts.buttonText).wrap('<div class="cc-compliance"></div>');
      var $resBlock = $('<div id="' + opts.idBanner + '" role="dialog" class="cc-window cc-banner cc-type-info cc-theme-block cc-bottom "></div>')
                            .append($spanMessage)
                            .append($spanGotItButton);
      $parent.append($resBlock);
      
      $spanGotItButton.click(function (event) {
        var date = new Date(Date.now() + (86400e3 * opts.expiresDays)); //10 days
        date = date.toUTCString();
        document.cookie = opts.cookieName  + "=true; expires=" + date;
      
        $resBlock.hide()
      })
    }

    if (!getCookie('unsupportedAlreadyChecked')) {
        createBanner(finalOptions)
    }
};

function errorHandler(errorMessage) {
  var parser = new UAParser();
  var browserData = parser.getBrowser();
  var allowedBrowsers = ['Chrome', 'Firefox', 'Mobile Safari', 'Safari'];
  
  if (allowedBrowsers.indexOf(browserData.name) === -1) {
    $('body').createBannerCookie();
  } else {
    console.error(message)
  }

}


