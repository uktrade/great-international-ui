#!/bin/bash
# This script will render the project css files.

# put the path of library scss files we want to incluide
libraries="\
	--load-path node_modules/govuk_frontend_toolkit/stylesheets \
	--load-path node_modules/trade_elements/sass \
	--load-path enrolment/static/sass \
	--load-path core/static/core/sass \
	--load-path node_modules/govuk-elements-sass/public/sass \
"

# put the path of source code files we want to include, and where we want them
# to be exported to e.g., input.scss:output.css
input_output_map="\
	enrolment/static/sass/main.scss:enrolment/static/main.css \
	enrolment/static/sass/main-bidi.scss:enrolment/static/main-bidi.css \
	enrolment/static/sass/enrolment.scss:enrolment/static/enrolment.css \
	enrolment/static/sass/company-profile-details.scss:enrolment/static/company-profile-details.css \
	enrolment/static/sass/company-profile-details-bidi.scss:enrolment/static/company-profile-details-bidi.css \
	enrolment/static/sass/company-profile-form.scss:enrolment/static/company-profile-form.css \
	enrolment/static/sass/supplier-profile-details.scss:enrolment/static/supplier-profile-details.css \
	enrolment/static/sass/supplier-case-study-detail.scss:enrolment/static/supplier-case-study-detail.css \
	enrolment/static/sass/ie8fixes.scss:enrolment/static/ie8fixes.css \
	enrolment/static/sass/company-search_results.scss:enrolment/static/company-search_results.css \
	industry/static/industry/sass/industry.scss:industry/static/industry/industry.css \
	industry/static/industry/sass/industry-article.scss:industry/static/industry/industry-article.css \
	industry/static/industry/sass/industry-list.scss:industry/static/industry/industry-list.css \
	industry/static/industry/sass/contact.scss:industry/static/industry/contact.css \
	core/static/core/sass/landing-page.scss:core/static/core/landing-page.css \
"

prod_command="sass --sourcemap=none --style compressed"

rm enrolment/static/*.css
rm industry/static/industry/*.css
rm core/static/core/*.css

eval $prod_command$libraries$input_output_map
