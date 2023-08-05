"""
自定义线程类
"""
import threading

from smssdk.utils.logger import Logger

logger = Logger('mythread.py')
threadLock = threading.Lock()


class Thread(threading.Thread):
    def __init__(self, target=None, args=(), kwargs=None):
        super().__init__()
        if kwargs is None:
            kwargs = {}
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.target(*self.args, **self.kwargs)
