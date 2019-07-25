

dit.tariffsCountrySelector = (new function() {
    var COUNTRY_SELECT = '#js-tariffs-country-select';
    var FLAG = '#tariffs-flag-container';

    this.init = function() {
        $(COUNTRY_SELECT).on('change', function() {
            var country = '';

            $(COUNTRY_SELECT + " option:selected").each(function() {
                country = $(this).attr('value');
            });

            $(FLAG).attr('class', 'flag-icon flag-icon-' + country.toLowerCase())
        });
    }
});

$(document).ready(function() {
  dit.tariffsCountrySelector.init();
});
