from swifttools.xrt_prods import XRTProductRequest
import time, json, glob, os, argparse
import numpy as np


def main():
    # Source Parameters
    ra  = 272.68549 
    dec = -26.15030
    dt  = 1

    # Load in the arguments
    parser = argparse.ArgumentParser(description='Read in the segments')
    parser.add_argument('--segments', '-s', nargs='+', help='Pass the segments separated by a space')
    parser.add_argument('--centroid',    action='store_true', help='Centroiding')
    parser.add_argument('--no-centroid', action='store_false', dest='centroid', help='No Centroiding')
    parser.add_argument('--targetID', '-t', default='00032459')
    args = parser.parse_args()
    segments = np.array(args.segments).astype(int)
    centroid = args.centroid
    targetID = str(args.targetID)

    # Format the segment list  to feed into the Pipeline commands
    ObsID=''
    for seg in segments:
        ObsID = ObsID + ',%s%03d' %(targetID,seg)
    ObsID = ObsID[1:] # Remove leading comma

    # Get the data products from the Swifttools pipeline
    print('# Running the Swift XRT pipeline #')
    myRequest = XRTProductRequest('hughes1@ualberta.ca', silent=False)

    # Set the global Parameters
    if centroid == True:
        myRequest.setGlobalPars(name='SAX J1810.8-2609',
                        targ=targetID,
                        SinceT0=False,
                        RA=ra,
                        Dec=dec,
                        centroid=centroid,
                        useSXPS=False,
                        poserr=1)
    else:
        myRequest.setGlobalPars(name='SAX J1810.8-2609',
                        targ=targetID,
                        SinceT0=False,
                        RA=ra,
                        Dec=dec,
                        centroid=centroid,
                        useSXPS=False)

    # Define the parameters to extract a light curve -- times are in seconds
    myRequest.addLightCurve(binMeth='obsid',
                          allowUL='no',
                          allowBayes='no',
                          whichData='user',
                          useObs=ObsID,
                          minEnergy=0.5,
                          maxEnergy=10.0,
                          softLo=0.5,
                          softHi=2.0,
                          hardLo=2.0,
                          hardHi=10.0,
                          minFracExp=0.0,
                          wtBinTime=1.0,
                          pcBinTime=2.51,
                          matchHR=True)

    # Check if valid
    if(myRequest.isValid()[0]==True):
        if not myRequest.submit():
            print (f"I couldn't submit error:{myRequest.submitError}")

        while not myRequest.complete:
            time.sleep(10)

        # Retrieve the products
        dictLC = myRequest.retrieveLightCurve(returnData=True, deprecate=False)
#        myRequest.downloadProducts('swift_lc', clobber=True)
#        os.system('tar -xf swift_lc/lc.tar.gz -C swift_lc/')
#        os.system('mv swift_lc/USER*/lc/* swift_lc/.')
#        os.system('rm -rf swift_lc/USER* swift_lc/lc.tar.gz')

    else:
        print("BAD REQUEST:", myRequest.isValid()[1])
        exit()

if __name__ == "__main__":
    main()
