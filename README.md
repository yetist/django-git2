django-git2
===========

git browser app for django use pygit2

Usage
===========

mysite/settings.py

	INSTALLED_APPS = (
	...
	'django_git2',
	...
	)

	DJANGO_GIT2_URLS = ['git://git.project.net', 'https://project.net/git']

	DJANGO_GIT2_GIT_REPO_PATH = {'parent': '/home/yetist/Dropbox/repos/'}

	DJANGO_GIT2_DEFAULT_OWNER = 'yetist <yetist@gmail.com>'


mysite/urls.py

	urlpatterns = patterns('',
	...
	url(r'^git/', include('django_git2.urls')),
	...
	)


Installation Notes
=====================

To clone the project from GitHub using git:

	git clone git@github.com:yetist/django-git2.git

To install django-git2 in a virtualenv environment:

	cd django-git2
	virtualenv --no-site-packages --distribute env
	source env/bin/activate
	pip install -r requirements.txt # django, pygit2

To run the examples:

	cd examples
	export PYTHONPATH=..
	python manage.py syncdb
	python manage.py runserver

To build the documentation:

	pip install -r docs/requirements.txt   # sphinx
	sphinx-build -c docs -b html -d docs/build docs html

To run the tests against the full set of supported configurations:

	deactivate  # Ensure we are not currently running in a virtualenv
	tox

To create the sdist packages:

	python setup.py sdist --formats=gztar,zip
