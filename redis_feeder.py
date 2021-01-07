import socket
import redis

r = redis.Redis(host='localhost', port=6379, db=0)


sock = socket.socket()
sf = sock.makefile()
sock.connect(('192.168.249.26', 30003))
while(True):
  fields = sf.readline().split(',')
  if(fields[0] == 'MSG' and fields[1] == '3'):
    if(fields[14].strip != '' and fields[15].strip != '' and fields[11].strip != ''):
      coords = ','.join([fields[14], fields[15], fields[11]])
      r.setex(coords, 3600, coords)
  
