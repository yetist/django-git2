#! /usr/bin/env python2
# -*- encoding:utf-8 -*-
# FileName: util.py

import os

if __name__=="__main__":
    import sys
    sys.path.insert(0, '../examples')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    import settings
else:
    from django_git2 import settings

import stat
import operator
import pygit2
from pprint import pprint

def get_projects():
    projects = {}
    if settings.GIT_REPO_PATH.has_key('gitosis'):
        projects = get_gitosis(settings.GIT_REPO_PATH['gitosis'])
    if settings.GIT_REPO_PATH.has_key('parent'):
        if projects.has_key(''):
            lst = projects['']
        else:
            lst = []
            projects[''] = lst
        for i in os.listdir(settings.GIT_REPO_PATH['parent']):
            path = os.path.join(settings.GIT_REPO_PATH['parent'], i)
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
        project['owner'] = settings.DEFAULT_OWNER
        project['desc'] = open(desc).read()
        project['path'] = path
        project['readme'] = "master:README"
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

def get_filemode(mode):
    m = oct(mode)
    perm = m[4:]
    permstring = ["-"]
    for i in perm:
        p = int(i)
        l = []
        if p & 4: l.append("r")
        else: l.append("-")
        if p & 2: l.append("w")
        else: l.append("-")
        if p & 1: l.append("-")
        else: l.append("-")
        permstring.append("".join(l))
    return "".join(permstring)

def get_repo_byname(repo):
    projects = get_projects()
    for k,v in projects:
        for i in v:
            if i['name'] == repo:
                path = i['path']
                return i
    else:
        return None

def get_tree_entries(tree, trees, path=""):
    for entry in tree:
        item = {}
        obj = entry.to_object()
        ext = os.path.splitext(entry.name)[1]
        if stat.S_ISDIR(entry.filemode):
            item['type'] = "dir"
            item['filemode'] = "d---------"
            item['size'] = len(obj.read_raw())
        else:
            item['type'] = "blob"
            item['filemode'] = get_filemode(entry.filemode)
            item['size'] = obj.size
            if ext != '':
                item['type'] = item['type'] + " " + ext[1:]
        item['name'] = entry.name
        item['path'] = os.path.join(path, entry.name)
        item['hex'] = entry.hex
        trees.append(item)

class Git(object):
    def __init__(self, project):
        self.project = get_repo_byname(project)
        if self.project is None:
            self.repo = None
        else:
            self.repo = pygit2.Repository(self.project['path'])
            self.refs = self._get_refs()

    def _get_refs(self):
        refs = {
            'branches':[],
            'tags':[],
            'head':self.repo.head.hex,
            }
        all_refs = self.repo.listall_references()
        for i in all_refs:
            if i.startswith('refs/heads/'):
                ref = self.repo.lookup_reference(i)
                commit = self.repo[ref.oid]
                refs['branches'].append((i[11:], commit))
            if i.startswith('refs/tags/'):
                ref = self.repo.lookup_reference(i)
                tag = self.repo[ref.oid]
                commit = self.repo[tag.target]
                refs['tags'].append((i[10:], tag, commit))
        return refs

    def has_error(self):
        if self.repo is None:
            return True

    def get_summary(self):
        branches_more = False
        refs = self._get_refs()
        if len(refs['branches']) > settings.BRANCHES_IN_SUMMARY:
            refs['branches'] = self.refs['branches'][:settings.BRANCHES_IN_SUMMARY]
            branches_more = True

        tags_more = False
        if len(refs['tags']) > settings.TAGS_IN_SUMMARY:
            refs['tags'] = self.refs['tags'][:settings.TAGS_IN_SUMMARY]
            tags_more = True

        walker = self.repo.walk(self.repo.head.hex, pygit2.GIT_SORT_TIME)
        commits = [ x for x in walker ]
        commits_more = False
        if len(commits) > settings.COMMITS_IN_SUMMARY:
            commits = commits[:settings.COMMITS_IN_SUMMARY]
            commits_more = True

        ctx = {
                "project": self.project,
                "refs": refs,
                "tags_more": tags_more,
                "branches_more": branches_more,
                "commits": commits,
                "commits_more": commits_more,
              }
        return ctx

    def get_refs(self):
        ctx = {
                "project": self.project,
                "refs": self._get_refs()
                }
        return ctx

    def get_log(self):
        refs = self._get_refs()
        walker = self.repo.walk(self.repo.head.hex, pygit2.GIT_SORT_TIME)
        commits = [ x for x in walker ]
        commits_more = False
        if len(commits) > 50:
            commits = commits[:50]
            commits_more = True

        ctx = {
                "refs": refs,
                "project": self.project,
                "commits": commits,
                "commits_more": commits_more
                }
        return ctx

    def get_tree(self, filepath):
        trees = []
        commit = self.repo[self.repo.head.hex]
        tree = commit.tree
        data = None
        ctx = {"project": self.project,
                "trees": trees}
        if filepath == "":
            get_tree_entries(tree, trees)
        else:
            ctx["filepath"] = filepath
            entry = tree[filepath]
            if stat.S_ISDIR(entry.filemode):
                tree = entry.to_object()
                get_tree_entries(tree, trees, filepath)
            else:
                obj = entry.to_object()
                ctx['blob'] = obj
                ctx['lines'] = [i+1 for i in range(len(obj.data.splitlines()))]
        return ctx

    def get_commit(self, cid=''):
        refs = self._get_refs()
        ctx = {"project": self.project}
        if cid == '':
            commit = self.repo[self.repo.head.hex]
        else:
            commit = self.repo[unicode(cid)]
        ctx['commit'] = commit
        ctx['refs'] = refs

        if len(commit.parents) > 0:
            commit_b = self.repo[commit.parents[0].hex]
            diff = commit_b.tree.diff(commit.tree)
            try:
                ctx['patch'] = diff.patch.decode('utf-8')
            except UnicodeDecodeError:
                ctx['patch'] = diff.patch
        else:
            tb = self.repo.TreeBuilder()
            diff = self.repo[tb.write()].diff(commit.tree)
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
    #print a.get_summary()
    #print a.get_tree('data/addon.desc')
    cid = "91251a60a15581bbb0f5676dd81717f97272f69d"
    first_cid = "93252c36d23a19ee5744df96532c60d3b0c20c3c"
    a.get_commit(first_cid)
