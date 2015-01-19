# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json
import urllib2

from fabric.api import abort, local, task
from fabric.contrib.console import confirm

from .utils import git, ui


@task(default=True)
def merge(number):
    '''Prepare and push a pull request.'''
    author, branch = patch(number)

    print ui.info('Changes checked out. Rebasing and squashing...')
    local('git fetch origin; git rebase origin/master')
    commits_ahead = git.commits_ahead('origin')
    local('git rebase -i HEAD~%d' % commits_ahead)

    if not confirm(ui.warning('Changes squashed. Push?')):
        abort('Push canceled.')

    local('git checkout master; git merge %s --ff-only' % branch)
    local('git pull --rebase')
    local('git push')

    print ui.success('Changes pushed! Deleting branch...')
    local('git branch -d %s' % branch)


@task
def patch(number):
    '''Fetch the branch associated with the given pull request.'''
    url = 'https://api.github.com/repos/bmun/huxley/pulls/%s' % number
    pr = json.loads(urllib2.urlopen(url).read())
    author = pr['head']['user']['login']
    repo = pr['head']['repo']['clone_url']
    branch = pr['head']['ref']

    print ui.info('Checking out %s from %s...' % (branch, author))
    local('git fetch %s %s:%s' % (repo, branch, branch))
    local('git checkout %s' % branch)

    return (author, branch)
