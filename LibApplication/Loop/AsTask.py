from LibApplication.Loop.Task import Task


def AsTask(target_loop):
    def decorator(func):
        def wrapper(*args):
        
            # Create a task
            task = Task(func, *args)

            # Return the observable
            return target_loop.add(task)

        # Return wrapper function
        return wrapper

    # Return the actual decorator
    return decorator
