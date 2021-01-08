import colorsys
import redis
import threading
import time
import schedule
from PIL import Image

# redis server
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# crop parameters
RADAR_COORDS = [55.83871, 37.18298] # not used but probably interesting
BBOX_COORDS  = [54.96787, 35.85686, 56.85398, 40.53386]
XY_COEFF     = 1.76
SIZE_DEGREES = [(BBOX_COORDS[2] - BBOX_COORDS[0]) * XY_COEFF, BBOX_COORDS[3] - BBOX_COORDS[1]]
CENTER       = [(BBOX_COORDS[0] + BBOX_COORDS[2]) / 2, (BBOX_COORDS[1] + BBOX_COORDS[3]) / 2]
COEFS        = [500, 500, 40000]
SIZE_PIXELS  = [int(SIZE_DEGREES[1] * COEFS[1]), int(SIZE_DEGREES[0] * COEFS[0])]
BGCOLOR      = (10, 0, 20)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

cntr = 0

def plot():
  im = Image.new('RGB', SIZE_PIXELS, color=BGCOLOR)
  for key in r.scan_iter():
    try:
      data = key.split(',')
      cdata = []
      cdata.append(int(((float(data[1]) - CENTER[1]) + SIZE_DEGREES[1]/2) * COEFS[1]))
      cdata.append(int(((float(data[0]) - CENTER[0]) + SIZE_DEGREES[0]/2) * COEFS[0]))
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
  im.save("plot/frame_%06d.png" % cntr)

def run_threaded(job_func):
  job_thread = threading.Thread(target=job_func)
  job_thread.start()

schedule.every(2).seconds.do(run_threaded, plot)

while(True):
  schedule.run_pending()
  cntr += 1
  time.sleep(2)