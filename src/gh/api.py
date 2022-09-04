from functools import cached_property, cache
from typing import List
from src.env import GITHUB_TOKEN

import requests


BASE = 'https://api.github.com'
REPO = 'core-infrastructure'
APPROVE = 'APPROVE'


class PullRequest():
    def __init__(self, resp):
        self._resp = resp

    @property
    def title(self):
        return self._resp['title']

    @property
    def username(self):
        return self._resp['user']['login']

    @property
    def id(self):
        return self._resp['id']

    @property
    def pr_number(self):
        return self._resp['number']

    @property
    def head(self):
        return self._resp['head']

    @property
    def commit_hash(self):
        return self.head['sha']

    @property
    def branch_name(self):
        return self.head['ref']

    @property
    def repo_name(self):
        return self.head['repo']['name']
    @property
    def owner_name(self):
        return self.head['repo']['owner']['login']

    @cached_property
    def review_comments(self):
        return get_reviews(self.repo_name, self.pr_number, owner=self.owner_name)


class ReviewComment():
    def __init__(self, resp):
        self._resp = resp

    @property
    def username(self):
        return self._resp['user']['login']

    @property
    def is_approved(self):
        return self._resp['state'] == 'APPROVED'


def get_pulls(repo, owner='github', state='open'):
    resp = requests.get(
        f'{BASE}/repos/{owner}/{repo}/pulls', headers=get_headers(), params={'state': state, 'per_page': 100}).json()
    return [PullRequest(pr_resp) for pr_resp in resp]


def should_approve_pull(pull: PullRequest, approval_users: List, comment_limit: int):
    if pull.username not in approval_users:
        return False
    approved_comments = [
        comment for comment in pull.review_comments if comment.is_approved
    ]
    user_not_in_approved_comments = get_username_for_token() not in set([comment.username for comment in approved_comments])
    return user_not_in_approved_comments and len(approved_comments) < comment_limit


@cache
def get_username_for_token():
    return requests.get(
        f'{BASE}/user',
        headers=get_headers()
    ).json()['login']


def get_reviews(repo, pr_number, owner="github"):
    return [ReviewComment(comment_json) for comment_json in requests.get(
        f'{BASE}/repos/{owner}/{repo}/pulls/{pr_number}/reviews',
        headers=get_headers()
    ).json()]


def get_headers():
    return {'Authorization': 'token ' + GITHUB_TOKEN, 'Accept': 'application/vnd.github+json'}


def submit_pr_review(pr: PullRequest, body='LGTM', event=APPROVE, owner="github"):
    return requests.post(
        f'{BASE}/repos/{owner}/{pr.repo_name}/pulls/{pr.pr_number}/reviews',
        headers=get_headers(),
        json={
            'commit_id': pr.commit_hash,
            'body': body,
            'event': event
        },
    ).json()