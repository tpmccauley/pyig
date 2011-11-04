from igfile.igfile import *

import sys
import math
import re
import fnmatch
import os

from ROOT import TCanvas
from ROOT import TH1D
from ROOT import TLegend

mass = 0.105658367 # GeV

def fourV(pt, eta, phi):
    theta = 2*math.atan(math.exp(-eta))
    px = pt*math.cos(phi)
    py = pt*math.sin(phi)
    pz = pt/math.tan(theta)
    E = math.sqrt(mass*mass +px*px + py*py + pz*pz)
    return [E, px, py, pz]
   
if len(sys.argv) != 3:
    print 'Usage python test_DumpCSV.py [ig file directory] [csv output file name]'
    sys.exit()

ig_dir = sys.argv[1]
csv_file = open(sys.argv[2], 'w')

first_line = 'RunNo, EvNo, E, px, py, pz, pt, eta, phi, Q, MET, phiMET'
csv_file.write(first_line+'\n')

print first_line

for file in os.listdir(ig_dir):

    if fnmatch.fnmatch(file, '*.ig'):

        print 'Processing', file
        archive = IgArchive(ig_dir+file)
        events = archive.events()

        for e in range(len(events)):
            event = archive.getEvent(events[e])

            for runn in event.Event_V2.run:
                new_line = str(runn)+', '
            
            for evn in event.Event_V2.event:
                new_line += str(evn)+', '
                
            charges = [ch for ch in event.GlobalMuons_V1.charge]
            pts = [pt for pt in event.GlobalMuons_V1.pt]
            etas = [eta for eta in event.GlobalMuons_V1.eta]
            phis = [phi for phi in event.GlobalMuons_V1.phi]

            for i in range(len(pts)):
                if pts[i] < 25.0:
                    continue
                fourv = fourV(pts[i], etas[i], phis[i])

                new_line += str(fourv[0])+', '+str(fourv[1])+', '
                new_line += str(fourv[2])+', '+str(fourv[3])+', '
                new_line += str(pts[i])+', '+str(etas[i])+', '+str(phis[i])+', '
                new_line += str(charges[i])+', '

            for met in event.METs_V1.pt:
                new_line += str(met)+', '

            for phi in event.METs_V1.phi:
                new_line += str(phi)

            csv_file.write(new_line+'\n')

            print new_line
            

csv_file.close()

            

                
                
                
             
            
            
