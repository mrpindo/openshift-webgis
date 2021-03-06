from django.shortcuts import render_to_response
from django.template import RequestContext
from maplite.models import IndonesiaProvince, WorldBorder, Geoname, GeonameAll, pois
import json
from django.views.decorators.csrf import csrf_protect


from django.core import urlresolvers
import datetime
from twitter import *		#Twitter-1.10.2 downloaded from Pypi

def twitpost(messg):
    t = Twitter(
            auth=OAuth('544171858-9fjXUCtv20hJC7OHO0lCpZIoB9jvsk4SXGtLinGA',             
                       'KhE2O0boTTqw3YOuWSQre179W81406GqFzdZENWOU',
                       'PdGhshzU7YV1Lpq3miOFFQ', 
                       'cDUlWi0wr7V5EI3RCuV2FFsMZINQD1pB6xU4MdLIY')
               )
    w = str(datetime.datetime.now())	
    t.statuses.update(
        status=w +", "+ messg)

'''
from django.contrib.gis.geos import GEOSGeometry
newid = 'null'
def add2pois(newpoi, newname):
    p = pois(poi='POINT('+ newpoi +')', poiname=newname)
    p.save()
    newid = p.id
'''


def home(request, template_name="home.html"):
    page_title = 'Home'
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def marker_detail(request, template_name="marker_detail.html"):
    page_title = 'Detail Masakan Padang'
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def landingpage_with_panel(request, template_name="landingpage_with_panel.html"):
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def alt_landingpage(request, template_name="alt_landingpage.html"):
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))



@csrf_protect
def alt_makemarker(request, template_name="alt_makemarker.html"):
    page_title = 'Buat Marker (Alternative)'

    #q0 = IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(kode_prov=52).geojson
    q0 = WorldBorder.objects.geojson().get(id=225).geojson
 
    qs = '{ "type": "Feature", "id": 0, "properties": { "PROPINSI": "Semua Propinsi", "COUNT": 14000 }, "geometry": '
    qs += q0
    qs += '}'


    q1 = pois.objects.filter(id__gte=1).geojson()
    if q1.count() != 0:
       qt = '{"type": "FeatureCollection", "features": ['
       for i in range(len(q1)):
           if i == len(q1)-1:       #put more elegant way, such  if i == "last dict"
             qt += '{ "type": "Feature", "id": '+ str(q1[i].id) +', "properties": {"poiname": "'+ str(q1[i]) +'" }, "geometry": '+ q1[i].geojson +'}]}'

           else:
             qt += '{ "type": "Feature", "id": '+ str(q1[i].id) +', "properties": {"poiname": "'+ str(q1[i]) +'" }, "geometry": '+ q1[i].geojson +'},'
    else:
       qt = '{"type": "FeatureCollection", "features": []}'


    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


@csrf_protect
def makemarker(request, template_name="makemarker.html"):
    page_title = 'Buat Marker'

    #q0 = IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(kode_prov=52).geojson
    q0 = WorldBorder.objects.geojson().get(id=225).geojson
 
    qs = '{ "type": "Feature", "id": 0, "properties": { "PROPINSI": "Semua Propinsi", "COUNT": 14000 }, "geometry": '
    qs += q0
    qs += '}'


    q1 = pois.objects.filter(id__gte=1).geojson()
    if q1.count() != 0:
       qt = '{"type": "FeatureCollection", "features": ['
       for i in range(len(q1)):
           if i == len(q1)-1:       #put more elegant way, such  if i == "last dict"
             qt += '{ "type": "Feature", "id": '+ str(q1[i].id) +', "properties": {"poiname": "'+ str(q1[i]) +'" }, "geometry": '+ q1[i].geojson +'}]}'

           else:
             qt += '{ "type": "Feature", "id": '+ str(q1[i].id) +', "properties": {"poiname": "'+ str(q1[i]) +'" }, "geometry": '+ q1[i].geojson +'},'
    else:
       qt = '{"type": "FeatureCollection", "features": []}'


    return render_to_response(template_name, locals(),context_instance=RequestContext(request))



def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
       cls = classes[clsname]
       obj = cls.__new__(cls)   # Make instance without calling __init__
       for key, value in d.items():
          setattr(obj, key, value)
          return obj
    else:
       return d


from django.contrib.gis.geos import GEOSGeometry
@csrf_protect
def makemarker_handler(request, req_type, kode_prov, template_name="makemarker_handler.html"):
    if request.method == 'GET':
        reqt = 'Request from client is: GET'
	#Do GET activity here
	
    else:    
        if (req_type == 'addnew'):
           reqt = 'Request from client is: POST'
           #reqc =  request.POST['csrfmiddlewaretoken']	#Works
           #reqc =  request.POST['geojson_data']		#Works
           #reqc =  request.POST				#Works

           reqd =  (request.POST['lng'] +' '+ request.POST['lat'])
           reqe =  request.POST['poiname']

           #Entry data to PostGIS
           p = pois(poi='POINT('+ reqd +')', poiname=reqe)
           p.save()

	   #reqc.extend([23]) might be possible to concat pois & respid  ? analise further
           reqc = {}        
           #reqc['pois'] = request.POST['lng'] +', '+ request.POST['lat'] +', '+ request.POST['poiname']
           reqc['respid'] = p.id 
           reqf = json.dumps(reqc)

        if (req_type == 'delete'):
           reqf = json.loads(request.POST['delpois'])

           qset = pois.objects.filter(id__in=reqf)
           qset.delete()

        if (req_type == 'update'):
           #reqf = json.loads(request.POST['updpois'])		#Works!
           #reqf = len(json.loads(request.POST['updpois']))	#Works!
           reqh = json.loads(request.POST['updpois'])		#Works!
           #reqh = request.POST['updpois']			#scrumbled egg!
           reqf = []
           for i in range(len(reqh)):
              #reqf.extend([reqh[i][0]])                #Works, returns id
              #reqf.extend([reqh[i][1]])		#Works, returns latlng	
              #reqf.extend([reqh[i][1]['lng']])		#Works, returns lng
              #reqf.extend([reqh[i][1]['lng'] +' '+ reqh[i][1]['lat']])		#KO
              #reqf.extend([i])				#Works!

              lng = str(reqh[i][1]['lng'])
              lat = str(reqh[i][1]['lat'])
              lnglat = (lng +' '+ lat)
              reqf.extend([lnglat])				


              updid = reqh[i][0]
              pois.objects.filter(id=updid).update(poi='POINT('+ lnglat +')')
              #pois.objects.filter(id=updid).update(poiname='Ampek')	#Works


           #for e in pois.objects.filter(id__in=reqf):
           #   lnglat = (request.POST['lng'] +' '+ request.POST['lat'])
           #   e.poi = 'POINT('+ lnglat +')'
           #   e.save()


    #Post status to Twitter @DmbHead1
    #twitpost(reqc);			#Works!  Temporarily disabled for localhost

    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def bootstrap_carousel(request, template_name="bootstrap_carousel.html"):
    page_title = 'Bootstrap Carousel'
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def marker_listing(request, template_name="marker_listing.html"):
    page_title = 'Daftar Rumah Makan Padang'

    #q0 = IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(kode_prov=52).geojson
    q0 = WorldBorder.objects.geojson().get(id=225).geojson
 
    qs = '{ "type": "Feature", "id": 0, "properties": { "PROPINSI": "Semua Propinsi", "COUNT": 14000 }, "geometry": '
    qs += q0
    qs += '}'


    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def leaflet_default_map(request, template_name="leaflet_default_map.html"):
    page_title = 'Leaflet Default Map'
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


###Test SSE
from django.http import StreamingHttpResponse
import time

from django.template import loader, Context






def sse(request):				#Fucking Works!
    t = loader.get_template('maplite/sse.html') # or whatever
    buffer = ' ' * 1024

    def gen_rendered():  
        yield t.render(Context({'varname': 'some value', 'buffer': buffer}))
        #                                                 ^^^^^^
        #    embed that {{ buffer }} somewhere in your template 
        #        (unless it's already long enough) to force display

        for x in range(1,11):
            #yield '<p>x = {}</p>{}\n'.format(x, buffer)
            yield '{} x = <br /> {}'.format(x, ' '*1024)
            time.sleep(3)

    #return StreamingHttpResponse(gen_rendered(), mimetype="text/html")
    return StreamingHttpResponse(gen_rendered(), mimetype="text/event-stream")


def test_sse(request, template_name="test_sse.html"):
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def Xtest_sse(request, template_name="sse.html"):
    def event_stream():
        while True:
            time.sleep(3)
            yield 'data: %s\n\n' % 'hola mundo'

    #return StreamingHttpResponse(event_stream(), mimetype="text/event-stream")
    return StreamingHttpResponse(event_stream(), mimetype="text/html")



    #def stream_response_generator():
    #    yield "<html><body>\n"
    #    for x in range(1, 100):
    #        yield "<div>%s</div>\n" % x
    #        yield " " * 10240
    #        time.sleep(1)
    #    yield "</body></html>\n"
 
 
    #def stream_response(request):
    #    resp = StreamingHttpResponse(stream_response_generator(), mimetype='text/html')
    #    return resp


    #return render_to_response(template_name, locals(),context_instance=RequestContext(request))

###/Test SSE

###
def ajaxdatapoint2(request, template_name="ajaxdatapoint2.html"):
    q0 = GeonameAll.objects.get(id=1)

    qs = '{ "type": "Feature", "geometry": '+ q0.pois.geojson +'}'

    #qs = q0.pois.geojson
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def leaflet_clusterpoint2(request, template_name="leaflet_clusterpoint2.html"):
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))
###

def ajaxdatapoint(request, template_name="ajaxdatapoint.html"):
    #q0 = Geoname.objects.filter(id__lte=10).geojson()		#Works
    #q0 = Geoname.objects.filter(id__lte=1000).geojson()
    #q0 = Geoname.objects.geojson().order_by('?')[:2000]		#get 2000 random, so expensive!
    q0 = Geoname.objects.geojson().order_by('?')[:100]			#Temp!

    q1 = '{"type": "FeatureCollection", "features": ['
    
    for i in range(len(q0)):
        #if i == q0[-1]:         #break in Python3, Negative indexing is not supported.
        if i == len(q0)-1:       #put more elegant way, such  if i == "last dict"
          q1 += '{ "type": "Feature", "properties": {"name": "'+ str(q0[i]) +'" }, "geometry": '+ q0[i].geojson +'}]}'

        else:
          q1 += '{ "type": "Feature", "properties": {"name": "'+ str(q0[i]) +'" }, "geometry": '+ q0[i].geojson +'},'

    qs = q1


    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def leaflet_ajaxdatapoint(request, template_name="leaflet_ajaxdatapoint.html"):
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def leaflet_clusterpoint(request, template_name="leaflet_clusterpoint.html"):
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))
def leaflet_landingpage(request, template_name="leaflet_landingpage.html"):
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))



###

def ajaxdata(request, req_type, kode_prov, template_name="ajaxdata.html"):
    #with param; reqtype in text and kode_prov in numeric
    #req_type can be geojson/peta, kode_prov can be 91 not 91A!
    qs = ''		#initialize qs
    #function to fetch json data during leaflet map init

    def mapinit():
        #jsondata = "init jsondata"

        json_dict = IndonesiaProvince.objects.all().values('propinsi', 'kode_prov')
        jsondata = {}
        q0 = []

        for item in json_dict:

            #jsondata = json_dict			#result dict
            #jsondata = item['kode_prov']		#result 12
            #jsondata = len(json_dict)			#OK, result 33
	    #jsondata += 1              		#result 33
            #jsondata += {item['kode_prov']}		#leads

            q0 += ['{ "PROPINSI": '+ item['propinsi'] +', "KODE_PROV": '+ item['kode_prov'] +', "COUNT": '+ item['kode_prov'] +' }']

        jsondata = json.dumps(q0)
        return jsondata


    if (kode_prov == '00'):
        #means leaflet map just been initialized, set Indonesia bbox as as full map.
	#fetch ONLY bbox, propinsi, kode_prov for each province. NOT including geom objects!
        req_type = 'Leaflet map initialised!'


        qs = mapinit()
        #return render_to_response(template_name, locals(),context_instance=RequestContext(request))

    else:
        qs = 'kode_prov <> 00, and req_type is not geojson/peta'
        if (req_type=='geojson'):
            #fetch only geom object based on kode_prov supplied

            q0 = IndonesiaProvince.objects.geojson().get(kode_prov=kode_prov).geojson
            prop_name = IndonesiaProvince.objects.values_list('propinsi', flat=True).get(kode_prov=kode_prov)


            qs = '{ "type": "Feature", "properties": { "PROPINSI": "'+ prop_name +'", "COUNT": 300 }, "geometry": '
            qs += q0
            qs += '}'




            #return render_to_response(template_name, locals(),context_instance=RequestContext(request))

        if (req_type=='peta'):
            #fetch other than geojson objects (like what?)
            qs = 'kode_prov <> 00, and req_type is peta'
            #return render_to_response(template_name, locals(),context_instance=RequestContext(request))


    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def leaflet_ajaxdata(request, template_name="leaflet_ajaxdata.html"):
    #this function init without calling ajaxdata, later call ajaxdata function which supply geojson or other Ajax data

    #qs = list(IndonesiaProvince.objects.all().values('propinsi', 'kode_prov'))
    #qs = simplejson.dumps(list(IndonesiaProvince.objects.all().values('id', 'propinsi', 'kode_prov')))
    qs = json.dumps(list(IndonesiaProvince.objects.all().values('id', 'propinsi', 'kode_prov')))

    return render_to_response(template_name, locals(),context_instance=RequestContext(request))
###

def mapdata3(request, template_name="mapdata3.html"):             ##Start from HEREEEE!

    json_dict = IndonesiaProvince.objects.all().values('propinsi', 'kode_prov')
    jsondata = {}
    q0 = []

    for item in json_dict:
            q0 += ['{"PROPINSI":'+item['propinsi']+',"KODE_PROV":'+item['kode_prov']+',"COUNT": '+item['kode_prov']+'}']

    qs = q0[22]

    return render_to_response(template_name, locals(),context_instance=RequestContext(request))



def mapdata2(request, template_name="mapdata2.html"):

    q0 = '{ "type": "Feature", "id": 1, "properties": { "PROPINSI": "Bali", "COUNT": 2300 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=1).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 2, "properties": { "PROPINSI": "Banten", "COUNT": 400 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=2).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 3, "properties": { "PROPINSI": "DI Yogyakarta", "COUNT": 600 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=3).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 4, "properties": { "PROPINSI": "DKI Jakarta", "COUNT": 1000 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=4).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 5, "properties": { "PROPINSI": "Jambi", "COUNT": 1300 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=5).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 6, "properties": { "PROPINSI": "Jawa Barat", "COUNT": 800 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=6).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 7, "properties": { "PROPINSI": "Jawa Tengah", "COUNT": 400 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=7).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 8, "properties": { "PROPINSI": "Jawa Timur", "COUNT": 1500 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=8).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 9, "properties": { "PROPINSI": "Kalimantan Barat", "COUNT": 500 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=9).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 10, "properties": { "PROPINSI": "Kep. Bangka Belitung", "COUNT": 300 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=10).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 11, "properties": { "PROPINSI": "Aceh", "COUNT": 900 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=11).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 12, "properties": { "PROPINSI": "Nusa Tenggara Barat", "COUNT": 1500 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=12).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 13, "properties": { "PROPINSI": "Papua Barat", "COUNT": 900 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=13).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 14, "properties": { "PROPINSI": "Sulawesi Barat", "COUNT": 3000 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=14).geojson
    q0 += '},'
  
    q0 += '{ "type": "Feature", "id": 15, "properties": { "PROPINSI": "Sulawesi Selatan", "COUNT": 900 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=15).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 16, "properties": { "PROPINSI": "Sulawesi Utara", "COUNT": 1200 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=16).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 17, "properties": { "PROPINSI": "Riau", "COUNT": 700 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=17).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 18, "properties": { "PROPINSI": "Sumatera Barat", "COUNT": 5400 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=18).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 19, "properties": { "PROPINSI": "Kep. Riau", "COUNT": 200 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=19).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 20, "properties": { "PROPINSI": "Maluku Utara", "COUNT": 100 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=20).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 21, "properties": { "PROPINSI": "Lampung", "COUNT": 800 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=21).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 22, "properties": { "PROPINSI": "Maluku", "COUNT": 1200 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=22).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 23, "properties": { "PROPINSI": "Nusa Tenggara Timur", "COUNT": 1400 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=23).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 24, "properties": { "PROPINSI": "Sulawesi Tenggara", "COUNT": 1900 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=24).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 25, "properties": { "PROPINSI": "Kalimantan Tengah", "COUNT": 900 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=25).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 26, "properties": { "PROPINSI": "Kalimantan Selatan", "COUNT": 200 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=26).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 27, "properties": { "PROPINSI": "Kalimantan Timur", "COUNT": 700 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=27).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 28, "properties": { "PROPINSI": "Bengkulu", "COUNT": 1200 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=28).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 29, "properties": { "PROPINSI": "Sumatera Selatan", "COUNT": 300 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=29).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 30, "properties": { "PROPINSI": "Gorontalo", "COUNT": 100 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=30).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 31, "properties": { "PROPINSI": "Sulawesi Tengah", "COUNT": 5500 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=31).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 32, "properties": { "PROPINSI": "Papua", "COUNT": 700 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=32).geojson
    q0 += '},'
    q0 += '{ "type": "Feature", "id": 33, "properties": { "PROPINSI": "Sumatera Utara", "COUNT": 3400 }, "geometry": '
    q0 += IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(id=33).geojson
    q0 += '}'

    qs = q0

    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def leaflet_propinsi(request, template_name="leaflet_propinsi.html"):
    #this function call mapdata2 function, holds geojson
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))



def leaflet_custom(request, kode_prov, template_name="leaflet_custom.html"):
    page_title = 'Map Custom'


    q0 = IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(kode_prov=kode_prov).geojson
    prop_name = IndonesiaProvince.objects.values_list('propinsi', flat=True).get(kode_prov=kode_prov)

    qs = '{ "type": "Feature", "id": 0, "properties": { "PROPINSI": "'+ prop_name +'", "COUNT": 4300 }, "geometry": '
    qs += q0
    qs += '}'

    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def mapdata(request, kode_prov, template_name="mapdata.html"):
    q0 = IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(kode_prov=kode_prov).geojson
    prop_name = IndonesiaProvince.objects.values_list('propinsi', flat=True).get(kode_prov=kode_prov)

    #qs = q0

    qs = '{"type": "FeatureCollection","features": ['
    qs += '{ "type": "Feature", "id": 0, "properties": { "PROPINSI": "'+ prop_name +'", "COUNT": 300 }, "geometry": '
    qs += q0
    qs += '}'
    qs += ']}'

    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def leaflet_bbox(request, template_name="leaflet_bbox.html"):
    #this function call mapdata function, holds geojson
    page_title = 'Map BBox'
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def leaflet_indonesia(request, template_name="leaflet_indonesia.html"):
    page_title = 'Map Indonesia'

    #q0 = IndonesiaProvince.objects.geojson(crs=True, bbox=True).get(kode_prov=52).geojson
    q0 = WorldBorder.objects.geojson().get(id=225).geojson
 
    qs = '{ "type": "Feature", "id": 0, "properties": { "PROPINSI": "Semua Propinsi", "COUNT": 14000 }, "geometry": '
    qs += q0
    qs += '}'


    return render_to_response(template_name, locals(),context_instance=RequestContext(request))



