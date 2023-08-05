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
from astropy.time import Time


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


def astrometry_from_list(file_containing_list_of_files)
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
