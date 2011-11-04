from igfile.igfile import *

# Open an ig-file
archive = IgArchive("/Users/ktf/Dropbox/Leaf/tests/RelValSingleMuonPt10.ig")
# Get a given event by index.
event = archive[0]

# Show eta / phi for all the EERecHits.
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
data=zip(event.EERecHits_V1.eta, event.EERecHits_V1.eta)
ax.plot([x for x in event.EERecHits_V1.eta], 
        [y for y in event.EERecHits_V1.phi], 'o')
ax.plot([x for x in event.EBRecHits_V1.eta], 
        [y for y in event.EBRecHits_V1.phi], 'x')

plt.show()