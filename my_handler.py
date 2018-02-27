#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:25:38 2018

@author: deveshmaheshwari
"""
import glob
import json
from logging.handlers import TimedRotatingFileHandler
from threading import Thread
from json_parser import parser
import os


def process_file(file_name):
    # Get file list
    json_lines = list()
    file_list =glob.glob(file_name+'*')
    file_list = [x for x in file_list if x!= file_name]
    file_list  = sorted(file_list, reverse=True)
    if file_list>0:
        file_to_read = file_list[0]
        print('ReadingFile', file_to_read)
        try:
            fd = open(file_to_read)
            for line in fd.readlines():
                d = json.loads(line.strip())
                json_lines.append(d)
            os.remove(file_to_read)
        except IOError:
            logging.error('Unable to open file: {}'.format(file_to_read))
        except ValueError:
            logging.error('Malformed json in file: {}'.format(file_to_read))
            
        parser(json_lines)
    
    
    
        # call json_parser
        
class MyTimedRotatingFileHandler(TimedRotatingFileHandler):

    def doRollover(self):
        print('rollingover')
        super(MyTimedRotatingFileHandler, self).doRollover()
        process_thread =Thread(target=process_file, args={self.baseFilename})
        process_thread.start()
        process_thread.stop =True

