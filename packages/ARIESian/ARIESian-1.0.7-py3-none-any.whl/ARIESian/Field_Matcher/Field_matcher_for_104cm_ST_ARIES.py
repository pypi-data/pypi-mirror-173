#field matcher for 104cm ST

from astropy.wcs import WCS
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astroquery.astrometry_net import AstrometryNet
from astropy import units as u
from astropy.coordinates import SkyCoord
import sys
from astroquery.simbad import Simbad
import warnings
warnings.filterwarnings("ignore")

def Field_Matcher(filename):
	ast=AstrometryNet()
	ast.api_key= 'iqmqwvazpvolmjmn'
	wcs_header=ast.solve_from_image(filename)
	wcs=WCS(wcs_header)
	ra=wcs.wcs.crval[0]
	dec=wcs.wcs.crval[1]
	c=SkyCoord(ra=ra*u.degree,dec=dec*u.degree)
	print("Center of image is ",c.to_string('hmsdms'))

	target_name=str(input("Enter the  name of target "))
	result_table = Simbad.query_object(target_name)

	ra_targte,dec_target=str(result_table['RA'].data[0]),str(result_table['DEC'].data[0])
	c_target=SkyCoord(ra=ra_targte,dec=dec_target,unit=(u.hourangle, u.deg))

	target_ra_h,target_ra_m,target_ra_s=c_target.ra.hms[0],c_target.ra.hms[1],c_target.ra.hms[2]
	ra_h,ra_m,ra_s=c.ra.hms[0],c.ra.hms[1],c.ra.hms[2]


	target_dec_h,target_dec_m,target_dec_s=c_target.dec.hms[0],c_target.dec.hms[1],c_target.dec.hms[2]
	dec_h,dec_m,dec_s=c.dec.hms[0],c.dec.hms[1],c.dec.hms[2]

	print("Your target will be at center if you move \nR.A. by ",target_ra_h-ra_h, "h",target_ra_m-ra_m, "m",target_ra_s-ra_s, "s\nDec by ",target_dec_h-dec_h,' d ',target_dec_m-dec_m, ' m ',target_dec_s-dec_s , ' s ')

	hdu=fits.open(sys.argv[1])[0]
	image=hdu.data
	header=hdu.header
	hdu.header.update(wcs.to_header())
	hdu.writeto('new.fits', output_verify='ignore',overwrite=True)

