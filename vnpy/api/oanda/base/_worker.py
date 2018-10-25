import logging

from vnpy.trader.utils import Logger

from ..ioloop import BackroundEventLoopProxy

class AsyncApiWorker(Logger):
    def __init__(self, api):
        self._api = api
        self._ioloop = api.ioloop
        self._proxy = BackroundEventLoopProxy(self._ioloop)

    @property
    def api(self):
        return self._api

    @property
    def ioloop(self):
        return self._ioloop

    def is_running(self):
        return self._api.is_running()

    def start(self):
        pass

    def close(self):
        pass

    def on_task_finished(self, task):
        """Gather info when task halt unexpectedly"""
        if task.cancelled():
            return 
        exception = task.exception()
        if exception:
            self._api.on_error(exception)

    def create_task(self, coro):
        task = self._proxy.create_task_threadsafe(coro)
        task.add_done_callback(self.on_task_finished)
        return task

    def cancel_task(self, task):
        return self._proxy.cancel_task_threadsafe(task)

    def log(self, msg, level=logging.INFO):
        return self._api.log(msg, level=level)
