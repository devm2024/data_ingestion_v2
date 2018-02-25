#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 19:23:32 2018

@author: deveshmaheshwari
"""

import logging
import glob
import time
import os
from threading import Thread
from flask import Flask, request
import json
app = Flask(__name__) #create the Flask app

read_files=[]
 
from logging.handlers import TimedRotatingFileHandler


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when, interval, backupCount, encoding=None, delay=False, utc=False):
        TimedRotatingFileHandler.__init__(self, filename, when, interval,backupCount, encoding, delay, utc)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dfn = self.baseFilename + ".old"
        if os.path.exists(dfn):
            os.remove(dfn)
        # Issue 18940: A file may not have been created if delay is True.
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        
        self.rolloverAt = newRolloverAt
        process_file(dfn)
        
        
def create_timed_rotating_log(path):
    """
    Returns the Timed Rotating file handler
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
 
    handler = MyTimedRotatingFileHandler(path,
                                       when="s",
                                       interval=15,
                                       backupCount=0)
    logger.addHandler(handler)
    return logger

def process_file(file_to_read):
    json_list=[]
    with open(file_to_read, 'r') as f:
        json_list = f.readlines()
    os.remove(file_to_read)
    for i in json_list:
            print i
        # call json_parser


log_file = "Raw.txt"
logger= create_timed_rotating_log(log_file)

        
@app.route('/submit',methods = ['POST'])
def process():
    data = request.data
    logger.info(data)
    return data

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    exit()
    #background_thread.deamon()
    return 'Server shutting down...'

app.run(host='0.0.0.0', port=5001, debug=True)
    