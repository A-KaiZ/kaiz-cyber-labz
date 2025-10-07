# Contributing to Cyber Lab Foundry

Thanks for taking the time to contribute! We welcome improvements that enhance
learning, safety, or automation.

## Branch strategy

* Use feature branches prefixed with your GitHub handle, e.g. `feature/jdoe-sql-hardening`.
* Submit pull requests against `main`.
* Keep commits focused and include meaningful messages.

## Development workflow

1. Fork and clone the repository.
2. Install [pre-commit](https://pre-commit.com/) and run `pre-commit install`.
3. Use the devcontainer (`.devcontainer/devcontainer.json`) or run locally with Python 3.11.
4. Run `make up` to launch the lab, then execute tests with `pytest`.
5. Document your changes in the README and docs as appropriate.

## Testing checklist

* `make up` (ensure services build)
* `pytest`
* `pre-commit run --all-files`
* `make detect` (confirm dashboard import succeeds)

## Reporting issues

Open GitHub issues with detailed reproduction steps, expected behavior, and any
screenshots or logs. For sensitive security issues, follow [`SECURITY.md`](SECURITY.md).
