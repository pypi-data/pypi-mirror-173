#!/usr/bin/env python
# coding: utf-8

import queue
import time
import threading
import json
import traceback
import intelliw.utils.message as message
from intelliw.utils.util import get_json_encoder
from intelliw.utils.logger import _get_framework_logger
from intelliw.config import config

logger = _get_framework_logger()


class Worker(threading.Thread):
    def __init__(self, work_queue, reporter=None, interval=6):
        threading.Thread.__init__(self)
        self.reporter = reporter
        self.queue = work_queue
        self.interval = interval
        self.start()

    def run(self):
        oldtime = int(time.time())
        while True:
            try:
                if int(time.time()) - oldtime > self.interval:
                    msg = self.pack()
                    oldtime = int(time.time())
                    if self.reporter is not None:
                        self.reporter.report(
                            message.CommonResponse(200, "inferstatus", '', json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)))
                else:
                    time.sleep(10)
            except:
                print(traceback.format_exc())
                pass


class Recorder:
    def __init__(self, reporter=None, not_delay=True):
        self.not_delay = not_delay
        self.duplicate = set()
        self.queue = queue.Queue()
        self.reporter = reporter

    def _pack(self):
        tmp = []
        while not self.queue.empty():
            item = self.queue.get()
            tmp.append(item)
        return tmp

    def report(self):
        try:
            if not self.queue.empty():
                msg = self._pack()
                if self.reporter is not None:
                    self.reporter.report(
                        message.CommonResponse(200, "inferstatus", '', json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)))
        except:
            logger.error(traceback.format_exc())

    def record(self, msg):
        if msg in self.duplicate:
            return

        self.duplicate.add(msg)
        if self.reporter is not None:
            if not self.queue.full():
                self.queue.put(msg)
            if self.not_delay:
                self.report()

    def record_infer_status(self, rid, issuccess, starttime, endtime, msg=''):
        if self.reporter is not None:
            if not self.queue.full():
                self.queue.put({
                    "id": rid,
                    "issuccess": issuccess,
                    "starttime": starttime,
                    "endtime": endtime,
                    "message": msg
                })
            if self.not_delay:
                self.report_infer()

    def report_infer(self):
        try:
            if not self.queue.empty():
                msg = self._pack()
                out_msg = [
                    {
                        'status': 'start',
                        'inferid': config.INFER_ID,
                        'instanceid': config.INSTANCE_ID,
                        'inferTaskStatus': msg
                    }
                ]
                json_msg = message.CommonResponse(200, "inferstatus", '', json.dumps(out_msg, cls=get_json_encoder(), ensure_ascii=False))
                if self.reporter is not None:
                    self.reporter.report(json_msg, False)
        except:
            logger.error(traceback.format_exc())
