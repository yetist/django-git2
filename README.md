# Django Git2

**django-git2 is a git browser app for django.**

It use [pygit2](https://github.com/libgit2/pygit2), the UI like [cgit](http://hjemli.net/git/cgit/).

## Requirements

Django-git2 requires the following:

* Python (2.6, 2.7)
* Django (1.3, 1.4, 1.5)

The following packages are optional:

* Pygments (1.4+) - code highlight
* Pygit2 (git version) - Python bindings for libgit2

## Installation

To clone the project from GitHub using git:

    git clone https://github.com/yetist/django-git2.git

To install django-git2 in a virtualenv environment:

    cd django-git2
    virtualenv --no-site-packages --distribute env
    source env/bin/activate
    pip install -r requirements.txt # django, pygit2
    python setup.py install_lib

## Usage

Add `'django_git2'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
    ...
    'django_git2',
    )

Add the following to your root `urls.py` file.

    urlpatterns = patterns('',
        ...
        url(r'^git/', include('django_git2.urls', namespace='django_git2')),
    )

Add the following line to your setting file.

    ### Setup git repo default owner
    DJANGO_GIT2_DEFAULT_OWNER = 'yourname <your@email.com>'
    
    ### Setup git clone url
    DJANGO_GIT2_URLS = ['git://git.project.net', 'https://project.net/git']
    
    ### setup git repo here
    DJANGO_GIT2_GIT_REPO_PATH = {}
    
    # if you have some repos under the same parent directory, should use:
    # DJANGO_GIT2_GIT_REPO_PATH['parent'] = '/the/git/repos/parents/directory/'
    
    # if you want to support gitosis's repos.list, like this:
    # DJANGO_GIT2_GIT_REPO_PATH['gitosis']='/home/git/gitosis/repos.list'

## Example

To see the example:

	cd examples
	python manage.py syncdb
	python manage.py runserver
