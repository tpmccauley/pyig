from igfile.igfile import *

import sys
import math
import re
import fnmatch
import os

from ROOT import TCanvas
from ROOT import TH1D

muon_mass = 0.105658367

class Muon:
    def __init__(self, eta, phi, pt, charge, type):

        self._eta = eta
        self._phi = phi
        self._pt = pt
        self._q = charge
        self._m = muon_mass

        theta = 2*math.atan(math.exp(-eta))
        self._px = pt*math.cos(phi)
        self._py = pt*math.sin(phi)
        self._pz = pt/math.tan(theta)
        
        E = self._m*self._m
        E += self._px*self._px + self._py*self._py + self._pz*self._pz
        self._E = math.sqrt(E)

        if re.search('Tracker', type):
            self._tracker = True
            self._global = False
        elif re.search('Global', type):
            self._global = True
            self._tracker = False
        else:
            print 'Unknown type of muon:', type
            self._global = False
            self._tracker = False

    def m(self):
        return self._m
    def E(self):
        return self._E
    def px(self):
        return self._px
    def py(self):
        return self._py
    def pz(self):
        return self._pz
    def eta(self):
        return self._eta
    def phi(self):
        return self.phi
    def pt(self):
        return self._pt
    def q(self):
        return self._q
    def isTracker(self):
        return self._tracker
    def isGlobal(self):
        return self._global

    def invariantMass(self, muon):
        m = (muon._E+self._E)*(muon._E+self._E)
        m -= (muon._px+self._px)*(muon._px+self._px)
        m -= (muon._py+self._py)*(muon._py+self._py)
        m -= (muon._pz+self._pz)*(muon._pz+self._pz)
        return math.sqrt(m)

    def printInfo(self):
        if self._tracker:
            print 'Tracker muon with eta, phi, q:', self._eta, self._phi, self._q
        elif self._global:
            print 'Global muon with eta, phi, q:', self._eta, self._phi, self._q
        else:
            print 'Unknown type of muon'

def GetGlobalMuons(event):

    muons = []
    
    gmuons = event.GlobalMuons_V1
    
    g_eta = [eta for eta in gmuons.eta]

    if len(g_eta) != 2:
        return muons

    g_q = [q for q in gmuons.charge]

    if g_q[0]*g_q[1] != -1:
        return muons
    
    g_phi = [phi for phi in gmuons.phi]
    g_pt = [pt for pt in gmuons.pt]

    for m in range(2):
        muons.append(Muon(float(g_eta[m]), float(g_phi[m]), float(g_pt[m]), int(g_q[m]), 'GlobalMuons_V1'))

    return muons

   
if len(sys.argv) != 2:
    print 'Usage python test_Dimuon.py [ig file directory] '
    sys.exit()

ig_dir = sys.argv[1]

nt = 'global dimuons'
spectrum = TH1D(nt, nt, 30, 2.0, 5.0)

for file in os.listdir(ig_dir):

    if fnmatch.fnmatch(file, '*.ig'):

        print 'Processing', file
        archive = IgArchive(ig_dir+file)
        events = archive.events()

        for e in range(len(events)):
            print '  Event', e
            event = archive.getEvent(events[e])
            muons = GetGlobalMuons(event)

            if len(muons) == 2:
                spectrum.Fill(muons[0].invariantMass(muons[1]))
                
c1 = TCanvas()
c1.cd()
spectrum.GetXaxis().SetTitle('\\mu+\\mu- invariant mass [GeV]')
spectrum.Draw()
            
if __name__ == '__main__':
   rep = ''
   while not rep in [ 'q', 'Q' ]:
      rep = raw_input( 'enter "q" to quit: ' )
      if 1 < len(rep):
         rep = rep[0]
