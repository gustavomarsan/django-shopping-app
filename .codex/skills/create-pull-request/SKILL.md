---
name: create-pull-request
description: Prepare and create a GitHub pull request from the current feature branch to main for this repository, after reviewing changes and running appropriate checks.
---

# Create Pull Request

Use this skill when the user asks to prepare, commit, push, or open a pull request for the current repository.

## Workflow

1. Inspect the repository instructions, current branch, remote, working-tree status, and diff.
2. Confirm the current branch is not `main`. Never create a pull request from `main` unless the user explicitly requests it.
3. Identify the project’s normal validation commands. For this Django project, run the relevant tests and `python manage.py check` when possible.
4. Report the proposed commit scope, validation results, target branch, and any warnings. Do not include unrelated user changes in the commit.
5. Ask for explicit approval immediately before any external or Git mutation: committing, pushing, or opening the pull request.
6. After approval, create a concise commit, push the current branch to `origin`, and open a pull request targeting `main` using `gh pr create` when GitHub CLI authentication is available.
7. Use a title and description that summarize the actual diff. Include validation commands and results in the pull request body.
8. Never merge the pull request automatically. Stop after reporting the pull request URL, or report the exact blocker if creation fails.

## Safety boundaries

- This skill is project-local and applies only when invoked from this repository.
- Never reset, checkout, clean, or delete user changes.
- Never commit secrets, `.env` files, generated databases, or unrelated changes.
- Do not invent test results. Clearly report skipped or failed checks.
- If the branch has no changes, report that there is nothing to commit and do not create an empty commit.
- If `gh` is unavailable or unauthenticated, stop after preparing the commit/push plan and explain what must be configured.
