import sys
import os
import re

import osceleton_trac
import score_trac
import video_timestamp

path = sys.argv[1]

for f in os.listdir(path):
  pathfile = path + "/" + f

  pattern = re.compile("^\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d-motion\.txt$")
  match = re.search(pattern, f)
  if match:
    print(pathfile)
    score_trac.run(path, f)
    print()

  pattern = re.compile("^points-MSK2-\d+\.?\d+\.csv$")
  match = re.search(pattern, f)
  if match:
    print(pathfile)
    osceleton_trac.run(path, f)
    print()

  pattern = re.compile("^.+\.(mov|MOV|mp4|MP4)$")
  match = re.search(pattern, f)
  if match:
    print(pathfile)
    video_timestamp.run(path, f)
    print()
