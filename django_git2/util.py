#! /usr/bin/env python2
# -*- encoding:utf-8 -*-
# FileName: util.py

if __name__=="__main__":
    import settings
else:
    from django_git2 import settings

import os
import operator
import pygit2
from pprint import pprint

def get_projects():
    projects = {}
    if settings.GIT_SUPPORT.has_key('gitosis'):
        projects = get_gitosis(settings.GIT_SUPPORT['gitosis'])
    if settings.GIT_SUPPORT.has_key('parent'):
        if projects.has_key(''):
            lst = projects['']
        else:
            lst = []
            projects[''] = lst
        for i in os.listdir(settings.GIT_SUPPORT['parent']):
            path = os.path.join(settings.GIT_SUPPORT['parent'], i)
            project = get_one_project(path)
            lst.append(project)
    sorted_projects = sorted(projects.iteritems(), key=operator.itemgetter(0))
    return sorted_projects

def get_one_project(path):
    project = {}
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    if ext == ".git":
        desc = os.path.join(path, "description")
        project['name'] = name
        project['url'] = basename
        project['owner'] = settings.owner
        project['desc'] = open(desc).read()
        project['path'] = path
        repo = pygit2.Repository(path)
        project['idle'] = repo.head.commit_time
    return project

def get_gitosis(path):
    projects = {}
    bufs = open(path).read()
    sections = bufs.split("section=")
    for i in sections:
        i = i.strip()
        head = i.splitlines()[0]
        if head.startswith("repo."):
            group = ''
            project = {}
            projects[group] = [project]
        else:
            group = head
            project = {}
            projects[group] = [project]
        for l in i.splitlines():
            line = l.strip()
            if line.startswith("repo."):
                key_value = line.split("=")
                key = key_value[0][5:]
                value = key_value[1]
                project[key] = value
                if key == "path":
                    repo = pygit2.Repository(value)
                    project['idle'] = repo.head.commit_time
            elif line == "":
                if len(project) != 0:
                    projects[group].append(project)
                    project = {}
    return projects

def get_repo_byname(repo):
    projects = get_projects()
    for k,v in projects:
        for i in v:
            if i['name'] == repo:
                path = i['path']
                return i
    else:
        return None

#def _find_parents(repo):
#    p = len(repo.parents)
#    if p == 1:
#        yield p[0]
#    else:
#        for i in repo.parents:
#            yield i
#            _find_parents(i)
#
def _get_parents(repo):
        walker = repo.walk(log[0], GIT_SORT_TIME)
        out = [ x.hex for x in walker ]
#    repo = repo.parents
#    if len(repo) > 1:
#        for i in repo:
#            lst.append(i)
#            print i.type
#    else:
#        print repo[0].type
#        lst.append(repo)
#        _get_parents(repo, lst)

class Git(object):
    def __init__(self, project):
        self.project = get_repo_byname(project)
        self.repo = pygit2.Repository(self.project['path'])

    def _get_refs(self):
        d = {
            'branch':[],
            'tags':[],
            }
        refs = self.repo.listall_references()
        for i in refs:
            if i.startswith('refs/heads/'):
                e = self.repo.lookup_reference(i)
                c = self.repo[e.oid]
                d['branch'].append((i[11:], c))
            if i.startswith('refs/tags/'):
                e = self.repo.lookup_reference(i)
                c = self.repo[e.oid]
                d['tags'].append((i[10:], c))
        return d

    def get_summary(self):
        walker = self.repo.walk(self.repo.head.hex, pygit2.GIT_SORT_TIME)
        commits = [ x for x in walker ]
        commits_more = False
        if len(commits) > 10:
            commits = commits[:10]
            commits_more = True

        refs = self._get_refs()
        ctx = {
                "refs": self._get_refs(),
                "project": self.project,
                "commits": commits,
                "commits_more": commits_more
                }
        print dir(commits[0])
        return ctx

    def get_refs(self):
        ctx = {
                "project": self.project,
                "refs": self._get_refs()
                }
        return ctx

    def get_tag(self, tid):
        ref = self.repo.lookup_reference('refs/tags/'+tid)
        tag = self.repo[ref.oid]
        commit = self.repo[tag.target]
        ctx = {
                "project": self.project,
                'id': tid,
                'tag': tag,
                "current": "summary",
                'commit': commit,
                }
        return ctx

if __name__=="__main__":
    #print get_projects()
    #get_repo_byname("ustore")
    a=Git("sunshine")
    #print a.get_refs()
    print a.get_summary()
