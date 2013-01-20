from django.conf.urls.defaults import *

urlpatterns = patterns('django_git2.views',
    url(r'^(?P<repo>[\w_-]+)/log/$', 'log', name='django-git-log'),
    url(r'^(?P<repo>[\w_-]+)/refs/$', 'refs', name='django-git-refs'),
    url(r'^(?P<repo>[\w_-]+)/tag/$', 'tag', name='django-git-tag'),
    url(r'^(?P<repo>[\w_-]+)/tree/', 'tree', name='django-git-tree'),
    url(r'^(?P<repo>[\w_-]+)/plain/', 'plain', name='django-git-plain'),

#    url(r'^(?P<repo>[\w_-]+)/commit/(?P<commit>[\w\d]+)/blob/$', 'blob', name='django-git-blob'),
#    url(r'^(?P<repo>[\w_-]+)/commit/(?P<commit>[\w\d]+)/$', 'commit', name='django-git-commit'),
    url(r'^(?P<repo>[\w_-]+)/commit/$', 'commit', name='django-git-commit'),
#    url(r'^(?P<repo>[\w_-]+)/diff/$', 'repo', name='django-git-repo'),
#    url(r'^(?P<repo>[\w_-]+)/tag/$', 'repo', name='django-git-repo'),
#    url(r'^(?P<repo>[\w_-]+)/patch/$', 'repo', name='django-git-repo'),
#    url(r'^(?P<repo>[\w_-]+)/plain/$', 'repo', name='django-git-repo'),

#    url(r'^(?P<repo>[\w_-]+)/patch/$', 'repo', name='django-git-repo'),
#    url(r'^(?P<repo>[\w_-]+)/patch/$', 'repo', name='django-git-repo'),
#    url(r'^(?P<repo>[\w_-]+)/patch/$', 'repo', name='django-git-repo'),
#    url(r'^(?P<repo>[\w_-]+)/patch/$', 'repo', name='django-git-repo'),
    url(r'^(?P<repo>[\w_-]+)/', 'summary', name='django-git-summary'),
    url(r'^$', 'list', name='django-git-list'),
)
