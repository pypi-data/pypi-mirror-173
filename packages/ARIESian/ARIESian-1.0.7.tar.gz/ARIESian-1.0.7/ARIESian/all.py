import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from glob import glob
from astroquery.astrometry_net import AstrometryNet
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import sys
import matplotlib as mp
import ccdproc,os,sys,time,random
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
from photutils.morphology import data_properties	
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.modeling.models import Const1D, Const2D, Gaussian1D, Gaussian2D
from photutils.detection import findstars


class Astrometry:
	def astrometry_from_image(filename):
		f=open(list_of_filenames)
		lines=f.readlines()

		for line in lines:
			ast=AstrometryNet()
			ast.api_key= 'iqmqwvazpvolmjmn'
			wcs_header=ast.solve_from_image(line.split()[0])
			wcs=WCS(wcs_header)
			hdu=fits.open(line.split()[0])[0]
			image=hdu.data
			header=hdu.header
			hdu.header.update(wcs.to_header())
			hdu.writeto(str(line.split()[0]), output_verify='ignore',overwrite=True)

		f.close()


	def astrometry_from_list(file_containing_list_of_files):
		f=open(file_containing_list_of_files)
		lines=f.readlines()

		for line in lines:
			ast=AstrometryNet()
			ast.api_key= 'iqmqwvazpvolmjmn'
			wcs_header=ast.solve_from_image(line.split()[0])
			wcs=WCS(wcs_header)
			hdu=fits.open(line.split()[0])[0]
			image=hdu.data
			header=hdu.header
			hdu.header.update(wcs.to_header())
			hdu.writeto(str(line.split()[0]), output_verify='ignore',overwrite=True)

		f.close()



class Telescope:
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





	def photometry(list_of_filenames_file):
		f=open(list_of_filenames_file)
		lines=f.readlines()
			
		mag_a1,mag_err_a1=[],[]
		mag_a2,mag_err_a2=[],[]	
		mag_a3,mag_err_a3=[],[]
		mag_a4,mag_err_a4=[],[]
		fwhm_list=[]


		fs=fits.open(lines[0].split()[0])
		daa=fs[0].data
		mean,std=np.mean(daa),np.std(daa)
		xclick=[]
		yclick=[]
		def onclick(event):
			xclick.append(event.xdata)
			yclick.append(event.ydata)

		fig,ax = plt.subplots()
		ax.imshow(daa,cmap='gray',vmin=mean-0.5*std,vmax=mean+0.5*std)
		ax.set_title("Click on stars you want to photometry to be done")	
		fig.canvas.mpl_connect('button_press_event', onclick)
		plt.show()
		w=WCS(lines[0].split()[0])
		stars=w.pixel_to_world(xclick,yclick)
		f=open("Photometry_star_radecs",'w+')
		f.writelines("RA Dec\n")
		for i in range(len(stars)):
			f.writelines(str(stars[i].to_string('hmsdms'))+'\n')

		f.close()

		for line in lines:
			print("Reading file ",line.split()[0])
			fs=fits.open(line.split()[0])
			daa=fs[0].data
			w=WCS(line.split()[0])
			#finding centroid and fwhm of stars
			positions=[]
			fwhms=[]
			for ijk in range(len(stars)):
				frcnc=w.world_to_pixel(stars[ijk])
				mydata=daa[int(frcnc[1])-10:int(frcnc[1])+10,int(frcnc[0])-10:int(frcnc[0]+10)]
				cs=centroid_2dg(daa[int(frcnc[1])-10:int(frcnc[1])+10,int(frcnc[0])-10:int(frcnc[0])+10])
				positions.append(frcnc+cs-(10,10))
				constant_init = 0.
				props = data_properties(mydata - np.min(mydata))
				g_init = (Const2D(constant_init) + Gaussian2D(amplitude=np.ptp(mydata),
									   x_mean=props.xcentroid,
									   y_mean=props.ycentroid,
									   x_stddev=props.semimajor_sigma.value,
									   y_stddev=props.semiminor_sigma.value,
									   theta=props.orientation.value))
				fitter = LevMarLSQFitter()
				y, x = np.indices(mydata.shape)
				gfit = fitter(g_init, x, y, mydata)
				fwhms.append(2.355*(gfit.x_stddev_1+gfit.y_stddev_1)/2)
			fwhm=np.mean(np.array(fwhms))
			radii=np.array([fwhm,2*fwhm,3*fwhm,4*fwhm]) #np.arange(5,15)
			apertures = [CircularAperture(positions, r=r) for r in radii]
			an_ap = CircularAnnulus(positions, r_in=5*fwhm, r_out=7*fwhm)
			bkg_phot=aperture_photometry(daa,an_ap)
			try:		
				exposure=fs[0].header['EXPTIME']
			except:
				exposure=fs[0].header['EXPOSURE']
			error=calc_total_error(daa,0,effective_gain=exposure)
			star_phot=aperture_photometry(daa,apertures,error=error)
			bkg_sum=bkg_phot['aperture_sum'] / an_ap.area
			colms=star_phot.colnames
			flux_sums=[]
			mags=[]
			flux_err=[]
			lasa=0
			for c in star_phot.colnames[3:][::2]:
				flux_sums.append(star_phot[c]-bkg_sum*apertures[lasa].area)
				mags.append(-2.5*np.log10((star_phot[c]-bkg_sum*apertures[lasa].area)/exposure)+22)			
				lasa+=1

			for c in star_phot.colnames[3:][1::2]:
				flux_err.append(star_phot[c])

			mag_err=1.09*np.array(flux_err)/np.array(flux_sums)
			mag_back=-2.5*np.log10(bkg_phot['aperture_sum']/exposure)+22


			mag_a1.append(mags[0])
			mag_err_a1.append(mag_err[0])
			mag_a2.append(mags[1])
			mag_err_a2.append(mag_err[1])
			mag_a3.append(mags[2])
			mag_err_a3.append(mag_err[2])
			mag_a4.append(mags[3])
			mag_err_a4.append(mag_err[3])
			fwhm_list.append(fwhm)


		f.close()
		f=open('1xFWHM','w+')
		ff=open('2xFWHM','w+')
		fff=open('3xFWHM','w+')
		ffff=open('4xFWHM','w+')

		for j in range(len(lines)):
			print("\t".join("{} {}".format(x, y) for x, y in zip(np.round(mag_a1[j],4), np.round(mag_err_a1[j],4))))
			f.writelines("\t".join("{} {}".format(x, y) for x, y in zip(np.round(mag_a1[j],4), np.round(mag_err_a1[j],4))))
			ff.writelines("\t".join("{} {}".format(x, y) for x, y in zip(np.round(mag_a2[j],4), np.round(mag_err_a2[j],4))))
			fff.writelines("\t".join("{} {}".format(x, y) for x, y in zip(np.round(mag_a3[j],4), np.round(mag_err_a3[j],4))))
			ffff.writelines("\t".join("{} {}".format(x, y) for x, y in zip(np.round(mag_a4[j],4), np.round(mag_err_a4[j],4))))



		f.close()
		ff.close()
		fff.close()
		ffff.close()


		f=open('FWHM.log','w+')
		for i in range(len(fwhm_list)):
			f.writelines(str(lines[i].split()[0])+'\t'+str(fwhm_list[i])+'\t'+str(2*fwhm_list[i])+'\t'+str(3*fwhm_list[i])+'\t'+str(4*fwhm_list[i])+'\t'+str(5*fwhm_list[i])+'\t'+str(7*fwhm_list[i])+'\n')

