from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'maplite.views.landingpage_with_panel', name='landingpage_with_panel'),
    url(r'^alt/$', 'maplite.views.alt_landingpage', name='alt_landingpage'),
    url(r'^home/$', 'maplite.views.home', name='home'),

    url(r'^marker_detail/$', 'maplite.views.marker_detail', name='marker_detail'),
    url(r'^marker_listing/$', 'maplite.views.marker_listing', name='marker_listing'),

    url(r'^bootstrap_carousel/$', 'maplite.views.bootstrap_carousel', name='bootstrap_carousel'),
    url(r'^makemarker/$', 'maplite.views.makemarker', name='makemarker'),
    url(r'^alt_makemarker/$', 'maplite.views.alt_makemarker', name='alt_makemarker'),
   url(r'^makemarker_handler/(?P<req_type>\w+)/(?P<kode_prov>\d+)/$', 'maplite.views.makemarker_handler', name='makemarker_handler'),

    url(r'^leaflet_default_map/$', 'maplite.views.leaflet_default_map', name='leaflet_default_map'),

    #url(r'^leaflet_propinsi/$', 'maplite.views.leaflet_propinsi', name='leaflet_propinsi'),
    #url(r'^$', 'maplite.views.leaflet_propinsi', name='leaflet_propinsi'),


    url(r'^leaflet_indonesia/$', 'maplite.views.leaflet_indonesia', name='leaflet_indonesia'),

    url(r'^ajaxdata/(?P<req_type>\w+)/(?P<kode_prov>\d+)/$', 'maplite.views.ajaxdata', name='ajaxdata'),
    url(r'^leaflet_ajaxdata/$', 'maplite.views.leaflet_ajaxdata', name='leaflet_ajaxdata'),


    url(r'^leaflet_custom/(?P<kode_prov>\d+)/$', 'maplite.views.leaflet_custom', name='leaflet_custom'),

    url(r'^mapdata/(?P<kode_prov>\d+)/$', 'maplite.views.mapdata', name='mapdata'),
    url(r'^leaflet_bbox/$', 'maplite.views.leaflet_bbox', name='leaflet_bbox'),

    url(r'^mapdata2/$', 'maplite.views.mapdata2', name='mapdata2'),
    url(r'^leaflet_propinsi/$', 'maplite.views.leaflet_propinsi', name='leaflet_propinsi'),

    url(r'^mapdata3/$', 'maplite.views.mapdata3', name='mapdata3'),

    url(r'^ajaxdatapoint/$', 'maplite.views.ajaxdatapoint', name='ajaxdatapoint'),
    url(r'^leaflet_ajaxdatapoint/$', 'maplite.views.leaflet_ajaxdatapoint', name='leaflet_ajaxdatapoint'),
    url(r'^leaflet_clusterpoint/$', 'maplite.views.leaflet_clusterpoint', name='leaflet_clusterpoint'),


    # url(r'^maplite/', include('maplite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
