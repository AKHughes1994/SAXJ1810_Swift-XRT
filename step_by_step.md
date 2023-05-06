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
This will run the pipeline creating the clean data products. Once the pipeline finished (without errors) it will make a lot of files, most of them we do not need. I make a new directory called `xrt_files`, and move in the following files, 
```
mv 00032459012-xrt/sw00032459012xwtw2po_cl.evt xrt_files/.
mv 00032459012-xrt/sw00032459012xwtw2po_ex.img xrt_files/.
mv 00032459012-xrt/sw00032459012xhdtc.hk xrt_files/.
gunzip 00032459012/auxil/sw00032459012pat.fits.gz
mv 00032459012/auxil/sw00032459012pat.fits xrt_files/.
gunzip 00032459012/auxil/sw00032459012pat.fits.gz
mv 00032459012/auxil/sw00032459012sao.fits xrt_files/.
```
From here we have all the files we need to perform the X-ray analysis.

### Applying the Barycentric Correction

Documentation is [here](https://www.swift.ac.uk/analysis/xrt/barycorr.php)

First `cd` into the directory with the data products (i.e., `xrt_files`), then run the following command,
```
barycorr ra=272.68549 dec=-26.15030
Input file name:[sw00032459012xwtw2po_cl.evt] sw00032459012xwtw2po_cl.evt 
Output file name:[sw00032459012xwtw2po_cl_bary.evt] sw00032459012xwtw2po_cl_bary.evt 
Orbit ephemeris file(s) (or @filename, or GEOCENTER):[sw00032459012sao.fits] sw00032459012sao.fits
```
repeat this same command by replacing the input file with the `.hk` and `pat.fits` file, now we have our barycentric corrected data files, and we are ready to make data products 

## Extract Data Products
Here we will outline how to extract data products, namely Light curves and Spectra

### Region files
Region files adopt ds9 formatting. The way to make region files is to open the `.evt` file in `fv` or `ds9`, locating the peak pixel and making circular regions. I keep the region files in a directory called `region_files` and for this outburst we have both circular and annular regions (since the source is piled up during the burst)

### Light Curve

Documentation is [here](https://www.swift.ac.uk/analysis/xrt/timing.php) and [here](https://www.swift.ac.uk/analysis/xrt/lccorr.php)

To extract light curves we are going to use `xselect` an example is as follows, we want to initialize, 
```
xselect [Enter]
read event
Enter the Event file dir [.]
Enter Event file list [sw00032459012xwtw2po_cl.evt]
```

From here we want to specify the time binning and region files, for example we are going to use a circular source region, and count rate of 1s
```
filter region ../region_files/src_circ.reg
set binsize 1
extract curve
save curve src_circ_1s.lc 
```

Applying the exposure time correction correction, from here,
```
xrtlccorr
Name of the input region file or NONE to read region from lcfile[none] none
Name of the input Light Curve FITS file or NONE to read region from regionfile[./00032459012-xrt/sw00032459012xwtw2stsr.lc] src_ann_3pix_1s.lc 
Name of the Corrected Light Curve or DEFAULT for standard name[./00032459012-xrt/sw00032459012xwtw2stsr_corr.lc] src_ann_3pix_1s_corr.lc 
Name of the output file or DEFAULT for standard name[./00032459012-xrt/sw00032459012xwtw2stsr_corrfact.fits] src_ann_3pix_1s_corrfact.fits    
Name of the input Attitude FITS file[./00032459012/auxil/sw00032459012pat.fits.gz] ../xrt_files/sw00032459012pat.fits 
Name of the output Instrument Map File or DEFAULT for standard name[./00032459012-xrt/sw00032459012xwtw2st_srawinstr.img] DEFAULT
Name of the input Event FITS file[./00032459012-xrt/sw00032459012xwtw2st_cl.evt] ../xrt_files/sw00032459012xwtw2po_cl.evt
Name of the input Housekeeping Header Packets FITS file[./00032459012-xrt/sw00032459012xhdtc.hk] ../xrt_files/sw00032459012xhdtc.hk 
```

Now apply the exposure time correction, 
```
lcmath err_mode=2
Name of input FITS file[] src_ann_3pix_1s_corr.lc 
Name of background FITS file[] bkg_circ_1s.lc 
Name of output FITS file[] src_ann_3pix_1s_sub.lc 
Scaling factor for input[1.] 0.9
Scaling factor for background[1.] 1.0
Add instead of subract?[no] no
```

Now you should have fully corrected, background subtracted light curves. The other option is to use the pipeline which should apply all of these corrections automatically, see ex. `get_lc_from_pipeline.py`
