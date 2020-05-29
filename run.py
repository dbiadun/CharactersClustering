import sys

from Runner import Runner

if len(sys.argv) < 2:
    print("Please pass a path to a file containing image paths list")
else:
    Runner.run('image_paths')
