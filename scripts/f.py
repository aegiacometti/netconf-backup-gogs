import fortigate

ip_addr = '10.100.14.2'
api_token = 'pH0hGq7kwmchNs8Gzqys33bQtcdfGg'

if fortigate.config_download(ip_addr, api_token, 'backup20190215.conf'):
  print('Done!')
else:
  print('Error!!')

with open('backup20190215.conf', 'r') as f:
  f.readline()
'#config-version=FGTAWS-6.0.4-FW-build0231-190107:opmode=0:vdom=0:user=api-admin\n'
