import open3d as o3d
import numpy as np
import copy
import redis
import time

RADAR_COORDS = [55.83871, 37.18298]



r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_points(r):
  rpts = []
  for key in r.scan_iter():
    try:
      data = r.get(key).split(',')
      cdata = []
      cdata.append(float(data[1]) - RADAR_COORDS[1])
      cdata.append(float(data[0]) - RADAR_COORDS[0])
      cdata.append(float(data[2]) / 20000.0)
      rpts.append(cdata)
    except ValueError as e:
      pass
    except AttributeError as e:
      pass
  pts = np.array(rpts)
  pcd = o3d.geometry.PointCloud()
  pcd.points = o3d.utility.Vector3dVector(pts)
  return pcd

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
points = get_points(r)
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.get_render_option().load_from_json('ro.json')

vc = vis.get_view_control()

vis.add_geometry(points)
print(vc)
i = 0
save_image = False

while(True):
  print(i)
  p = get_points(r)
  print(p)
  vis.clear_geometries()
  vis.add_geometry(p)
  vis.poll_events()
  vis.update_renderer()
  vis.run
  if save_image:
    vis.capture_screen_image()
  i+=1
  time.sleep(1)

vis.destroy_window()
