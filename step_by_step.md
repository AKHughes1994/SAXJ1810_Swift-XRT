## Preliminary Files and Information 

Before starting data reduction get the following information:
1. Get the Observation IDs and the Source ID through [here](https://www.swift.psu.edu/operations/obsSchedule.php). The naming convention is 000 + targetID + segment number (e.g., 012). The name is 00032459012 for this example.
2. The data is acquired from the archive located [here](https://www.swift.ac.uk/swift_portal/)
3. The X-ray position of the source can be calcualted [here](https://www.swift.ac.uk/user_objects/). For this source (SAX J1810.8-2609) the source position is (272.68532, -26.15054).

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
gunzip 00032459012/auxil/sw00032459012sao.fits.gz
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

### Spectra
We need to make the preliminary files (specifically the ARF and get the RMF file) 
The following command can make the arf file
```
xrtmkarf clobber=yes expofile=sw00032459012xwtw2po_ex.img outfile=sw00032459012.arf phafile=src.pha srcx=-1 srcy=-1 psfflag=yes
```
The RMF file will be given in the output of  `xrtmkarf`, e.g., 
```
xrtmkarf_0.6.4: Info: Processing '/home/akh/Programs/caldb/data/swift/xrt/cpf/rmf/swxwt0to2s6_20131212v015.rmf' CALDB file.
```
From here you need to apply grppha and then you have everything you need to fit spectra in Xspec of PyXspec

### X-ray upper limits
If you do not have an X-ray detection, adopt the following steps:

1. Using a 30-pixel extraction region get an initial estimate of the count rate then using the count rate pick an extraction region following Evans 2009. For the 2023 ToO observations of SAX J1810 the 30-pixel count rate (without background subtraction) was 1.55e-3 counts per second and the background count rate was 1.39e-2 (the annular region with an inner radius of 60 pixels and outer of 110 pixels). Therefore calculating the areas, and correcting for the different areas we get a background subtracted count rate (i.e., Corr = Src - Bkg * Area_ratio) of 2e-4, the lowest count rate region suggesting a 5-pixel extraction radius. 

2. With the next extraction region get the number of total counts, do this using `xselect', and extracting a curve/spectra will output (see below). For this example, there were only 1 + 0 = 1 photons (we got two back-to-back event files hence the summation) in the 1-10 keV range in the source range. For the background range, we got 54 + 31 = 85.
```
 Spectrum         has        1 count for  2.5815E-04 counts/sec
```
3. Record the BACKSCAL for the Src (7.9e-5), background (2.669e-2), dad-time corrected on sources time (5.32448753e3). Use the ratio of the BACKSCAL parameters to correct for the different area of the extraction regions, and once again calculate a net number of counts (and a count rate using the exposure time). Adopt 3x the upper Gehrels error as your count rate.

4. To convert from a count rate to a flux first make a spectrum, arf, and rmf file. Load in the spectrum and the arf (using `arf [ARFFILE]`) and rmf (using `resp [RMFFILE]`) into xspec. Then pick a simple tbabs*pegpwrlw model (fill in the known NH), and from there you can predict a count rate using `show rates`, record the model predicted rate for the assumed model flux (by default just use 1e-12) and from there you can convert the count rate to flux, and you have your upper limit.  




