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
from logging.handlers import TimedRotatingFileHandler
app = Flask(__name__) #create the Flask app
from my_handler import MyTimedRotatingFileHandler
LOG_FILE='/srv/runme/prefix/Raw.txt'
#LOG_FILE='Raw.txt'

        
def create_timed_rotating_log(path):
    """
    Returns the Timed Rotating file handler
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
 
    handler = MyTimedRotatingFileHandler(path,
                                       when="s",
                                       interval=10,
                                       backupCount=0)
    
    logger.addHandler(handler)
    return logger

logger= create_timed_rotating_log(LOG_FILE)

        
@app.route('/submit',methods = ['POST'])
def process():
    data = request.data
    logger.info(data)
    print(data)
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

app.run(host='0.0.0.0', port=5000, debug=True)
    