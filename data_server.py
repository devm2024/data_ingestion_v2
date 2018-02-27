#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 19:23:32 2018

@author: deveshmaheshwari
"""

import logging
import glob
import sys
import json
from logging.handlers import TimedRotatingFileHandler
from threading import Thread
from json_parser import parser
import os
import time
from threading import Thread
from flask import Flask, request
import json
from logging.handlers import TimedRotatingFileHandler
app = Flask(__name__) #create the Flask app
LOG_FILE='Raw.txt'
OUT_FILE_NAME = 'proc.txt'
JSON_DIR = '/Users/deveshmaheshwari/Documents/Bigdatabusiness_stategy/dataingest_v2/datav2'
given_prefix='prefix'

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
    

        
class MyTimedRotatingFileHandler(TimedRotatingFileHandler):

    def doRollover(self):
        print('rollingover')
        super(MyTimedRotatingFileHandler, self).doRollover()
        process_thread =Thread(target=process_file, args={self.baseFilename})
        process_thread.start()
        process_thread.stop =True
        

def parser(json_lines):
    '''
    Parses through each line and writes name and age to /srv/runme/prefix.txt file
    :param json_lines: List of properly formatted json lines
    :return: None
    '''
    output = list()

    # Parse through individual dictionaries and append relevant lines to output
    for d in json_lines:
        try:
            name = str(d.get('name', ''))
            age = int(d['prop'].get('age', ''))
            # Checks if name is not empty and age is a positive number
            # Also checks if name and age are present in correct location
            if name != '' and age >= 0 and (u'age' not in d.keys()) and \
                    (u'name' not in d['prop'].keys()):
                output.append((name, age))
        except KeyError:
            logging.error(
                'Failed to parse dictionary: {}. Key not present in dictionary'.format(d))
        except ValueError:
            logging.error('Malformed json in dictionary: {}'.format(d))

    out_folder = os.path.join(JSON_DIR, given_prefix)
    output_file = os.path.join(out_folder, OUT_FILE_NAME)

    print(output)
    # Remove output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)
        logging.info('Removed output file')

    with open(output_file, 'w+') as f:
        for name, age in output:
            entry = name + '\t' + str(age) + '\n'
            f.write(entry)
        logging.info('Parsed all files succesfully')
    return None
        

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


        
@app.route('/submit',methods = ['POST'])
def process():
    data = request.data
    logger.info(data)
    return data



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Malformed python call. Correct call is 'python data_server.py prefix'")
        sys.exit()
    given_prefix = sys.argv[1]
    log_loc = os.path.join(JSON_DIR, given_prefix)
    log_loc = os.path.join(log_loc, LOG_FILE)
    logger= create_timed_rotating_log(log_loc)
    app.run(host='0.0.0.0', port=5000, debug=True)
    