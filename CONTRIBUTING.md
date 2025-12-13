# Contributing

Thank you for your interest in contributing. This document explains how to get started, the workflow we follow, and the standards we expect for code, tests, docs, and reviews.

## Purpose
This repository values clear, well-tested, and maintainable contributions. Follow the guidance below to make it easier for maintainers to review and accept your work.

## Code of Conduct
All contributors must follow the project's Code of Conduct. Be respectful, constructive, and inclusive in discussions and reviews.

## Getting started (local setup)
1. Fork the repository and clone your fork:
    ```
    git clone git@github.com:<your-username>/<repo>.git
    cd <repo>
    ```
2. Add upstream remote:
    ```
    git remote add upstream git@github.com:<org-or-upstream>/<repo>.git
    git fetch upstream
    ```
3. Create a feature branch from the latest main:
    ```
    git checkout -b feat/<short-description> upstream/main
    ```
4. Install dependencies and run the local build/test commands described in README:
    - Use the repo's package manager or build tool (e.g., npm/yarn/pip/mvn) to install.
    - Run the test suite and linter locally before opening a PR.

## Issue workflow
- Search existing issues before opening a new one.
- Use a clear title and describe steps to reproduce, expected vs actual behavior, environment, and logs.
- Tag issues with suggested labels (bug, enhancement, docs, question).
- If you plan to work on an issue, leave a comment stating intent and reference the issue in your PR.

## Branching and commits
- Branch naming:
  - feat/<short-description>
  - fix/<short-description>
  - docs/<short-description>
  - chore/<short-description>
- Commit messages:
  - Use a concise subject line (max ~72 chars) and an optional body.
  - Follow Conventional Commits where practical:
     ```
     feat(parser): add support for X
     fix(auth): handle expired tokens
     docs: update CONTRIBUTING.md
     ```
- Keep commits focused and atomic. Rebase and squash local commits before merging if requested.

## Pull request process
- Base your PR against the default branch (usually main). Keep PRs small and focused.
- PR title should summarize the change. In the description include:
  - Linked issue number (e.g., "Fixes #123")
  - Motivation and high-level design
  - Key changes and potential impact
  - How to test locally
- Add reviewers and relevant labels. Use templates if available.
- Address review comments promptly. Maintainers may request changes or ask for additional tests.
- Once approved and CI passes, a maintainer will merge. Do not merge your own PR unless explicitly allowed.

## Testing & CI

- Include tests for all new features and bug fixes where applicable. Aim for a mix of unit, integration, and end-to-end tests appropriate to the change.
- Run the project's full test suite and static checks locally before opening a PR. Use the repository's documented commands or scripts rather than ad-hoc commands.
- Test types and scope:
    - Unit tests: fast, isolated, deterministic, exercising single functions/components.
    - Integration tests: verify interactions between modules and external dependencies (use fixtures or test doubles as needed).
    - End-to-end / acceptance tests: validate user-facing flows in an environment that mirrors production.
    - Smoke tests: quick checks that a build is sane after major changes.
- Make tests deterministic and fast. Avoid reliance on timing, network flakiness, or shared global state. Use seeded randomness where applicable and document seeds in failures.
- Test data and secrets:
    - Use synthetic or fixture data; never commit secrets or real credentials.
    - Prefer mocks or local test doubles for external services. For integration tests that require real services, document setup steps.
- Local reproducibility:
    - Provide clear instructions in the README for running tests and any required environment setup (env vars, service emulators, containers).
    - If the project uses containers or VMs for tests, include commands or scripts to build and run them.
- CI expectations:
    - Ensure CI passes on your branch before requesting a review. CI should run the same suites described in the repository docs (unit, integration, linters, formatters, and any required checks).
    - If CI fails intermittently, report the failure in the PR with links to logs. Re-run or bisect to identify flakiness and add mitigations or tests to reproduce the issue.
    - When adding longer-running tests (e.g., performance, end-to-end), mark them clearly and consider configuring them to run on a scheduled basis or in a separate CI job to keep PR feedback fast.
- Test quality and coverage:
    - Write meaningful assertions and cover edge cases. Prefer clarity over trying to hit arbitrary coverage percentages.
    - Add tests that document expected behavior for future maintainers.
- Commit and PR guidance:
    - Include which tests you ran locally and any special steps in the PR description.
    - For code that touches public APIs or behavior, add or update tests that prevent regressions.
    - If introducing new test infrastructure or fixtures, provide a brief explanation and usage examples.
- Flakiness and debugging:
    - If a test is flaky, attempt to reproduce locally, isolate the cause, and either fix the test or add guards (retries with diminishing scope, increased timeouts, isolation).
    - Document any non-obvious test requirements and troubleshooting steps in the test docs or README.
- Performance and resource considerations:
    - Keep PR test runs fast; move heavy or long-running scenarios to separate pipelines.
    - Make tests parallelizable when safe, and ensure they can run in CI environments with limited resources.

Adopt these guidelines to keep test suites reliable, maintainable, and fast, improving the chance of quick review and merge.

## Code style & quality
- Follow the existing style in the repository. Use existing linters/formatters (Prettier, ESLint, Black, etc.).
- Avoid large refactors in the same PR as feature work. Separate concerns across PRs.
- Strive for clear function names, small functions, and reasonable comments for non-obvious logic.

## Documentation
- Update relevant docs and README sections when behavior or APIs change.
- Include usage examples, config flags, and expected outputs where applicable.
- For breaking changes, document migration steps.

## Releases & changelog
- Use semantic versioning (major.minor.patch).
- Record user-facing changes in the changelog. Follow the project's changelog format.
- For breaking changes, clearly document migration steps and rationale.

## Security & sensitive issues
- Do not disclose security vulnerabilities in public issues or PRs.
- Report security issues privately by contacting the maintainers via the repository's security policy or provided email.
- Do not include secrets (API keys, passwords, credentials) in commits. Use environment variables or secret stores.

## Communication
- Use issue comments and PR threads for technical discussion.
- For real-time or broader discussions, use the project's preferred channels (Slack, Discord, mailing list) if available.
- Be patient and constructive during reviews—maintainers are often volunteers with limited time.

Thank you for contributing. Your effort helps improve the project for everyone.