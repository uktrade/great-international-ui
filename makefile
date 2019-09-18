clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv,node_modules --max-line-length=120
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
	export CSRF_COOKIE_SECURE=False; \
	export SESSION_COOKIE_SECURE=false; \
	export SECURE_HSTS_SECONDS=0 ;\
	export SECURE_SSL_REDIRECT=false; \
	export CMS_URL=http://cms.trade.great:8010; \
	export CMS_SIGNATURE_SECRET=debug; \
	export DEFAULT_FROM_EMAIL=jessica.gilbert@digital.trade.gov.uk; \
	export IIGB_AGENT_EMAIL=j.jgilbert@yahoo.com; \
	export CAPITAL_INVEST_CONTACT_EMAIL=jessica.gilbert@digital.trade.gov.uk; \
	export EMAIL_HOST=digital.trade.gov.uk; \
	export EMAIL_HOST_USER=debug; \
	export EMAIL_HOST_PASSWORD=debug; \
	export FEATURE_SEARCH_ENGINE_INDEXING_DISABLED=true; \
	export REDIS_URL=redis://localhost:6379; \
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export DIRECTORY_FORMS_API_BASE_URL=http://api.trade.great:8000; \
	export FEATURE_FORMS_API_ENABLED=true; \
	export HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS=test@example.com; \
	export HEALTH_CHECK_TOKEN=debug; \
	export FEATURE_EU_EXIT_BANNER_ENABLED=true; \
	export FEATURE_INTERNATIONAL_CONTACT_LINK_ENABLED=true; \
	export FEATURE_INTERNATIONAL_TARIFFS_ENABLED=true; \
	export FEATURE_INTERNATIONAL_TARIFFS_COUNTRY_SELECT_ENABLED=true; \
	export DIRECTORY_API_CLIENT_API_KEY=debug; \
	export DIRECTORY_API_CLIENT_BASE_URL=http://api.trade.great:8000; \
	export DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC=http://exred.trade.great:8007/; \
	export DIRECTORY_CONSTANTS_URL_GREAT_INTERNATIONAL=http://international.trade.great:8012/international/; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_BUYER=http://buyer.trade.great:8001; \
	export DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS=http://soo.trade.great:8008; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER=http://international.trade.great:8012/international/trade/; \
	export DIRECTORY_CONSTANTS_URL_INVEST=http://international.trade.great:8012/international/invest/; \
	export DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON=http://sso.trade.great:8004; \
	export IP_RESTRICTOR_RESTRICT_UI=true; \
	export LANGUAGE_COOKIE_DOMAIN=.trade.great; \
	export DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=15; \
	export DIRECTORY_FORMS_API_API_KEY=debug; \
	export DIRECTORY_FORMS_API_SENDER_ID=debug; \
	export EU_EXIT_ZENDESK_SUBDOMAIN=debug; \
	export FEATURE_CAPITAL_INVEST_LANDING_PAGE_ENABLED=true; \
	export FEATURE_CAPITAL_INVEST_REGION_PAGE_ENABLED=true; \
	export FEATURE_ABOUT_UK_REGION_PAGE_ENABLED=true; \
	export FEATURE_ABOUT_UK_REGION_LISTING_PAGE_ENABLED=true; \
	export FEATURE_CAPITAL_INVEST_OPPORTUNITY_PAGE_ENABLED=true; \
	export FEATURE_CAPITAL_INVEST_OPPORTUNITY_LISTING_PAGE_ENABLED=true; \
	export FEATURE_CAPITAL_INVEST_REGION_SECTOR_OPP_PAGE_ENABLED=true; \
	export FEATURE_CAPITAL_INVEST_SUB_SECTOR_PAGE_ENABLED=true; \
	export FEATURE_CAPITAL_INVEST_CONTACT_FORM_PAGE_ENABLED=true; \
	export FEATURE_EXPAND_REDIRECT_ENABLED=false; \
	export FEATURE_GUIDE_TO_BUSINESS_ENVIRONMENT_FORM_ENABLED=true; \
	export PFP_API_CLIENT_API_KEY=debug; \
	export PFP_API_CLIENT_BASE_URL=http://pfp.trade.great:8014; \
	export PFP_AWS_S3_PDF_STORE_ACCESS_KEY_ID=debug; \
	export PFP_AWS_S3_PDF_STORE_SECRET_ACCESS_KEY=debug; \
	export PFP_AWS_S3_PDF_STORE_BUCKET_NAME=debug; \
	export THUMBNAIL_STORAGE_CLASS_NAME=local-storage; \
	export THUMBNAIL_KVSTORE_CLASS_NAME=redis; \
	export FEATURE_INVESTMENT_SUPPORT_DIRECTORY_ENABLED=True; \
	export FEATURE_FIND_A_SUPPLIER_ENABLED=True; \
	export FEATURE_NEW_IA_ENABLED=True; \
	export FEATURE_HOW_TO_SET_UP_REDIRECT_ENABLED=false; \
	export FEATURE_INDUSTRIES_REDIRECT_ENABLED=false; \
	export FEATURE_EXPORTING_TO_UK_ON_ENABLED=true; \
	export FEATURE_CAPITAL_INVEST_CONTACT_IN_TRIAGE_ENABLED=true; \
	export CONTACT_INDUSTRY_AGENT_EMAIL_ADDRESS=buying@example.com; \
	export GUIDE_TO_UK_BUSINESS_ENVIRONMENT_AGENT_EMAIL=debug

TEST_SET_ENV_VARS := \
	export DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export DIRECTORY_FORMS_API_API_KEY=debug; \
	export DIRECTORY_FORMS_API_SENDER_ID=debug; \
	export REDIS_URL=; \
	export DIRECTORY_API_CLIENT_API_KEY=debug; \
	export DIRECTORY_API_CLIENT_BASE_URL=http://debug.com; \
	export EU_EXIT_ZENDESK_SUBDOMAIN=debug; \
	export DEBUG=false

debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST) --cov-report=html

debug_test_last_failed:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST) --last-failed --cov-report=html

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
