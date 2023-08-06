from lenskappa.counting import SingleCounter
from lenskappa.catalog import MaxValueFilter, MinValueFilter, QuantCatalogParam
import multiprocess
from heinlein import load_dataset

from astropy.coordinates import SkyCoord
import astropy.units as u
from shapely import geometry
import logging
import time
import os

def get_range(x_range, y_range, output_dir):

    aperture = 120*u.arcsec
    for i_x in x_range:
        for i_y in y_range:


if __name__ == "__main__":
    weights = 'all'
    zmax_filter = MaxValueFilter('z_gal', 1.523)
    magmax_filter = MaxValueFilter('mag_i', 23.0)
    mindist_filter = MinValueFilter('r', 5*u.arcsec)
    param = [QuantCatalogParam("M_Stellar[M_sol/h]", "m_gal"), QuantCatalogParam('mag_SDSS_i', 'mag_i')]
    output_dir = "/Users/patrick/code/Production/environment_study/lenskappa/tests"
    mils = load_dataset("ms")
    ct = SingleCounter(mils, False)
    output_file = "ms_{}_{}_sampled.csv".format(i_x, i_y)
    output_path = os.path.join(output_dir, output_file)
    mils.load_catalogs_by_field(i_x,i_y,z_s = 1.523, params=param)
    ct.add_catalog_filter(zmax_filter, 'zmax')
    ct.add_catalog_filter(magmax_filter, 'magmax')
    ct.add_catalog_filter(mindist_filter, 'mindist')
    ct.get_weights(output_positions=True, weights=weights, meds=True, output_file = output_path, overlap=4,aperture=aperture, n_samples=10)

 