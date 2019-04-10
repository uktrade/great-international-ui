clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv,node_modules
PYTEST := pytest . -v --ignore=node_modules --cov=. --cov-config=.coveragerc --capture=no $(pytest_args)
COLLECT_STATIC := python manage.py collectstatic --noinput
COMPILE_TRANSLATIONS := python manage.py compilemessages

test:
	$(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST) && $(CODECOV)

DJANGO_WEBSERVER := \
	python manage.py collectstatic --noinput && \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DEBUG_SET_ENV_VARS := \
	export PORT=8012; \
	export SECRET_KEY=debug; \
	export DEBUG=true ;\
	export FEATURE_CONTACT_COMPANY_FORM_ENABLED=true; \
	export RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI; \
	export RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe; \
	export GOOGLE_TAG_MANAGER_ID=GTM-TC46J8K; \
	export GOOGLE_TAG_MANAGER_ENV=&gtm_auth=Ok4kd4Wf_NKgs4c5Z5lUFQ&gtm_preview=env-6&gtm_cookies_win=x; \
	export UTM_COOKIE_DOMAIN=.great; \
	export NOCAPTCHA=True; \
	export SESSION_COOKIE_SECURE=false; \
	export SECURE_HSTS_SECONDS=0 ;\
	export SECURE_SSL_REDIRECT=false; \
	export CMS_URL=http://cms.trade.great:8010; \
	export CMS_SIGNATURE_SECRET=debug; \
	export DEFAULT_FROM_EMAIL=debug@foo.com; \
	export IIGB_AGENT_EMAIL=test@example.com; \
	export EMAIL_HOST=foo.com; \
	export EMAIL_HOST_USER=debug; \
	export EMAIL_HOST_PASSWORD=debug; \
	export FEATURE_SEARCH_ENGINE_INDEXING_DISABLED=true; \
	export REDIS_URL=redis://localhost:6379; \
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export FEATURE_FORMS_API_ENABLED=true; \
	export HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS=test@example.com; \
	export HEALTH_CHECK_TOKEN=debug; \
	export FEATURE_EU_EXIT_BANNER_ENABLED=true; \
	export FEATURE_INTERNATIONAL_CONTACT_LINK_ENABLED=true; \
	export FEATURE_INTERNATIONAL_TARIFFS_ENABLED=true; \
	export FEATURE_INTERNATIONAL_TARIFFS_COUNTRY_SELECT_ENABLED=true; \
	export DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC=http://exred.trade.great:8007/; \
	export DIRECTORY_CONSTANTS_URL_GREAT_INTERNATIONAL=http://international.trade.great:8012/international/; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_BUYER=http://buyer.trade.great:8001; \
	export DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS=http://soo.trade.great:8008; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER=http://supplier.trade.great:8005; \
	export DIRECTORY_CONSTANTS_URL_INVEST=http://invest.trade.great:8012; \
	export DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON=http://sso.trade.great:8004; \
	export IP_RESTRICTOR_RESTRICT_UI=true

TEST_SET_ENV_VARS := \
	export DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export DIRECTORY_FORMS_API_API_KEY=debug; \
	export DIRECTORY_FORMS_API_SENDER_ID=debug; \
	export DEBUG=false

debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST) --cov-report=html

debug_manage:
	$(DEBUG_SET_ENV_VARS) && ./manage.py $(cmd)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

debug: test_requirements debug_test

compile_requirements:
	python3 -m piptools compile requirements.in
	python3 -m piptools compile requirements_test.in

translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py makemessages -a

compile_translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py compilemessages

compile_css:
	./node_modules/.bin/gulp sass

watch_css:
	./node_modules/.bin/gulp sass:watch

.PHONY: build clean test_requirements debug_webserver debug_test debug heroku_deploy_dev heroku_deploy_demo
