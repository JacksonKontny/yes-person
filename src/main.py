import time

from src.env import (
    APPROVAL_USERS,
    REPO_OWNER,
    APPROVALS_REQUIRED,
    INTERVAL_IN_SECONDS,
    TITLE_REGEX,
    REPO,
)
from src.gh.api import get_pulls, should_approve_pull, submit_pr_review


def run():
    while True:
        open_prs = get_pulls(REPO, owner=REPO_OWNER)
        prs_to_approve = [
            pr
            for pr in open_prs
            if should_approve_pull(pr, APPROVAL_USERS, APPROVALS_REQUIRED, TITLE_REGEX)
        ]
        if len(prs_to_approve) == 0:
            print("No PRs to approve...")
        for pr in prs_to_approve:
            print(f'APPROVING PR: "{pr.title}" for user: "{pr.username}"')
            submit_pr_review(pr, owner=REPO_OWNER)
            print(f"APPROVED PR: {pr.title} for user: {pr.username}")
        time.sleep(INTERVAL_IN_SECONDS)


if __name__ == "__main__":
    run()
