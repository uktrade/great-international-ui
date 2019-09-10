# Changelog

## Pre-release

### Implemented enhancements
- CMS-1754 - Change /eu-exit-news to /brexit and add redirects
- CI-400 - Added clickable maps to About Uk landing pages
- CI-366 - Added cta to invest home page
- CI-439 - Added redirects from invest to expand if `EXPAND_REDIRECT_ON` and if invest url 404s look up with expand url will try
- CI-460 - Updated capital invest contact and success pages and confirmation email and goes through GOV.UK Notify
- CI-405 - Added new IA candidate to nav header (behind a feature flag)
- CI-475 - About DIT services page uses featured description on featured cards instead so separate to teaser
- CI-476 - Allowed invest region pages to be linked to in maps in about uk pages
- CI-335 - Added breadcrumbs and labels to pages missing them
- CI-479 - Added video to Why choose UK Page

### Fixed bugs
- no ticket - change FAS search input broken id
- TT1752 - fix links on homepage
- no ticket - Fixed invest contact success going to expand
- no ticket - Fixed invest going to expand 

## [2019.08.29](https://github.com/uktrade/great-international-ui/releases/tag/2019.08.29)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.08.20...2019.08.29)

### Implemented enhancements
- GTRANSFORM-353-resize-searchform-select  - change FAS search to match soo and exops - needs design review
- CI-437 - Protect against clickjacking, XSS and content type sniffing attacks.
- CI-437 - Ensure that all cookies are secure and httponly.
- CI-431 - Added `AboutUkRegionListingPage` and `AboutUkRegionPage` which will replace `CapitalInvestRegionPage`

### Fixed bugs
- CMS-1826 - Fix engineering industry redirect
- CMS-1826 - Fix healthcare and life-sciences redirects.
- No ticket - Fix unloaded tag in template
- CMS-1825 - Fix breadcrumbs on ISD company contact page
- CMS-1827 - Fix FAS search term

## [2019.08.20](https://github.com/uktrade/great-international-ui/releases/tag/2019.08.20)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.08.08...2019.08.20)

### Implemented enhancements
- CMS-1815 - Update FAS contact redirect
- CMS-1816 - Add FAS industry contact pages
- CMS-1812 (Follow-up) - Fix homepage hero missing image
- CMS-1812 - Fix lazyload missing images, FAS cards, header lang select
- GTRANSFORM-349 - add external link attributes to FAS suppliers website
- CMS-1794 - Add child article cards to industry pages
- CMS-1639 - Added FAS subscribe form
- CMS-1641 - Added FAS search pages
- CI-276 - Added `CapitalInvestContactFormPage` and `CapitalInvestContactFormSuccessPage`
- CMS-1746 - Trade redirects
- CI-434 - Capital invest contact form edits
- CI-428 - Updated content for confirmation email from Capital Invest Contact form

### Fixed bugs
- CMS-1803, CMS-1804, CMS-1805, CMS-1806, CMS-1807, CMS-1808 - Various ISD and FAS bug fixes
- CMS-1800 - Try to fix ISD images not displaying, fix homepage hero styling
- CI-426 - Uses pdf document link for why choose uk page in ebook section
- CMS-1799 - ISD search form missing filters
- CMS-424 - Update version of directory-components to turn off lazyloading of images.


## [2019.08.08](https://github.com/uktrade/great-international-ui/releases/tag/2019.08.08)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.08.07...2019.08.08)

### Fixed bugs
- No ticket - Update HPO contact form invest redirect

## [2019.08.07](https://github.com/uktrade/great-international-ui/releases/tag/2019.08.07)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.07.25...2019.08.07)

### Fixed bugs:
- CMS-1772 - Add invest contact form pages
- No ticket - Fix duplication of constants in code
- CI-376 - Fixes About DIT How we help section issue on Internet Explorer
- CI-378 - Fixed guide landing page spacings
- CI-375 - Fix spacings on Why choose UK Page
- No ticket - Update styling on ebooks promotional section
- CI-396 - Fix case study section on sector page bug
- CI-419 - Commonised responsive behaviour for column-third
- CI-422 - Update Django to 1.2.23


### Implemented enhancements
- CMS-1596 - Add FAS homepage
- CMS-1774 - Add Invest region page, organise sass files
- No ticket - Namespace ISD contact page styling to fix pollution on other pages
- CMS-1734 - Added GA360 data to Perfect Fit views
- CI-363 - Add anchor tags to all headings in setup guide articles
- CMS-1640 - Move ISD pages to great international
- CI-383 - Create About DIT landing page
- CI-353 - Invest International Home page uses directory components card and wagtails focal area on images
- CMS-1745 - Implement invest redirects
- CI-420 - Added redirect from Capital Invest url ('/international/invest-capital') to one using tree based routing (/international/content/capital-invest')
- CI-321 - About UK landing page


## [2019.07.25](https://github.com/uktrade/great-international-ui/releases/tag/2019.07.25)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.07.08...2019.07.25)

### Fixed bugs:
- No ticket - Upgrade vulnerable django version to django 1.11.22
- No ticket - Updated `directory_components` to `20.3.1` and `directory_constants` to `18.1.2`
- CI-313 - Update JS dev dependencies to cover security vulnerabilities
- No ticket - Updated directory components requirements to fix pagination bug
- CI-301 - Opportunity cards and Article Cards now use the base template, making the whole card clickable etc.
- CI-352 - Fix image being squashed on guide landing page
- CI-365 - Change "Contact Us" section on services page in "About DIT" to markdown
- CI-368 - Add ebooks promotional section on "why choose the UK" page
- No ticket - Fixed Industries landing page extending tag being in the wrong order
- No ticket - Fix hero image on international home page
- No ticket - Fix hero images on topic and guide landing pages.

### Implemented enhancements
- CMS-1692 - Added HPO form pages from Invest
- CMS-1692 - Added HPO detail page from Invest and updated styling
- TT-1678 - Rename EU exit to Brexit
- CI-267 - Added cta text and link for sector page for related opportunities section
- CI-325 - CI projects shown on sector page are randomised
- CI-211 (& CI-252 & CI-268) - Created opportunity listing page filtering by sector, region and scale
- CI-303 - Update international header design.
- CI-324 - Made sub-sector page and opportunity listing page filters by sub sector
- CI-345 - Sass changes on spacing around details section on CapitalInvestOpportunityPage
- CI-322 - Add services page to "About DIT" section
- CI-342 - Promoted similar projects on `CapitalInvestOpportunityPage` are now randomised
- CI-344 - `Similar projects` title in `CapitalInvestOpportunityPage` is now hard coded
- CI-332 - Sass changes for mobile design for `CapitalInvestOpportunityListingPage`
- CI-323 - Add "Why choose the UK" page to "About the UK" section
- CI-372 - Updated trade CTA on sector pages to go to trade contact form
- CI-367 - Updated `CapitalInvestRegionPage` and added accordions js file



## [2019.07.08](https://github.com/uktrade/great-international-ui/releases/tag/2019.07.08)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.06.13...2019.07.08)

### Fixed bugs:
- No ticket - Changed `card-grid` to `flex-grid` on CI landing page, region and opp pages
- No ticket - Opportunity card changes to reflect new card component changes
- No ticket - Card with publish date (industry cards) updated to use image same as directory component

### Implemented enhancements
- CMS-1664 - Added invest homepage and upgraded directory-components
- CMS-1594 - Add perfect fit prospectus views to International UI
- CI-250 - Added an opportunity listing page template and put it behind a feature flag
- No ticket - Added 'Opportunity' Subheading for opportunity pages
- No ticket - Update breadcrumbs on opportunity pages.
- CI-271 - Add new URL for 'Invest Capital Homepage'
- CMS-1677 - Perfect fit prospectus cosmetic changes




## [2019.06.13](https://github.com/uktrade/great-international-ui/releases/tag/2019.06.13)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.05.16...2019.06.13)

### Fixed bugs
- No ticket - Fix healthchecks
- Upgrade cms client to prevent uncached pages being treated as cached
- no ticket - Fix typo on sector pages.
- Fix Article Listing Page failing to render
- Fix breadcrumbs displaying 'great.gov' instead of 'Great.gov' on some pages.
- CI-217: Update Django Version to fix security vulnerability.


### Implemented enhancements
- CMS-1677 - Refactored and tidied up Perfect Fit Prospectus. Upgraded directory-components to use new style breadcrumbs.
- TT-1432 - Added link to Investment Support Directory on UK setup guide page
- CI-108 - Added back in sending data to GA 360, and updated the format to the new spec.
- CI-104 - Added capital invest landing, region, sector and opportunity pages. All new pages behind feature flag to return 404 until ready to release.
- CI-144 - Updated capital invest landing page to match more recent invision designs
- CI-148 - Updated capital invest region, sector and opportunity pages to match more recent invision designs
- CI-151 - Added blank alt text to images on capital invest pages for accessibility
- CI-152 - Changed `next steps` sections to be `contact` section on capital invest pages
- CI-153 - Removed the card with pdf button on Capital Invest Landing page, region cards are now only displayed with markdown text
- CI-154 - Changed hard coded text in guide landing page to come from cms
- CI-146 - Changed English copy that was hard coded text in sector page
- CMS-1465 - Tidied context modifier implementation and improved test (tree-based-routing related)
- CI-145 - Use invest logo in header
- CMS-1577 - Update content on Brexit CTA buttons
- no-ticket - Make the 'home' breadcrumb label translatable.
- CI-165 - Redesign of capital invest pages - removed regional sector pages, uses normal industry page
- CI-200 - Decoupled capital invest feature flags so landing page, region and opportunity pages can all be released separately
- CI-196 - Similar opportunity cards on opportunity page use same card as on sector page
- CI-250 - Gave opportunity listing page a template and put it behind a feature flag


## [2019.05.16](https://github.com/uktrade/great-international-ui/releases/tag/2019.05.16)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.05.13_2...2019.05.16)

### Implemented enhancements:

- CI-108 - Temporarily turn off additional GA tagging.
- CMS-1480 - Add translations to po files and templates

### Fixed bugs

- CMS-1514 Fix case studies disappearing on mobile
- CMS-1510 - Remove prefix_path shim to fix related article urls
- Upgrade `directory-components` to version `13.0.0` to fix CMS-1254 and CMS-1460
- CMS-1543: Fix link to invest contact us form on sector pages.
- No ticket - Fix links to industries landing page and how to setup page on homepage
- No ticket - Fix invest contact link on industry pages

## [2019.05.13_2](https://github.com/uktrade/great-international-ui/releases/tag/2019.05.13_2)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.05.13_1...2019.05.13_2)

## Fixed bugs

- CMS-1472 - Follow-up to contact form ticket: fixed incorrect margin on breadcrumbs on form pages, fix incorrect page title

## [2019.05.13_1](https://github.com/uktrade/great-international-ui/releases/tag/2019.05.13_1)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.05.13...2019.05.13_1)

### Fixed bugs

- CMS-1472 - Follow-up to contact form ticket: fixed 500 error on contact page due to wrong url in template


## [2019.05.13](https://github.com/uktrade/great-international-ui/releases/tag/2019.05.13)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.04.26...2019.05.13)


### Implemented enhancements:

- CMS-1472 - Implement contact us form
- CMS-1465 - Implement tree based routing

### Fixed bugs:

- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)
- CMS-1395 - Fix language cookie name and domain to be the same across all our services.
- CMS-1241 - Accessibility fixes - img alt attributes and breadcrumbs
- CMS-1465 - Follow-up to tree-based routing ticket: fixed breadcrumbs home link not displaying

## [2019.04.26](https://github.com/uktrade/great-international-ui/releases/tag/2019.04.26)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.04.24...2019.04.26)

### Implemented enhancements:

- CMS-1400 - Added new url/view to support tree-based routing
- CMS-775 - Added alternate language url metadata to base template to improve SEO
- CMS-1386 - Updated homepage design
- CMS-1247 - Fix Brexit contact form URLs in CTAs on "How to do business in the UK" and "How to set up in the UK" pages
- CMS-1384 - Fix the invest CTA on sector pages to link directly to invest's contact form

## [2019.04.24](https://github.com/uktrade/great-international-ui/releases/tag/2019.04.24)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.04.11...2019.04.24)

### Implemented enhancements:

- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [API client][directory-api-client], [Forms client][directory-forms-api-client] and because [CMS client][directory-cms-client] upgrade results in [Client core][directory-client-core] being upgraded.
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.

### Fixed bugs:

- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)


[directory-api-client]: https://github.com/uktrade/directory-api-client
[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
[directory-components]: https://github.com/uktrade/directory-components
[directory-constants]: https://github.com/uktrade/directory-constants
