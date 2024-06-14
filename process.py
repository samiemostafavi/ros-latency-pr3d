import paramiko
import re

# SSH configuration
server1 = {'hostname': '130.237.11.122', 'username': 'root', 'password': 'expeca'}
server2 = {'hostname': '130.237.11.123', 'username': 'root', 'password': 'expeca'}
log_path = '/root/logs.txt'

def download_file(server, remote_path, local_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server['hostname'], username=server['username'], password=server['password'])
    
    sftp = ssh.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()
    ssh.close()

def parse_log(file_path):
    pattern = re.compile(r"\[INFO\] \[(\d+\.\d+)\]: (\d+)")
    data = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                timestamp = float(match.group(1))
                seq_id = int(match.group(2))
                data[seq_id] = timestamp
                
    return data

def compute_delays(data1, data2):
    delays = []
    for seq_id in data1:
        if seq_id in data2:
            delay = abs(data1[seq_id] - data2[seq_id])
            delays.append((seq_id, delay))
    return delays

# Download log files from both servers
download_file(server1, log_path, 'logs_server1.txt')
download_file(server2, log_path, 'logs_server2.txt')

# Parse log files to extract timestamps and sequence IDs
data1 = parse_log('logs_server1.txt')
data2 = parse_log('logs_server2.txt')

# Compute delays
delays = compute_delays(data1, data2)

# Print delays
for seq_id, delay in delays:
    print(f"{delay:.9f}")
