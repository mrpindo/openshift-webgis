from django.contrib.gis.db import models

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    #def __unicode__(self):
    def __str__(self):		#Python3
        return self.name


class IndonesiaProvince(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # Indonesia Province shapefile.

    propinsi = models.CharField(max_length=30)
    kode_prov = models.CharField(max_length=2)
    kode = models.IntegerField()


    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    #def __unicode__(self):
    def __str__(self):			#Python3
        return self.propinsi

class Geoname(models.Model):
    geonameid = models.IntegerField()
    name = models.CharField(max_length=200)
    asciiname = models.CharField(max_length=200,null=True)
    alternatenames = models.CharField(max_length=6000,null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    fclass = models.CharField(max_length=1,null=True)
    fcode = models.CharField(max_length=10,null=True)
    country = models.CharField(max_length=2,null=True)
    cc2 = models.CharField(max_length=60,null=True)
    admin1 = models.CharField(max_length=20,null=True)
    admin2 = models.CharField(max_length=80,null=True)
    admin3 = models.CharField(max_length=20,null=True)
    admin4 = models.CharField(max_length=20,null=True)
    population = models.BigIntegerField(null=True)
    elevation = models.IntegerField(null=True)
    gtopo30 = models.IntegerField(null=True)
    timezone = models.CharField(max_length=40,null=True)
    moddate = models.DateTimeField(null=True)

    poi = models.PointField(srid=4326,null=True)
    objects = models.GeoManager()
   
    #def __unicode__(self):
    def __str__(self):			#Python3
        return self.name


class GeonameAll(models.Model):
    allname = models.CharField(max_length=200, null=True)

    pois = models.MultiPointField(srid=4326, null=True)
    objects = models.GeoManager()

    #def __unicode__(self):
    def __str__(self):			#Python3
        return self.allname


class pois(models.Model):
    poiname = models.CharField("PoI Name", max_length=200, null=True)
    poiscore = models.IntegerField("Score made by enthusiast", null=True)
    posteremail = models.EmailField("Person's email who entering PoI", max_length=50, null=True)
    posterphone = models.CharField("Person's phone who entering PoI", max_length=20, null=True)
    useOpenID = models.BooleanField("Whether Person's who entering PoI use openID for authentication", default=False)
    #add more field later
    #
    #
    poi = models.PointField(srid=4326,null=True)
    objects = models.GeoManager()

    def __str__(self):			
        return self.poiname

