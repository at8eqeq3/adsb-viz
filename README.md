# ADSB visualization

## Requirements

* some ADSB receiver software capable to send data in SBS3 format. Tested with [dump1090-fa](https://github.com/flightaware/dump1090)
* [redis](https://redis.io) server
* python3 interpreter
* [redis-py](https://github.com/andymccurdy/redis-py)
* [ffmpeg](http://ffmpeg.org) to make videos from frames

## How to run

First of all, make sure your ADSB receiver is running and exposes it's data feed. For dump1090 it's `--net-sbs-port <ports>` option. Set appropriate values in `redis_feeder.py`.

Next, start redis server. Set connection details in both `redis_feeder.py` and `redis_plotter.py`.

Start `redis_feeder.py`. It will grab data from ADSB receiver and send to redis. I use `SETEX` command so points will disappear after some amount of time. You can tweak this value as you wish.

`mkdir plot` or whatever you want (don't forget to change the path in `redis_plotter.py`). Set your antenna location (to convert coordinates to pixels) and run `redis_plotter.py`. This will start to fill you destination directory fith frames.

`ffmpeg -y -thread_queue_size 4096 -r 30 -pattern_type glob -i "plot/*.png" -r 30 output.mp4` when you think there're enough frames. Feel free to change framerate (the `-r <num>` option) or play with output format.

## What's not perfect

* Coeffs for coords-to-pixels convertion are set by wild guess. This, for my setup, results in too wide picture with almost empty left side. Probably will be better to define a desired area in coords, create image based on this and just skip coords that don't fit.
* This also leads to `redis_plotter.py` failures when coords are out of guessed bounds. Probably solution for previous problem will solve this too.
* Time intervals are almost random and mostly depend on how long we receive data from redis. Would be better to use some sort of scheduler -- built into script or even `cron`.

