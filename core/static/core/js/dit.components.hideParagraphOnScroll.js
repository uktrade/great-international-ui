
$(document).ready(function() {

  (function() {
    var $container = $('#contact-section');
    var $paragraph = $container.find('p');
    var hero = document.getElementById('hero');

    $(window).on('scroll', function(e) {

      if (window.innerWidth <= 640) {
        // deactivate for mobile.
        return
      }

      var rect = hero.getBoundingClientRect();

      if (rect.bottom <= 0) {
        $container.addClass('sticky');

      } else if (rect.bottom > 30) {
        $container.removeClass('sticky');
      }

    });
  })()

});
