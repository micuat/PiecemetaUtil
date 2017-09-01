# https://stackoverflow.com/questions/15041103/get-total-length-of-videos-in-a-particular-directory-in-python/15043503#15043503
import time
import calendar
import os

owd = os.getcwd()

os.chdir(os.environ["PROGRAMFILES"] + "\\mediainfo")
from MediaInfoDLL3 import MediaInfo, Stream
os.chdir(owd)

def run(path, filename):

  MI = MediaInfo()

  MI.Open(path + '/' + filename)
  duration_string = MI.Get(Stream.General, 0, "Encoded_Date")
  # print(duration_string)

  try:
    pattern = 'UTC %Y-%m-%d %H:%M:%S'
    epoch = int(calendar.timegm(time.strptime(duration_string, pattern)))
    print(epoch)
  except ValueError:
    print("{} ain't no media file!".format(filename))

  MI.Close()
