## Preliminary Files and Information 

Before starting data reduction get the following information:
1. Get the Observation IDs and the Source ID through [here](https://www.swift.psu.edu/operations/obsSchedule.php). The naming convention is 000 + targetID + segment number (e.g., 012). The name is 00032459012 for this example.
2. The data is acquired from the archive located [here](https://www.swift.ac.uk/swift_portal/)
3. The X-ray position of the source can be calcualted [here](https://www.swift.ac.uk/swift_portal/). For this source (SAX J1810.8-2609) the source position is (272.68532, -26.15054).

Once you have downloaded/got this information you are ready for HEASOFT data reduction

## Getting the Event Files

In this section we will clean the event files with `xrtpipeline`, apply barrycenter corrections with `barrycor', and isolate the files that are needed for our analysis

### Running xrtpipeline

Documentation [here](https://www.swift.ac.uk/analysis/xrt/xrtpipeline.php)

When you download the observations from it should come in the form of a `.tar` file, i.e., `00032459012.tar`, we want to peform the following steps to run the xrtpipeline (remember to initialize HEASOFT with `heainit` or whatever your alias is),
```
cd into_to_dir
tar -xf 00032459012.tar
xrtpipeline clobber=yes createexpomap=yes cleanup=no
```
This will ask for a number of inputs, here is the inputs for this example,
```
Source RA position (degrees or hh mm ss.s) or POINT or OBJECT[272.68549] 272.68549
Source DEC position (degrees or dd mm ss.s) or POINT or OBJECT[-26.15030] -26.15030
Target Archive Directory Path[00032459005] 00032459012
Stem for FITS input files [i.e. sw00000000000][sw00032459005] sw00032459012
Directory for outputs[00032459005-xrt] 00032459012-xrt
```
This will run the pipeline creating the clean data products. 

