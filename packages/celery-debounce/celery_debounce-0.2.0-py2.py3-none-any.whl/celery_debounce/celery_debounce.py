import importlib
import os

import celery
from celery import shared_task

# default countdown is 60 sec, it can be also override from task.debounce
DEBOUNCE_COUNTDOWN = os.environ.get('DEBOUNCE_COUNTDOWN', 60)


@shared_task
def task_debounce_check(task_to_call: str, task_args: list, task_kwargs: dict):
    """
    Check if this task is scheduled again, if so, cancel it.
    """
    # Get the list of scheduled tasks
    scheduled_tasks = celery.current_app.control.inspect().scheduled()
    # Check if the task exists in the scheduled tasks with same args, kwargs and name
    # If you have cache backend then it can also be done using key and counts
    if scheduled_tasks:
        for key, val in scheduled_tasks.items():
            for task in val:
                if (
                    task["request"]["args"][1] == task_args
                    and task["request"]["args"][2].get("kwargs")
                    == task_kwargs.get("kwargs")
                    and task["request"]["args"][0] == task_to_call
                ):
                    return False

    # This will be the last call
    mod_name, func_name = task_to_call.rsplit(".", 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    func.delay(*task_args, **task_kwargs)


class DebouncedTask(celery.Task):
    def debounce(self, *args, **kwargs):
        """
        Debounce the task until given countdown is over.
        """
        task_debounce_check.apply_async(
            (self.name, args, kwargs),
            countdown=kwargs.pop("countdown", DEBOUNCE_COUNTDOWN),
        )
