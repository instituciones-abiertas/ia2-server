SHELL=/bin/bash
.DEFAULT_GOAL := help

# -------------------------------
# Common targets for Dev projects
# -------------------------------
#
# Edit these targets so they work as expected on the current project.
#
# Remember there may be other tools which use these targets, so if a target is not suitable for
# the current project, then keep the target and simply make it do nothing.

help: ## This help dialog.
help: help-display

nuke: ## Wipes database
nuke: django-drop-db

reset: ## Resets your local environment. Useful after switching branches, etc.
reset: venv-check venv-wipe pip-install django-migrate

nuke-reset: ## Nuke & Reset & Load fixtures
nuke-reset: nuke reset django-load-fixtures

clear: ## Like reset but without the wiping of the installs.
clear: django-migrate

test: ## Run tests.
test: django-test

# ---------------
# Utility targets
# ---------------
#
# Targets which are used by the common targets. You likely want to customise these per project,
# to ensure they're pointing at the correct directories, etc.

# Virtual Environments
venv-check:
ifndef VIRTUAL_ENV
	$(error Must be in a virtualenv)
endif

venv-wipe: venv-check
	if ! pip list --format=freeze | grep -v "^appdirs=\|^distribute=\|^packaging=\|^pip=\|^pyparsing=\|^setuptools=\|^six=\|^wheel=" | xargs pip uninstall -y; then \
	    echo "Nothing to remove"; \
	fi


# Pip
pip-install: venv-check
	pip install -r requirements/local.txt


# Django
django-test: 
	./manage.py test 

django-createsuperuser: DJANGO_DEV_USERNAME ?= admin
django-createsuperuser: DJANGO_DEV_MAIL_DOMAIN ?= @camba.coop
django-createsuperuser: DJANGO_DEV_PASSWORD ?= admin
django-createsuperuser:
	@echo "import sys; from django.contrib.auth import get_user_model; obj = get_user_model().objects.create_superuser('$(DJANGO_DEV_USERNAME)', '$(DJANGO_DEV_USERNAME)$(DJANGO_DEV_MAIL_DOMAIN)', '$(DJANGO_DEV_PASSWORD)');" | python manage.py shell >> /dev/null
	@echo
	@echo "Superuser details: "
	@echo
	@echo "    $(DJANGO_DEV_USERNAME)$(DJANGO_DEV_MAIL_DOMAIN):$(DJANGO_DEV_PASSWORD)"
	@echo

django-migrate:
	./manage.py migrate

django-drop-db:

	./manage.py sqlflush | ./manage.py dbshell

django-load-fixtures:
	for i in $$(find . -wholename "*/fixtures/*.json"  -printf "%f\n" | sort -t '\0' -n); do \
	    echo "Loading $$i" ;\
		find -name $$i -exec python manage.py loaddata {}   \; ;\
	done

django-compile-messages:
	./manage.py compilemessages

# Help
help-display:
	@awk '/^[[:alnum:]-]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)
