import os
from typing import Tuple

import click

from .env_keys import ORGANIZATION_KEY, TOKEN_KEY, WORKSPACE_KEY


def get_org_workspace():
    token = os.getenv(TOKEN_KEY)
    if token:
        try:
            _, user, _ = token.split(":", 2)
            org, workspace = user.split("/", 1)
            return org, workspace
        except ValueError:
            return None, None

    return os.getenv(ORGANIZATION_KEY), os.getenv(WORKSPACE_KEY)


def ensure_org_workspace() -> Tuple[str, str]:
    org, workspace = get_org_workspace()
    if org is None or workspace is None:
        raise click.UsageError(click.style(
            "Could not identify Launchable organization/workspace. "
            "Please confirm if you set LAUNCHABLE_TOKEN or LAUNCHABLE_ORGANIZATION and LAUNCHABLE_WORKSPACE environment variables",
            fg="red"))
    return org, workspace


def authentication_headers():
    token = os.getenv(TOKEN_KEY)
    if token:
        return {'Authorization': 'Bearer {}'.format(token)}

    if os.getenv('GITHUB_ACTIONS'):
        headers = {
            'GitHub-Actions': os.environ['GITHUB_ACTIONS'],
            'GitHub-Run-Id': os.environ['GITHUB_RUN_ID'],
            'GitHub-Repository': os.environ['GITHUB_REPOSITORY'],
            'GitHub-Workflow': os.environ['GITHUB_WORKFLOW'],
            'GitHub-Run-Number': os.environ['GITHUB_RUN_NUMBER'],
            'GitHub-Event-Name': os.environ['GITHUB_EVENT_NAME'],
            'GitHub-Sha': os.environ['GITHUB_SHA'],
        }

        # GITHUB_PR_HEAD_SHA might not exist
        pr_head_sha = os.getenv('GITHUB_PR_HEAD_SHA')
        if pr_head_sha:
            headers['GitHub-Pr-Head-Sha'] = pr_head_sha

        return headers
    return {}
