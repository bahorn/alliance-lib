import signal
import contextlib
import joblib
import numpy as np


@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress """
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


# https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call
class TimeoutException(Exception):
    pass


@contextlib.contextmanager
def timelimit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(int(seconds))
    try:
        yield
    finally:
        signal.alarm(0)


def gen_seed(values):
    state = list(map(lambda x: abs(hash(x)) % (2**32 - 1), values))
    state = np.random.RandomState(state)
    return state.randint(0, 2**32 - 1)
