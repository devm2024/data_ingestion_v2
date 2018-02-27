# Group Name: InsaneSprinters
# Group Members: Sri Santhosh Hari, Kunal Kotian, Devesh Maheshwari, Vinay Patlolla

import json
import sys
import os
import logging

LOG_FILE = './json_parse.log'
JSON_DIR = '/srv/runme/prefix/'
PREFIX ='proc.txt'

def json_parser(json_lines):
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

    #output_file = os.path.join(JSON_DIR, '{}.txt'.format(PREFIX))
    output_file = PREFIX

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
