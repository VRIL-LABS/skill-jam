# Contributing to skill-jam

Thanks for your interest in improving `skill-jam`. Contributions help keep the repository useful for developers, researchers, and AI builders working with agent skills.

This project follows the standard GitHub contributor workflow: keep changes focused, use a clear pull request description, and make it easy for maintainers to review your work.

## Ways to contribute

You can help by:

- reporting bugs or broken skill instructions
- improving documentation and examples
- adding or refining skills in `skills/` or `featured-skills/`
- suggesting a new submodule or reference collection
- improving project tooling, structure, or metadata

## Before you start

1. Fork the repository and create a feature branch from `main`.
2. Keep each change scoped to a single concern.
3. Sync your fork with the latest upstream changes before opening a pull request.
4. If your work is still in progress, open a draft pull request and update it as you go.

## Recommended workflow

```bash
git checkout main
git pull upstream main
git checkout -b fix/my-change
# make updates
# validate as needed
git add .
git commit -m "fix: describe the change"
git push origin fix/my-change
```

Use clear branch names such as:

- `fix/readme-badge-counts`
- `feat/add-new-skill`
- `docs/improve-contributing-guide`

## Pull request expectations

When you open a pull request:

- write a descriptive title and summary
- explain the reason for the change and the impact
- keep the diff focused and easy to review
- link the related issue if one exists
- include validation notes or examples of how you checked the change

For upstream repository changes, maintainers may choose the merge strategy that best fits the repo. Keep the PR ready for review and respond to comments in a timely, constructive way.

## Skill contributions

If you are adding a skill, follow the repository conventions in [`docs/contributing.md`](docs/contributing.md) and the skill format described in the project README.

At minimum, a skill should:

- have a clear, single responsibility
- use a descriptive kebab-case directory name
- include a `SKILL.md` file with the required sections
- provide example input/output details and dependencies
- be broadly useful and not narrow to a single niche use case

## Documentation updates

Documentation fixes are welcome and often the easiest way to contribute. If you update README files, examples, or contributor guidance, keep the content clear, accurate, and consistent with the rest of the repo.

## Reporting issues

Open a GitHub issue with:

- a clear title
- the expected behavior versus the current behavior
- reproduction steps when relevant
- environment details such as OS, Node version, or tool version
- the affected skill or file path

## Code of conduct

Please be respectful, constructive, and inclusive. We value thoughtful collaboration and encourage contributors to engage kindly and professionally.

For more project-specific guidance, see:

- [`README.md`](README.md)
- [`docs/contributing.md`](docs/contributing.md)
- [GitHub Docs: Setting guidelines for repository contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)
- [GitHub Docs: About pull requests](https://docs.github.com/en/pull-requests)
