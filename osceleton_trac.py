import csv
import datetime
import sys
import pandas as pd

def run(path, filename):
  joints = {}

  with open(path + '/' + filename, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    first = True
    for row in csvreader:
      if row[0] == 'Joint' and row[1].isdigit() and len(row) == 9:
        user_id = row[2]
        joint = int(row[3]) - 1
        x = row[4]
        y = row[5]
        z = row[6]
        timestamp = str(int(float(row[8])))
        if first:
          first = False
          print(float(timestamp) * 0.001)

        if timestamp not in joints:
          joints[timestamp] = {}
        if user_id not in joints[timestamp]:
          joints[timestamp][user_id] = []

        while len(joints[timestamp][user_id]) < 24:
          joints[timestamp][user_id].append({'x': float('nan'), 'y': float('nan'), 'z': float('nan')})

        joints[timestamp][user_id][joint]['x'] = x
        joints[timestamp][user_id][joint]['y'] = y
        joints[timestamp][user_id][joint]['z'] = z

  tempfilename = 'temp-' + filename
  with open(path + '/' + tempfilename, 'w', newline='') as csvfile:
    csvfile.write("Time	X1	Y1	Z1	X2	Y2	Z2	X3	Y3	Z3	X4	Y4	Z4	X5	Y5	Z5	X6	Y6	Z6	X7	Y7	Z7	X8	Y8	Z8	X9	Y9	Z9	X10	Y10	Z10	X11	Y11	Z11	X12	Y12	Z12	X13	Y13	Z13	X14	Y14	Z14	X15	Y15	Z15	X16	Y16	Z16	X17	Y17	Z17	X18	Y18	Z18	X19	Y19	Z19	X20	Y20	Z20	X21	Y21	Z21	X22	Y22	Z22	X23	Y23	Z23	X24	Y24	Z24\n")
    csvwriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for timestamp in joints:
      row = []
      row.append(timestamp)
      # find the closest user to the camera
      torso_z = {}
      for user_id in joints[timestamp]:
        torso_z[user_id] = joints[timestamp][user_id][2]['z']
      closest_user_id = min(torso_z, key=torso_z.get)

      for data in joints[timestamp][closest_user_id]:
        row.append(data['x'])
        row.append(data['y'])
        row.append(data['z'])
      csvwriter.writerow(row)

  finalfilename = 'final-' + filename
  # https://stackoverflow.com/questions/34883101/pandas-converting-row-with-unix-timestamp-in-milliseconds-to-datetime
  convert = lambda x: datetime.datetime.fromtimestamp(float(x) / 1e3)
  df = pd.read_csv(path + '/' + tempfilename, sep='\t', index_col=0, date_parser=convert)
  # drop last row since it is likely corrupted
  df = df[:-1]

  with open(path + '/' + finalfilename, 'w', newline='') as csvfile:
    csvfile.write('''PathFileType	4	(X/Y/Z)	%s
  DataRate	CameraRate	NumFrames	NumMarkers	Units	OrigDataRate	OrigDataStartFrame	OrigNumFrames
  30.00	30.00	      %d	24	mm	30.00	1	      %d
  Frame#	Time	Head			SpineShoulder			SpineMid			SpineBase			CollarRight			ShoulderRight			ElbowRight			WristRight			HandRight			FingerRight			CollarLeft			ShoulderLeft			ElbowLeft			WristLeft			HandLeft			FingerLeft			HipRight			KneeRight			AnkleRight			FootRight			HipLeft			KneeLeft			AnkleLeft			FootLeft
      X1	Y1	Z1	X2	Y2	Z2	X3	Y3	Z3	X4	Y4	Z4	X5	Y5	Z5	X6	Y6	Z6	X7	Y7	Z7	X8	Y8	Z8	X9	Y9	Z9	X10	Y10	Z10	X11	Y11	Z11	X12	Y12	Z12	X13	Y13	Z13	X14	Y14	Z14	X15	Y15	Z15	X16	Y16	Z16	X17	Y17	Z17	X18	Y18	Z18	X19	Y19	Z19	X20	Y20	Z20	X21	Y21	Z21	X22	Y22	Z22	X23	Y23	Z23	X24	Y24	Z24\n'''
      % (finalfilename, df.shape[0], df.shape[0]))
    csvfile.close()
  df = df.resample('33333U').bfill()
  df = df.reset_index()
  df.to_csv(path + '/' + finalfilename, sep='\t', date_format='%H%M%S%f', mode='a')
