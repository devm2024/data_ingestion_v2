# Group Name: InsaneSprinters
# Group Members: Sri Santhosh Hari, Kunal Kotian, Devesh Maheshwari, Vinay Patlolla

import json
import sys
import os
import logging

LOG_FILE = './json_parse.log'
JSON_DIR = '/srv/runme/'


def read_json_files(prefix):
    '''
    Reads files starting with prefix in JSON_DIR and returns properly formatted json lines
    :param prefix: keyword used to subset files
    :return: formatted json lines
    '''
    json_lines = list()
    files = os.listdir(JSON_DIR)
    for f in files:
        if f.startswith(prefix):
            try:
                file_loc = os.path.join(JSON_DIR, f)
                fd = open(file_loc)
                for line in fd.readlines():
                    d = json.loads(line)
                    json_lines.append(d)
            except IOError:
                logging.error('Cannot open file: {}'.format(file_loc))
            except ValueError:
                logging.error('Malformed json in file: {}'.format(file_loc))

    logging.info('Successfully read {} json lines'.format(len(json_lines)))
    return json_lines


def json_parser(prefix, json_lines):
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

    output_file = os.path.join(JSON_DIR, '{}.txt'.format(prefix))

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


# Read input argument and execute parser function
if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    if len(sys.argv) != 2:
        print("Malformed python call. Correct call is 'python json_parser.py prefix'")
        sys.exit()
    prefix = sys.argv[1]
    json_lines = read_json_files(prefix)
    json_parser(prefix, json_lines)
