// Header code
//
// Requires
// jQuery
// dit.js
// dit.components.js
//#" + id);


$(document).ready(function() {
  $('.accordion-content').each(function() {
      var $this = $(this);
      new dit.classes.Expander($this, {
        hover: false,
        blur: false,
        wrap: false,
        $control: $this.parent().find('a.accordion-expander')
      });
    });
});
