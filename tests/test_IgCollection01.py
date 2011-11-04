from igfile.igfile import *

# Open an ig-file
archive = IgArchive("/Users/ktf/Dropbox/Leaf/tests/RelValSingleMuonPt10.ig")

# Simple way of listing all the events contained in the file.
print archive.events()

# Get a given event by index.
event = archive[0]

# Get a collection and print its schema.
c = event.Event_V1
print c

# Print the name of all the columns in a given collection
for column in event.Event_V1.columns():
  print "\tColumn:", column

# Programmatically print all the columsn
for collection in event.collections():
  if collection.name != "Event_V1":
    continue
  print "Collection", collection.name, ":", collection
  for column in collection.columns():
    print "\tColumn:", column
    for item in collection.column(column):
      print "\t\t", item

# Sum all the electromagnetic contributions to the calo towers.
print sum(em for em in event.CaloTowers_V1.emEnergy)

# Sum all the hadronic contributions to the calo towers above a given level.
print sum(had for had in event.CaloTowers_V1.hadEnergy if had > 1.)

# Show eta / phi for all the EERecHits.
print zip(event.EERecHits_V1.phi, event.EERecHits_V1.eta)