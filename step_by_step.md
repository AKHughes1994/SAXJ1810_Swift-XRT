## Preliminary Files and Information 

Before starting data reduction get the following information:
1. Get the Observation IDs and the Source ID through [here](https://www.swift.psu.edu/operations/obsSchedule.php). The naming convention is 000 + targetID + segment number (e.g., 012). The name is 00032459012 for this example.
2. The data is acquired from the archive located [here](https://www.swift.ac.uk/swift_portal/)
3. The X-ray position of the source can be calcualted [here](https://www.swift.ac.uk/swift_portal/). For this source (SAX J1810.8-2609) the source position is (272.68532, -26.15054).

Once you have downloaded/got this information you are ready for HEASOFT data reduction

## Getting the Event Files

In this section we will clean the event files with `xrtpipeline`, apply barrycenter corrections with `barrycor', and isolate the files that are needed for our analysis

### Running xrtpipeline

When you download the observations from it should come in the form of a `.tar` file, i.e., `00032459012.tar`, we want to peform the following steps to run the xrtpipeline (remember to initialize HEASOFT with `heainit` or whatever your alias is),
```
cd into_to_dir
tar -xf 00032459012.tar
xrtpipeline clobber=yes createexpomap=yes cleanup=no
```
This will ask for a number of inputs, here is the inputs for this example,
```

```
