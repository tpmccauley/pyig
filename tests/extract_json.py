from igfile import *

import sys
import simplejson as json

import math
import re
import fnmatch
import os

if len(sys.argv) != 3:
    print 'Usage: python root2json.py [ig file name] [json file name]'
    sys.exit()

igfile_name = sys.argv[1]
ofile = open(sys.argv[2], 'w')

archive = IgArchive(igfile_name)
events = archive.events()

nevents = len(events)
muons = []

for e in range(nevents):
	event = archive.getEvent(events[e])

	#tracker_muons = event.TrackerMuons_V2
	standalone_muons = event.StandaloneMuons_V2
	#global_muons = event.GlobalMuons_V1

	pts = [pt for pt in standalone_muons.pt]

	if len(pts) == 0:
		continue

	charges = [charge for charge in standalone_muons.charge]
	etas = [eta for eta in standalone_muons.eta]
	phis = [phi for phi in standalone_muons.phi]

	for i in range(len(pts)):
		muons.append({'type':'standalone', 'pt':pts[i], 'charge':charges[i], 'eta':etas[i], 'phi':phis[i]})

	
ofile.write(json.dumps(muons, sort_keys=True, separators=(',',':')))
ofile.close()
