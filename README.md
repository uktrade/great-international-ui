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
    $ make

## Development

### Configuration

Secrets such as API keys and environment specific configurations are placed in `conf/.env` - a file that is not added to version control. You will need to create that file locally in order for the project to run.

Here are the env vars to get you going:

```
DIRECTORY_FORMS_API_API_KEY
DIRECTORY_FORMS_API_SENDER_ID
DIRECTORY_FORMS_API_BASE_URL
```

## Running the webserver

### Setup debug environment

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## CSS development

If you're doing front-end development work you will need to be able to compile the SASS to CSS. For this you need:

### Requirements

[node](https://nodejs.org/en/download/)

[SASS](http://sass-lang.com/)

[gulp](https://gulpjs.com/)


    $ npm install yarn
    $ yarn install --production=false


### Update CSS under version control

	$ make compile_css

### Rebuild the CSS files when the scss file changes

	$ make watch_css

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

[circle-ci-image]: https://circleci.com/gh/uktrade/great-international-ui/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/great-international/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/great-international-ui/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/great-international-ui

[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg
[calver]: https://calver.org
