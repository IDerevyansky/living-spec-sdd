"""`awaits` marker for Python tests (unittest and pytest).

A test written before its implementation carries `@awaits("T-CODE-NN")`,
naming the [IMPL] task that will make it pass.

- While that task's box is not ticked, a failing test is reported as skipped
  ("awaits T-CODE-NN"), so the test can be merged before the code exists.
- Once the box is ticked, the test runs normally and must pass.

Never remove or edit the marker: ticking the box is what makes the test
blocking.
"""

from __future__ import annotations

import functools
import inspect
import unittest
from pathlib import Path

from .core import find_root, load_project

_DONE_CACHE: dict[Path, set[str]] = {}


def _done_tasks(root: Path) -> set[str]:
    if root not in _DONE_CACHE:
        project = load_project(root)
        _DONE_CACHE[root] = {task.id for task in project.tasks if task.done}
    return _DONE_CACHE[root]


def is_done(task_id: str, root: Path | None = None) -> bool:
    base = root or find_root(Path(__file__).parent)
    return task_id in _done_tasks(base)


def awaits(task_id: str, root: Path | None = None):
    """Mark a test as written for the [IMPL] task `task_id`.

    `root` is only for testing this helper; normal tests omit it.
    """

    def decorate(test):
        if inspect.isclass(test):
            raise TypeError("@awaits goes on test functions or methods, not classes")

        @functools.wraps(test)
        def wrapper(*args, **kwargs):
            if is_done(task_id, root):
                return test(*args, **kwargs)
            try:
                test(*args, **kwargs)
            except unittest.SkipTest:
                raise
            except Exception as error:  # any failure means "not built yet"
                raise unittest.SkipTest(f"awaits {task_id} (not done yet): {type(error).__name__}") from error
            return None

        setattr(wrapper, "__awaits__", task_id)
        return wrapper

    return decorate
