# Project Agent Instructions

- After every change to project files, run the complete test suite with `python -m pytest` before continuing.
- If any file changes after a test run, run the complete test suite again.
- Do not consider a change complete until the tests pass. If tests cannot be run or fail, report that clearly and explain why.
- The test suite is configured in `pytest.ini` and covers the `tests/` directory.
- Foillow best practices on [how to build an integration](https://contributors.home-assistant.io/core/integrations/create/)
- Follow [translation guide](https://contributors.home-assistant.io/translate/guides/developers/)
- Ideally reuse provided [Home Assistant translation strings](https://github.com/home-assistant/core/blob/dev/homeassistant/strings.json)