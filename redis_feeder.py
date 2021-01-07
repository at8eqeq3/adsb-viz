import redis
import socket

# redis server
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# ADSB feeder
FEEDER_HOST = '192.168.249.26'
FEEDER_PORT = 30003
# TTL of records, in seconds
EXPIRATION = 1200

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


sock = socket.socket()
sf = sock.makefile()
sock.connect((FEEDER_HOST, FEEDER_PORT))
while(True):
  fields = sf.readline().split(',')
  if(fields[0] == 'MSG' and fields[1] == '3'):
    if(fields[14].strip != '' and fields[15].strip != '' and fields[11].strip != ''):
      coords = ','.join([fields[14], fields[15], fields[11]])
      r.setex(coords, EXPIRATION, '')
  
