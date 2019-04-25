# Changelog

## Pre-release

### Implemented enhancements:

- [CMS-775](https://uktrade.atlassian.net/browse/CMS-775) Added alternate language url metadata to base template to improve SEO

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
