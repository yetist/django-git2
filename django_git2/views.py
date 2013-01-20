from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core import urlresolvers

from django_git2 import settings
from django_git2 import util

import os
import pygit2

from pprint import pprint
from operator import itemgetter, attrgetter  

_commits_in_summary = 15

def list(request):
    projs = util.get_projects()
    sort = request.GET.get('s', '')
    query = request.GET.get('q', '')
    if query != '':
        projects = []
        for k,v in projs:
            lst = []
            for i in v:
                if i['name'].decode(settings.message_charset).lower().find(query) >= 0 or i['desc'].decode(settings.message_charset).lower().find(query) >= 0:
                    lst.append(i)
            if len(lst) > 0:
                lst.sort(key=lambda x:x['name'])
                projects.append((k, lst))
        projs = projects
    if sort == "name":
        projects = []
        lst = []
        for k,v in projs:
            for i in v:
                lst.append(i)
        lst.sort(key=lambda x:x['name'])
        projects.append(('', lst))
    elif sort == "desc":
        projects = []
        lst = []
        for k,v in projs:
            for i in v:
                lst.append(i)
        lst.sort(key=lambda x:x['desc'])
        projects.append(('', lst))
    elif sort == "owner":
        projects = []
        lst = []
        for k,v in projs:
            for i in v:
                lst.append(i)
        lst.sort(key=lambda x:x['owner'])
        projects.append(('', lst))
    elif sort == "idle":
        projects = []
        lst = []
        for k,v in projs:
            for i in v:
                lst.append(i)
        lst.sort(key=lambda x:x['idle'], reverse=True)
        projects.append(('', lst))
    else:
        projects = projs
    ctx = {
            'projects':projects,
            'query':query
          }
    return render_to_response("django_git2/list.html", ctx, context_instance=RequestContext(request))

def summary(request, repo):
    r = util.Git(repo)
    ctx = r.get_summary()
    ctx['current'] = 'summary'
    return render_to_response("django_git2/summary.html", ctx, context_instance=RequestContext(request))

def refs(request, repo):
    r = util.Git(repo)
    ctx = r.get_refs()
    ctx['current'] = 'refs'
    return render_to_response("django_git2/refs.html", ctx, context_instance=RequestContext(request))

def log(request, repo):
    gitpath = os.path.join(settings.parent_path, repo + ".git")
    if os.path.isdir(gitpath):
        gitrepo = pygit2.Repository(gitpath)
        meta = {
                'current':'log',
                'project':repo,
                }
        ctx = {
            'project': repo,
            'meta': meta,
            'repo': gitrepo,
            'refs': getrefs(gitrepo),
            'owner': 'owner',
            'homepage': 'http://',
            }
        return render_to_response("django_git2/log.html", ctx, context_instance=RequestContext(request))

def about(request, repo):
    gitpath = os.path.join(settings.parent_path, repo + ".git")
    if os.path.isdir(gitpath):
        gitrepo = pygit2.Repository(gitpath)

def commit(request, repo):
    gitpath = os.path.join(settings.parent_path, repo + ".git")
    if os.path.isdir(gitpath):
        gitrepo = pygit2.Repository(gitpath)
        meta = {
                'current':'log',
                'project':repo,
                }
        ctx = {
            'project': repo,
            'meta': meta,
            'repo': gitrepo,
            'refs': getrefs(gitrepo),
            'owner': 'owner',
            'homepage': 'http://',
            }
        return render_to_response("django_git2/commit.html", ctx, context_instance=RequestContext(request))

def tag(request, repo):
    r = util.Git(repo)
    if 'id' in request.GET and request.GET['id']:
        tid = request.GET['id']
        ctx = r.get_tag(tid)
        ctx['current'] = 'tag'
        return render_to_response("django_git2/tag.html", ctx, context_instance=RequestContext(request))
    else:
        "Bad tag reference: master"
