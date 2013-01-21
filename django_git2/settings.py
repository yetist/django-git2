""" Settings of django_git2 """
from django.conf import settings

### Default page title and description.
#
TITLE = getattr(settings, 'DJANGO_GIT2_TITLE', 'Git repository browser')
DESCRIPTION = getattr(settings, 'DJANGO_GIT2_DESCRIPTION', 'a fast webinterface for the git dscm')

### Commits per page shown in Log section
# Default value is 'utf8'.
#
#DJANGO_GIT2_MESSAGE_CHARSET = 'utf8'
MESSAGE_CHARSET = getattr(settings, 'DJANGO_GIT2_MESSAGE_CHARSET', 'utf8')

### Commits per page shown in Log section
# Default value is 50.
#
#DJANGO_GIT2_COMMITS_PER_PAGE = 50
COMMITS_PER_PAGE = getattr(settings, 'DJANGO_GIT2_COMMITS_PER_PAGE', 50)

### Number of commits shown in Summary section
# Default value is 15
#
#DJANGO_GIT2_COMMITS_IN_SUMMARY = 15
COMMITS_IN_SUMMARY = getattr(settings, 'DJANGO_GIT2_COMMITS_IN_SUMMARY', 10)

### Maximal length of one line comment (shown for example in log)
# Default value is 50
#
#DJANGO_GIT2_ONE_LINE_COMMENT_MAX_LEN = 50
ONE_LINE_COMMENT_MAX_LEN = getattr(settings, 'DJANGO_GIT2_ONE_LINE_COMMENT_MAX_LEN', 50)

### Owner of project
#
#DJANGO_GIT2_DEFAULT_OWNER = 'yetist <yetist@gmail.com>'
DEFAULT_OWNER = getattr(settings, 'DJANGO_GIT2_DEFAULT_OWNER', 'yetist <yetist@gmail.com>')

### List of urls from which can be repository cloned
#
#DJANGO_GIT2_URLS = ['git://git.project.net', 'https://project.net/git']
URLS = getattr(settings, 'DJANGO_GIT2_URLS', [])

### List of formats in which snapshots can be downloaded.
# Available formats are 'tgz', 'tbz2', 'txz', 'zip'
#
# DJANGO_GIT2_SNAPSHOTS = ['tgz', 'tbz2', 'txz', 'zip']
SNAPSHOTS = getattr(settings, 'DJANGO_GIT2_SNAPSHOTS ', ['tgz', 'tbz2'])

### Supported git repo type and path
# Avaiable types are 'parent', 'gitosis'
# if 'parent', should setup the path of the git repos parents.
# if 'gitosis', should setup the file's path that have repos infomations.
#
#DJANGO_GIT2_GIT_REPO_PATH = {
#        'parent': '/home/yetist/Dropbox/repos/',
#        'gitosis': "/home/git/gitosis/repos.list"
#        }
GIT_REPO_PATH = getattr(settings, 'DJANGO_GIT2_GIT_REPO_PATH', {})
