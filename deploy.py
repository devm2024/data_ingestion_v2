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
    stdin, stdout, stderr = client.exec_command('rm -rf data_ingestion_v2')
    # Exeute command to clone repository
    print('Cloning repository')
    stdin, stdout, stderr = client.exec_command('git clone https://github.com/devm2024/data_ingestion_v2.git')
    print('Running the script')
    # Remove existing cronjobs
    stdin, stdout, stderr = client.exec_command('cd data_ingestion_v2')
    
    stdin, stdout, stderr = client.exec_command('python data_server.py {}'.format(prefix))
    
    print('Script Running')

    return None