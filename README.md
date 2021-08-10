# great-international-ui
[Great International UI](https://www.directory.exportingisgreat.gov.uk/)

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

---

## Requirements

[Python 3.9.2](https://www.python.org/downloads/release/)

[redis](https://redis.io/)

## Local installation

    $ git clone https://github.com/uktrade/great-international-ui
    $ cd great-international-ui
    $ [create and activate virutal environment]
    $ make install_requirements

### Docker setup

To start the Great International UI in Docker instead, including the supporting 'directory-cms' service, you will first need to clone [directory-cms](https://github.com/uktrade/directory-cms) in the parent directory, and initialise and populate its secrets file:

```shell
$ cd ..
$ git clone git@github.com:uktrade/directory-cms.git
$ cd directory-cms
$ make secrets
# populate directory-cms/conf/env/secrets-do-not-commit with relevant environment variables
$ cd ../great-international-ui
```

You will also need a dump of the directory-cms database, which should be saved as `dockerise/postgres/directory_cms.sql`.

Create a secrets file for great-international-ui if you haven't already:
```shell
$ make secrets
```

Then start the docker containers -- it may take a while the first time, as the data is being seeded into the database and migrations are run:

```shell
$ docker-compose -f development.yml up
```

Once all containers have started, the site will be accessible at <http://international.trade.great:8012/international/>. You may need the following entries in your hosts file:

```
127.0.0.1   international.trade.great
127.0.0.1   cms.trade.great
```

You may need to rebuild the redis cache if you are getting 501 backend errors. If so, rebuild teh cache in the directory-cms container:
```shell
$ make manage rebuild_all_cache
```

## Development

### Configuration

Secrets such as API keys and environment specific configurations are placed in `conf/env/secrets-do-not-commit` - a file that is not added to version control. To create a template secrets file with dummy values run `make secrets`.

### Commands

| Command                       | Description |
| ----------------------------- | ------------|
| make clean                    | Delete pyc files |
| make pytest                   | Run all tests |
| make pytest test_foo.py       | Run all tests in file called test_foo.py |
| make pytest -- --last-failed` | Run the last tests to fail |
| make pytest -- -k foo         | Run the test called foo |
| make pytest -- <foo>          | Run arbitrary pytest command |
| make manage <foo>             | Run arbitrary management command |
| make webserver                | Run the development web server |
| make requirements             | Compile the requirements file |
| make install_requirements     | Installed the compile requirements file |
| make css                      | Compile scss to css |
| make secrets                  | Create your secret env var file |

## CSS development

If you're doing front-end development work you will need to be able to compile the SASS to CSS. For this you need:

### Requirements

[node](https://nodejs.org/en/download/)

[SASS](http://sass-lang.com/)

[gulp](https://gulpjs.com/)


    $ npm install yarn
    $ yarn install --production=false

## Translations

### Requirements

[GNU gettext](https://www.gnu.org/software/gettext/)

- brew install gettext
- which msgfmt should be able to find it

After adding new translatable strings, either with `{% trans 'Phrase to translate' %}` in templates or `_('Phrase to translate')` in python, add them to locale files with `django-admin makemessages`. Once translations are added to `.po` files run `django-admin compilemessages` to compile to them `.mo`. For more info see [Django documentation on translation](https://docs.djangoproject.com/en/2.2/topics/i18n/translation/).

## Session

Signed cookies are used as the session backend to avoid using a database. We therefore must avoid storing non-trivial data in the session, because the browser will be exposed to the data.

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
