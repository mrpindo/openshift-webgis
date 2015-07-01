import os
from django.contrib.gis.utils import LayerMapping
from maplite.models import IndonesiaProvince

IP_mapping = {
    'propinsi' : 'PROPINSI_',
    'kode_prov' : 'KODE_PROV',
    'kode' : 'KODE',
    'mpoly' : 'MULTIPOLYGON',
}

IP_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/IP.shp'))

def run(verbose=True):
    lm = LayerMapping(IndonesiaProvince, IP_shp, IP_mapping,
                      transform=False, encoding='iso-8859-1')


    lm.save(strict=True, verbose=verbose)
