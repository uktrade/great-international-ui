ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

pytest:
	ENV_FILES='test,dev' pytest $(ARGUMENTS)

test:
	flake8 && make pytest

manage:
	ENV_FILES='secrets-do-not-commit,dev' ./manage.py $(ARGUMENTS)

webserver:
	ENV_FILES='secrets-do-not-commit,dev' python manage.py runserver 0.0.0.0:8012 $(ARGUMENTS)

requirements:
	pip-compile --upgrade -r --annotate  requirements.in
	pip-compile --upgrade -r --annotate requirements_test.in

install_requirements:
	pip install -r requirements_test.txt

secrets:
	@if [ ! -f ./conf/env/secrets-do-not-commit ]; \
		then sed -e 's/#DO NOT ADD SECRETS TO THIS FILE//g' conf/env/secrets-template > conf/env/secrets-do-not-commit \
			&& echo "Created conf/env/secrets-do-not-commit"; \
		else echo "conf/env/secrets-do-not-commit already exists. Delete first to recreate it."; \
	fi

# Usage: make pytest_single <path_to_file>::<method_name>
pytest_single:
	ENV_FILES='secrets-do-not-commit,test,dev' \
	pytest \
	    $(ARGUMENTS)
		--junit-xml=./results/pytest_unit_report.xml \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov=. \

pytest_codecov:
	ENV_FILES='secrets-do-not-commit,test,dev' \
	pytest \
		--junitxml=test-reports/junit.xml \
		--cov-config=.coveragerc \
		--cov-report=term \
		--cov=. \
		--codecov \
		$(ARGUMENTS)
		
.PHONY: clean pytest manage webserver requirements install_requirements secrets
