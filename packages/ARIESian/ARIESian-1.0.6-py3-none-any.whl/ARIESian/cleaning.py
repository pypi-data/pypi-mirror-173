import numpy as np
import matplotlib as mp
import ccdproc,os,sys,time,random
from astropy import units as u
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from glob import glob
#from astroquery.astrometry_net import AstrometryNet
from astropy.wcs import WCS
import astroalign as aa
from astropy.coordinates import SkyCoord
#from pyraf import iraf
#from iraf import noao,imred,specred
from astropy.nddata import CCDData
from astropy.stats import sigma_clipped_stats, SigmaClip
from astropy.visualization import ImageNormalize, LogStretch
from matplotlib.ticker import LogLocator
from photutils.background import Background2D, MeanBackground,SExtractorBackground
from photutils import find_peaks, CircularAperture, CircularAnnulus, aperture_photometry
from photutils.centroids import centroid_2dg
from astropy.stats import SigmaClip, mad_std
from photutils import Background2D, MedianBackground, DAOStarFinder
from photutils.utils import calc_total_error
#from photutils.detection import findstars
from glob import glob
import sys
from astropy.time import Time
from photutils.morphology import data_properties	
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.modeling.models import Const1D, Const2D, Gaussian1D, Gaussian2D




#dira = '.'
#gain = 2 * u.electron / u.adu  # float(input("Enter gain value")) gain and readout noise are properties of the CCD and will change for different CCDs.
#readnoise = 7.5 * u.electron    # float(input("Enter Read out noise value"))


def cleaning(dira,gain,readnoise):
	gain*=u.electron / u.adu
	readnoise*=u.electron
	mastebia=sorted(glob(os.path.join(dira,'masterbias.fits')))
	aa='n'
	if len(mastebia)==1:
		aa=str(input("Master BIAS already generated. want to regenerate?(y/n)"))

	if aa=='y' or len(mastebia)==0:
		bias_files = sorted(glob(os.path.join(dira,sys.argv[1])))
		biaslist = []
		for i in range (0,len(bias_files)):
			data= ccdproc.CCDData.read(bias_files[i],unit='adu')
			biaslist.append(data)

		masterbias = ccdproc.combine(biaslist,method='median',sigma_clip=True,sigma_clip_low_thresh=5,sigma_clip_high_thresh=5,sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std)
		masterbias.write('masterbias.fits', overwrite=True)
		mbias=ccdproc.CCDData.read('masterbias.fits',unit='adu')
		print('Master bias generated')
		print(" Mean and median of the masterbias: ",np.mean(masterbias), np.median(masterbias))



	flat_files=sorted(glob(os.path.join(dira,sys.argv[2])))
	print(flat_files)
	def inv_median(a):
	    return 1 / np.median(a)


	counter=0
	mastefla=sorted(glob(os.path.join(dira,'masterflat.fits')))
	if len(mastefla)==1:
		aa=str(input("Master FLAT  has already been generated. want to regenerate?(y/n)"))

	if aa=='y' or len(mastefla)==0:
		print(counter,'masterflat.fits')
		flatlist = []
	for k in flat_files:
		flat=ccdproc.CCDData.read(k,unit='adu')
		flat_bias_removed=ccdproc.subtract_bias(flat,masterbias)
		flatlist.append(flat_bias_removed)
		masterflat = ccdproc.combine(flatlist,method='median', scale=inv_median,sigma_clip=True, sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std)
		masterflat.write('masterflat.fits', overwrite=True)
		mflat=ccdproc.CCDData.read('masterflat.fits',unit='adu')
		print('Master flat generated')
		print(" Mean and median of the masterflat: ",np.mean(masterflat), np.median(masterflat))

	print("Master BIAS and Master Flat are generated")


	file_names = sorted(glob(os.path.join(dira,sys.argv[3])))

	counter=0
	for k in file_names:	
		fs=fits.open(k)
		#print(fs[0].header['FILTER1'],fs[0].header['OBJECT'])
		image=ccdproc.CCDData.read(k,unit='adu')
		header=fits.getheader(k)
		mflat=ccdproc.CCDData.read('masterflat.fits',unit='adu')
		mbais=ccdproc.CCDData.read('masterbias.fits',unit='adu')
		bias_subtracted = ccdproc.subtract_bias(image, mbais)
		flat_corrected = ccdproc.flat_correct(bias_subtracted, mflat)
		cr_cleaned =ccdproc.cosmicray_lacosmic(flat_corrected,readnoise=7.5,sigclip=5,satlevel=65535,niter=20,cleantype='meanmask',gain_apply=True)
		clean_file=k.replace('.fits','')
		fits.writeto(clean_file+'_cleaned.fits',cr_cleaned,header,output_verify='ignore',overwrite=True)
		print('Cleaning done on ',k )	



#cleaning()
