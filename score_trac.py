import re
import csv
import sys

def run(path, filename):
  data = []

  with open(path + '/' + filename, 'r') as f:
      for line in f:
          m = re.search('^([\d\.]+) \+?(.*) \+?(.*) \+?(.*) \+?(.*) \+?(.*) \+?(.*) \+?(.*)$', line)
          if m:
              row = []
              row.append(int(m.group(2)))
              row.append(float(m.group(1)))
              row.append(float(m.group(3)))
              row.append(0)
              row.append(0)
              row.append(float(m.group(4)))
              row.append(float(m.group(5)))
              row.append(0)
              row.append(float(m.group(6)))
              row.append(float(m.group(7)))
              row.append(0)
              row.append(float(m.group(8)))
              row.append(0)
              row.append(0)
              data.append(row)

  print(data[0][1])

  newfilename = 'pm-' + filename
  with open(path + '/' + newfilename, 'w', newline='') as csvfile:
    csvfile.write('''PathFileType	4	(X/Y)	%s
  DataRate	CameraRate	NumFrames	NumMarkers	Units	OrigDataRate	OrigDataStartFrame	OrigNumFrames
  30.00	30.00	      %d	4	mm	30.00	1	      %d
  Frame#	Time	Rotation			Translation			Scaling			Triangle
      X1	M1	N1	X2	Y2	N2	X3	Y3	N3	X4	M4	N4\n'''
      % (newfilename, len(data), len(data)))
    csvwriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in data:
      csvwriter.writerow(row)
