from pssh.clients import ParallelSSHClient
#,'157.253.205.7'
#hosts = ['192.168.0.16']
hosts = ['172.23.66.56',
         '172.23.66.57',
         '172.23.66.58',
         '172.23.66.59',
         '172.23.66.60',
         '172.23.66.61',
         '172.23.66.62',
         '172.23.66.63',
         '172.23.66.64',
         '172.23.66.65',
         ]


#'git clone https://github.com/JuanCamiloUsecheRodriguez/UDP-FT'
client = ParallelSSHClient(hosts, user='isis', password='labredesML340')
output = client.run_command('cd TCPFileTransfer && ls')
for host, host_output in output.items():
    for line in host_output.stdout:
        print("Host [%s] - %s" % (host, line))