# Changelog

## Pre-release


## [2019.05.13_1](https://github.com/uktrade/great-international-ui/releases/tag/2019.05.13_1)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.05.13...2019.05.13_1)

### Fixed bugs

- [CMS-1472](https://uktrade.atlassian.net/browse/CMS-1472) Follow-up to contact form ticket: fixed 500 error on contact page due to wrong url in template


## [2019.05.13](https://github.com/uktrade/great-international-ui/releases/tag/2019.05.13)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.04.26...2019.05.13)


### Implemented enhancements:

- [CMS-1472](https://uktrade.atlassian.net/browse/CMS-1472) Implement contact us form
- [CMS-1465](https://uktrade.atlassian.net/browse/CMS-1465) Implement tree based routing

### Fixed bugs:

- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)
- [CMS-1395](https://uktrade.atlassian.net/browse/CMS-1395) Fix language cookie name and domain to be the same across all our services.
- [CMS-1241](https://uktrade.atlassian.net/browse/CMS-1241) Accessibility fixes - img alt attributes and breadcrumbs
- [CMS-1465](https://uktrade.atlassian.net/browse/CMS-1465) Follow-up to tree-based routing ticket: fixed breadcrumbs home link not displaying

## [2019.04.26](https://github.com/uktrade/great-international-ui/releases/tag/2019.04.26)
[Full Changelog](https://github.com/uktrade/great-international-ui/compare/2019.04.24...2019.04.26)

### Implemented enhancements:

- [CMS-1400](https://uktrade.atlassian.net/browse/CMS-1400) Added new url/view to support tree-based routing
- [CMS-775](https://uktrade.atlassian.net/browse/CMS-775) Added alternate language url metadata to base template to improve SEO
- [CMS-1386](https://uktrade.atlassian.net/browse/CMS-1386) Updated homepage design
- [CMS-1247](https://uktrade.atlassian.net/browse/CMS-1247) Fix EU exit contact form URLs in CTAs on "How to do business in the UK" and "How to set up in the UK" pages
- [CMS-1384](https://uktrade.atlassian.net/browse/CMS-1384) Fix the invest CTA on sector pages to link directly to invest's contact form

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
