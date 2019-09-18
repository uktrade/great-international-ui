# great-international-ui
[Great International UI](https://www.directory.exportingisgreat.gov.uk/)

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

---

## Requirements

[Python 3.6](https://www.python.org/downloads/release/python-366/)

[redis](https://redis.io/)

## Local installation

    $ git clone https://github.com/uktrade/great-international-ui
    $ cd great-international-ui
    $ [create and activate virutal environment]
    $ make install_requirements

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

[circle-ci-image]: https://circleci.com/gh/uktrade/great-international-ui/tree/develop.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/great-international/tree/develop

[codecov-image]: https://codecov.io/gh/uktrade/great-international-ui/branch/develop/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/great-international-ui

[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg
[calver]: https://calver.org
