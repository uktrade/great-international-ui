
$(document).ready(function() {

  (function() {
    var container = document.getElementById('contact-section');
    var propositionOne = document.getElementById('proposition-one');
    var paragraph = container.getElementsByTagName('p')[0];
    var hero = document.getElementById('hero');
    window.addEventListener('scroll', function(e) {
      if (window.innerWidth <= 375) {
        // deactivate for mobile.
        paragraph.style.display = 'block';
        return
      }
      var rect = hero.getBoundingClientRect();
      if (paragraph.style.display != 'none' && rect.bottom <= -20) {
        propositionOne.style['margin-top'] = container.offsetHeight + 'px';
        paragraph.style.display = 'none';
        container.style.position = 'fixed';
      } else if (paragraph.style.display != 'block' && rect.bottom > 30) {
        paragraph.style.display = 'block';
        container.style.position = 'relative';
        propositionOne.style['margin-top'] = 0;
      }
    });
  })()

});
