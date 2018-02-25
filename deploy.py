# Group Name: InsaneSprinters
# Group Members: Sri Santhosh Hari, Kunal Kotian, Devesh Maheshwari, Vinay Patlolla

import paramiko

def deploy(key = 'key/test_key.pem', server_ip = None, prefix = None):
    '''
    key - ssh key to login into the server
    server_ip - ip address of the server
    prefix - prefix of the associated file
    '''
    # Create a client object
    client = paramiko.client.SSHClient()
    # Autoaddkey if not available
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    # Connect to the server
    try:
        client.connect(server_ip, pkey = paramiko.RSAKey.from_private_key_file(key), username='testtest')
    except:
        print('Connection error. Please check if your server is running and given credentials are valid.')
        return None
    print('Connected to server')
    
    # Delete folder before cloning
    stdin, stdout, stderr = client.exec_command('rm -rf data_ingestion_system')
    # Exeute command to clone repository
    print('Cloning repository')
    stdin, stdout, stderr = client.exec_command('git clone https://github.com/vinnsvinay/data_ingestion_system')
    print('Configuring cronjob')
    # Remove existing cronjobs
    stdin, stdout, stderr = client.exec_command('crontab -r')
    # Adding a crontab
    stdin, stdout, stderr = client.exec_command('crontab -l > json_cron')
    cron_command = 'echo "*/5 * * * * python /home/testtest/data_ingestion_system/json_parser.py {}" \
                            >> json_cron'.format(prefix)
    stdin, stdout, stderr = client.exec_command(cron_command)
    stdin, stdout, stderr = client.exec_command('crontab json_cron')
    print('Running cronjob')

    return None