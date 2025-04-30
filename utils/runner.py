import os
import sys
import traceback
from utils.logs_management import init_logs
from utils.rabbitmq_utils import define_payload, send_message_to_rabbitmq


def run_main(main_func):
    """
    Initializes the logger and executes the given main function.
    The log file is saved in the root ./log directory and named after the folder containing the main module.

    Arguments:
        main_func (callable): The main function to execute.
    """
    try:
        run_try_main(main_func)
    except Exception as e:
        common_exception_handler(e)


def run_try_main(main_func):
    """
    Retrieves the calling script's directory name to initialize the logger with a contextual name.
    Executes the given main function and prints start/end messages.

    Arguments:
        - main_func (callable): The main function to execute.
    """
    caller_path = sys.modules["__main__"].__file__
    caller_folder = os.path.basename(os.path.dirname(caller_path))
    log_file_name = f"{caller_folder}"
    init_logs(log_file_name)

    print("Starting job")
    main_func()
    print("Job completed successfully")


def common_exception_handler(e):
    """
    Handles an exception by printing and returning a concise traceback pointing to user code.
    Skips internal library stack frames to focus on the most relevant file in the project.

    Arguments:
        - e (Exception): The caught exception.

    Returns:
        - str: A concise traceback string pointing to the relevant source file.
    """
    tb = traceback.extract_tb(sys.exc_info()[2])
    user_trace = next(
        (
            frame
            for frame in reversed(tb)
            if ".venv" not in frame.filename and "site-packages" not in frame.filename
        ),
        tb[-1],
    )

    location = f"{user_trace.filename}:{user_trace.lineno} in {user_trace.name}"
    error_message = f"{type(e).__name__}: {e}"

    short_trace = f"{location}\n{error_message}"
    print(f"An error occurred:\n{short_trace}")
    return short_trace
