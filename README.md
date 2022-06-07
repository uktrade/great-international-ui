# great-international-ui

[Great International UI](https://www.directory.exportingisgreat.gov.uk/)

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

---

## Requirements

- [Docker](https://www.docker.com/get-started/)

If running 'manually', you will also need:

- [Python 3.9.7](https://www.python.org/downloads/release/)
- [Postgres](https://www.postgresql.org/)
- [redis](https://redis.io/)

## Local setup

To run `great-international-ui` locally, you will first need to clone the supporting services in the parent directory:

- [directory-cms](https://github.com/uktrade/directory-cms)
- [directory-api](https://github.com/uktrade/directory-api) :

To initialise the secrets files, run the following for `great-international-ui`, `directory-cms` and `directory-api` in
their respective root directory:

```shell
$ make secrets
```

Add the following entries to your hosts file:

```
127.0.0.1   international.trade.great
127.0.0.1   cms.trade.great
```

You can then start `great-international-ui` and the associated services using Docker or manually.

### Starting using Docker

You will need a dump of the `directory-cms` database, which should be saved
as `dockerise/postgres/data/directory_cms.sql` (you can use the CloudFoundry command line tool to download a SQL dump of
the dev database).

Then start the docker containers -- it may take a while the first time, as the data is being seeded into the database
and migrations are run:

```shell
$ docker-compose -f development.yml up
```

Once all containers have started, the site will be accessible at <http://international.trade.great:8012/international/>.

You may need to rebuild the redis cache if you are getting `5XX` backend errors. If so, rebuild the cache in the
directory-cms container:

```shell
$ make manage rebuild_all_cache
```

### Starting 'manually'

To run Great International UI locally, you will need to create and activate virtual environments
in `great-international-ui` and all supporting services as per their READMEs.

You will also need:

- Postgres running locally
- Redis running locally

Then, start each service individually using:

```shell
$ make webserver
```

The site should now be accessible at <http://international.trade.great:8012/international/>.

### Troubleshooting

#### Rebuild `directory-cms` cache

If the server is running, but you are getting `5XX` errors from `directory-cms`, try to rebuild the cache
in `directory-cms` (in the container if using Docker):

```shell
$ make manage rebuild_all_cache
```

#### Enabling 'Find a supplier'

> If you are running `great-international-ui` manually, you will first need to run a local OpenSearch container (this is
> run automatically if you start using Docker):
>
> ```shell
> $ docker run -p 9200:9200 -e "discovery.type=single-node" -e "plugins.security.disabled=true" opensearchproject/opensearch:1.2.2
> ```

You will then need to migrate the elastic search indices, then create some test search data in the database. To do so,
run the following commands in `directory-api` (in the container if using Docker):

```shell
$ make manage elasticsearch_migrate
$ make manage create_test_search_data
```

The search should now work at <http://international.trade.great:8012/international/trade/>.

## Development

### Useful commands

| Command                       | Description                              |
|-------------------------------|------------------------------------------|
| make clean                    | Delete pyc files                         |
| make pytest                   | Run all tests                            |
| make pytest test_foo.py       | Run all tests in file called test_foo.py |
| make pytest -- --last-failed` | Run the last tests to fail               |
| make pytest -- -k foo         | Run the test called foo                  |
| make pytest -- <foo>          | Run arbitrary pytest command             |
| make manage <foo>             | Run arbitrary management command         |
| make webserver                | Run the development web server           |
| make requirements             | Compile the requirements file            |
| make install_requirements     | Installed the compile requirements file  |
| make secrets                  | Create your secret env var file          |

## Front-end development

The CSS and JS for Great International UI are compiled using Webpack.

First, install dependencies:

```shell
$ npm install
```

Then build and copy all the relevant assets:

```shell
$ npm run build
```

Rebuild CSS and JS on file changes:

```shell
$ npm run watch
```

### Atlas styles, scripts and assets

The Atlas styles are found in `core/sass/atlas` and provide styles to all the newer pages of the site. The older pages
are styled mainly from `core/sass/main.scss`, which does include the header and footer Atlas styles as these are now
included on all pages.

The Atlas JS scripts are found in `core/js/src`, come with tests, and are compiled into individual files
in `core/static/core/js`. This destination directory also contains scripts used on the older pages of the site. These
typically do not have tests, and are not compiled or minified.

Atlas assets are found in `core/assets` and are optimised and copied to `core/static/core` using Webpack. Older assets
reside directly in this destination directory.

## Translations

*NOTE: GIUI no longer provides translations. The following is for reference only.*

### Requirements

[GNU gettext](https://www.gnu.org/software/gettext/)

- brew install gettext
- which msgfmt should be able to find it

After adding new translatable strings, either with `{% trans 'Phrase to translate' %}` in templates
or `_('Phrase to translate')` in python, add them to locale files with `django-admin makemessages`. Once translations
are added to `.po` files run `django-admin compilemessages` to compile to them `.mo`. For more info
see [Django documentation on translation](https://docs.djangoproject.com/en/2.2/topics/i18n/translation/).

## Session

Signed cookies are used as the session backend to avoid using a database. We therefore must avoid storing non-trivial
data in the session, because the browser will be exposed to the data.

## Cookies

To be able to test cookies locally add the following to your `/etc/hosts`:

```
127.0.0.1       international.trade.great
```

Then run the server and visit `international.trade.great:8012`


[code-climate-image]: https://codeclimate.com/github/uktrade/great-international-ui/badges/issue_count.svg

[code-climate]: https://codeclimate.com/github/uktrade/great-international-ui

[circle-ci-image]: https://circleci.com/gh/uktrade/great-international-ui/tree/develop.svg?style=shield

[circle-ci]: https://circleci.com/gh/uktrade/great-international/tree/develop

[codecov-image]: https://codecov.io/gh/uktrade/great-international-ui/branch/develop/graph/badge.svg

[codecov]: https://codecov.io/gh/uktrade/great-international-ui

[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg

[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg

[calver]: https://calver.org
