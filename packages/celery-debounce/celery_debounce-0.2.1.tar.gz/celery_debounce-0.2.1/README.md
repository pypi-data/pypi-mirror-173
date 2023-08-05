# Celery Debounce




Celery debounce without using cache.


How to create debounce task?
```
from celery_debounce.celery_debounce import DebouncedTask

@app.task(bind=True, base=DebouncedTask)
def testing_task(self, some_id):
    """
    how to call task?
    testing_task.debounce(some_id=1234)
    """
    print("from testing_task", some_id)

```

How to call the task?

```
testing_task.debounce(some_id=1234)
```
With countdown (By default it's 60 seconds):
```
testing_task.debounce(some_id=1234, countdown=10)
```

