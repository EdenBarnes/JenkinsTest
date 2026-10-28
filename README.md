# Jenkins + Python Multibranch Pipeline Example

A tiny Python package (`textutils`) with tests, linting, packaging, and a
`Jenkinsfile` designed for a Jenkins **Multibranch Pipeline**.

## Layout

```
.
├── Jenkinsfile            # pipeline definition (runs per branch / PR)
├── pyproject.toml         # package + pytest config
├── requirements-dev.txt   # pytest, pytest-cov, flake8, build
├── .flake8
├── src/textutils/         # the application code
└── tests/                 # unit tests
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt && pip install -e .
flake8 src tests
pytest --cov=textutils
python -m build
```

## What the pipeline does

| Stage         | Runs on        | Purpose                                   |
|---------------|----------------|-------------------------------------------|
| Setup         | all branches   | Create venv, install dependencies         |
| Lint          | all branches   | flake8 (parallel with tests)              |
| Unit tests    | all branches   | pytest, JUnit + coverage reports          |
| Build package | all branches   | Build sdist and wheel into `dist/`        |
| PR checks     | pull requests  | Uses `CHANGE_ID`, `CHANGE_TARGET`         |
| Deploy        | `main` only    | Placeholder deploy / publish step         |

## Jenkins setup

Prerequisites: Jenkins with the **Pipeline**, **Git**, **Docker Pipeline**,
and **JUnit** plugins, plus Docker on the agent. For GitHub, also install
**GitHub Branch Source**.

1. Push this repo to GitHub/GitLab/Bitbucket.
2. In Jenkins: **New Item -> Multibranch Pipeline**.
3. **Branch Sources -> Add source** -> choose your provider, add credentials,
   and enter the repo URL.
4. **Build Configuration**: Mode = *by Jenkinsfile*, Script Path = `Jenkinsfile`.
5. Save. Jenkins scans the repo and creates a job per branch and PR.
6. Add a webhook so pushes trigger builds:
   - GitHub: `https://<jenkins>/github-webhook/`
   - Or set **Scan Multibranch Pipeline Triggers** to e.g. every 5 minutes.

## Try it

```bash
git checkout -b feature/add-reverse
# edit code, commit, push
git push -u origin feature/add-reverse
```

Jenkins discovers the new branch, builds it, and skips the Deploy stage.
Open a PR and you also get the PR checks stage. Merge to `main` and Deploy runs.

Break a test or add a lint error on a branch to see the build fail and the
JUnit report show the failure.

## Notes

- The Docker agent uses `-u root:root` to keep the example simple. For
  production, use a non-root user or a custom image with your tools preinstalled.
- No Docker on your agents? Change `agent { docker {...} }` to `agent any`
  and make sure Python 3 with `venv` is installed.
