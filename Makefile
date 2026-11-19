# Living-spec SDD commands. Requires only Python 3.10+ and git.
# Add your project's own targets (format, lint, typecheck, run) below and
# call them from `check`.

PY ?= python3
BASE ?= origin/main

.PHONY: check spec-check test test-tools test-project status next new-change close-change guard remove-example help

help:
	@echo "make check            spec check + all tests (what CI runs)"
	@echo "make spec-check       requirements, specs, changes, tasks, test markers"
	@echo "make test             tool tests + project tests"
	@echo "make status           open changes and their tasks"
	@echo "make next             tasks that are ready now"
	@echo "make new-change SLUG=add-tags CODE=TAGS TITLE=\"Add tags\""
	@echo "make close-change CHANGE=2026-11-18-add-tags"
	@echo "make guard BASE=origin/main"
	@echo "make remove-example   delete the bundled notes example"

check: spec-check test

spec-check:
	$(PY) tools/spec_check.py

test: test-tools test-project

test-tools:
	$(PY) -m unittest discover -s tools/tests -t .

test-project:
	@$(PY) -m unittest discover -s tests -t . || [ $$? -eq 5 ]  # 5 = no tests yet

status:
	$(PY) tools/task_status.py

next:
	$(PY) tools/task_status.py --next

new-change:
	$(PY) tools/new_change.py --slug "$(SLUG)" --code "$(CODE)" --title "$(TITLE)"

close-change:
	$(PY) tools/close_change.py "$(CHANGE)"

guard:
	$(PY) tools/guard.py --base "$(BASE)"

remove-example:
	$(PY) tools/remove_example.py
