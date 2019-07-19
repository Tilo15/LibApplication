from LibApplication.Loop.Task import Task


def AsTask(target_loop):
    def decorator(func):
        def wrapper(*args, **kwargs):
        
            # Create a task
            task = Task(func, *args, **kwargs)

            # Return the observable
            return target_loop.add(task)

        # Return wrapper function
        return wrapper

    # Return the actual decorator
    return decorator
