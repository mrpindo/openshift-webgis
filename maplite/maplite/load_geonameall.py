from maplite.models import Geoname, GeonameAll
#from django.utils import simplejson
from django.contrib.gis.geos import (Point, fromstr, fromfile,
               GEOSGeometry, MultiPoint, MultiPolygon, Polygon)

def run(verbose=True):
    #q0 = Geoname.objects.filter(id__lte=10).geojson()
    #q0 = Geoname.objects.filter(id__lte=10).values('longitude', 'latitude')   #Works
    #q0 = Geoname.objects.filter(id__gte=1).values('longitude', 'latitude')  #Works, but bring browser to its knee
    #q0 = Geoname.objects.filter(id__lte=1000).values('longitude', 'latitude')   #Works

    #q0 = Geoname.objects.order_by('?')[:2000].values('longitude', 'latitude')    #Works
    q0 = Geoname.objects.filter(id__gte=1).values('longitude', 'latitude')

    #print q0   #Works

    q1 = []


    for item in q0:
        #q1 = q0[seq]['longitude'] +' '+ q0[seq]['latitude']
        #q1 += [str(item['longitude']) +' '+ str(item['latitude'])]   #Works
        #q1 += [str(item['longitude']) +' '+ str(item['latitude'])]   #Works
        #q1.append(str(item['longitude']) +' '+ str(item['latitude']))   #Works

        q1.append( GEOSGeometry('POINT(%s %s)' %(item['longitude'], item['latitude'])))



    q2 = MultiPoint(q1) 

    q3 = GeonameAll.objects.get(id=1)
    q3.pois = q2 
    q3.save()


    qs = q2

    #print qs		#Works

