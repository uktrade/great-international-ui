
$(document).ready(function() {

  (function() {
    var $container = $('#contact-section');
    var header = document.getElementsByClassName('great-sub-header')[0];

    $(window).on('scroll', function(e) {

      if (window.innerWidth <= 640) {
        // deactivate for mobile.
        return
      }

      var rect = header.getBoundingClientRect();

      if (rect.bottom <= 0) {
        $container.addClass('sticky');

      } else if (rect.bottom > 0) {
        $container.removeClass('sticky');
      }

    });
  })()

});
