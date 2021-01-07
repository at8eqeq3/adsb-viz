import colorsys
import redis
import time
from PIL import Image

# redis server
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# crop parameters
RADAR_COORDS = [55.83871, 37.18298]
COEFS        = [300, 300, 40000]
SIZE         = [3000, 1000]


r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

i = 0
while(True):
  im = Image.new('RGB', SIZE, color=(10, 0, 20))
  for key in r.scan_iter():
    try:
      data = key.split(',')
      cdata = []
      cdata.append(int(((float(data[1]) - RADAR_COORDS[1]) * COEFS[0]) + SIZE[0]/2))
      cdata.append(int(((float(data[0]) - RADAR_COORDS[0]) * COEFS[1]) + SIZE[1]/2))
      cdata.append(float(data[2]) / COEFS[2])
      colors = colorsys.hls_to_rgb(cdata[2], 0.6, 1.0)
      im.putpixel((int(cdata[0]), int(cdata[1])), (int(colors[0] * 255), int(colors[1] * 255), int(colors[2] * 255)))
    except ValueError as e:
      pass
    except AttributeError as e:
      pass
    except IndexError as e:
      pass
  im = im.transpose(Image.FLIP_TOP_BOTTOM)
  im.save("plot/frame_%06d.png" % i)
  i += 1
  time.sleep(1)
