import ROOT
import sys
import random

# name = "/opt/ppd/darkmatter/CREF/pub/CAEN_files/run_14/RAW/DataR_run_14.root"
name = "DataR_run_17.root"
f = ROOT.TFile.Open(name, "READ")

def printTree(fl, tName):
    # Get the tree name with some intelligence
    tree = fl.Get(tName)
    try :
        ddr = tree.GetListOfKeys()[0].GetName() # Just use the first name in this list. Should be only one sub-tree anyway.
        tree = fl.Get(tName + "/" + ddr)
    except AttributeError:
        print("Maybe no sub-directory (Genius level user ...)? Continue with the main name")
    except IndexError:
        print("Likely Corrupted tree (if not file). Try the next tree")
        return

    # Get the branches
    try:
        branches = tree.GetListOfBranches()
        nBranches = len(branches)
        if type(nBranches) != type(0):
            print("Strange branch problem ... corrupted file? Returning. Branch type is ", type(branches))
            return
    except: # Really?
        print("Unknown tree and branches. Life is too short to proceed beyond this 1.")
        return

    # The number of events we are skipping.
    totEvents = tree.GetEntries()
    listOfLeaves = range(nBranches)

    # Some printouts once per tree
    print("Reading the following branches :")
    print(listOfLeaves)
    for i in range(nBranches):
        # print(dir(branches[listOfLeaves[i]]))
        if branches[listOfLeaves[i]].GetName() == "Samples":
            print("-----", i, listOfLeaves[i], branches[listOfLeaves[i]].GetName(),
                branches[listOfLeaves[i]].GetTitle(),
                branches[listOfLeaves[i]].GetBrowsables())
            print(len(branches[listOfLeaves[i]].GetBrowsables()))
            for bb in branches[listOfLeaves[i]].GetBrowsables():
                print(bb)
    print("Running over %s events" % tree.GetEntries())

    # Now loop over the events in the tree and read in each branch / leaf
    kount = 0
    for event in tree:
        for iBranch in range(nBranches): # Read in the branches randomly
            nleaves = branches[iBranch].GetListOfLeaves()
            browsables = branches[iBranch].GetBrowsables()
            print(f"We have {len(nleaves)}")
            value = tree.GetLeaf(branches[listOfLeaves[iBranch]].GetName()).GetValue()
            print("Browsables ...", len(browsables))
            print(i, event, iBranch, listOfLeaves[iBranch], branches[listOfLeaves[iBranch]].GetName(), value)
        print(f"Size of array : {event.Samples.fN} {event.Samples.GetSum()} {event.Samples.GetSize()}")
        for ii in range(event.Samples.fN):
            print(f"Value of element {ii} : {event.Samples.fArray[ii]}")
        kount = kount + 1
        print ("Tree : %s, Event number : %s" %(tName, kount))
        if kount %1000 == 3:
            return

for key in f.GetListOfKeys():
    print("Looping over tree ", key.GetName())
    printTree(f, key.GetName())
f.Close()
