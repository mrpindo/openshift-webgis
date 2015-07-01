#!/usr/bin/env python
import imp
import os, os.path
import urllib.parse
import sys		

import cherrypy
from cherrypy.process import plugins

import django
from django.conf import settings

if 'OPENSHIFT_REPO_DIR' in os.environ:    
    ON_OPENSHIFT = True
else:
    ON_OPENSHIFT = False


#from django.core.handlers.wsgi import WSGIHandler		#moved to #53

from httplogger import HTTPLogger

__all__ = ['DjangoAppPlugin']


class DjangoAppPlugin(plugins.SimplePlugin):
    def __init__(self, bus, settings_module='maplite.settings', wsgi_http_logger=HTTPLogger):
        """ CherryPy engine plugin to configure and mount
        the Django application onto the CherryPy server.
        """
        plugins.SimplePlugin.__init__(self, bus)

        if ON_OPENSHIFT:
            sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/maplite'))
            os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
        else:
            sys.path.append('/home/endik/Documents/WorkSpace/Python/endikApp/VENV/OPENSHIFT/mapp/wsgi/maplite')
            os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

        self.wsgi_http_logger = wsgi_http_logger


    def start(self):
        """ When the bus starts, the plugin is also started
        and we load the Django application. We then mount it on
        the CherryPy engine for serving as a WSGI application.
        We let CherryPy serve the application's static files.
        """
        cherrypy.log("Loading and serving the Django application")



        from django.core.handlers.wsgi import WSGIHandler
        cherrypy.tree.graft(self.wsgi_http_logger(WSGIHandler()))	
        #settings = self.load_settings()		##Fucked Up!

        # App specific static handler
        #### 
        if ON_OPENSHIFT:
            static_handler = cherrypy.tools.staticdir.handler(
                section="/",
                dir="",
                root=os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/static/')
            )
        else:
            static_handler = cherrypy.tools.staticdir.handler(
                section="/",
                dir="static",
                root="/home/endik/Documents/WorkSpace/Python/endikApp/VENV/OPENSHIFT/mapp/wsgi/"
            )

            config = {'/':
                {
                    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                    'tools.trailing_slash.on': False,
                }
            }

        #cherrypy.tree.mount(Root(), "/", config=config)
        #hack for localhost
        cherrypy.tree.mount(static_handler, settings.STATIC_URL)

        # Admin static handler. From django's internal (django.core.servers.basehttp)
        admin_static_dir = os.path.join(django.__path__[0], 'contrib', 'admin', 'static')
        admin_static_handler = cherrypy.tools.staticdir.handler(
            section='/',
            dir='admin',
            root=admin_static_dir
        )
        cherrypy.tree.mount(admin_static_handler, urllib.parse.urljoin(settings.STATIC_URL, 'admin'))

    def load_settings(self):
        """ Loads the Django application's settings. You can
        override this method to provide your own loading
        mechanism. Simply return an instance of your settings module.
        """
        name = os.environ['DJANGO_SETTINGS_MODULE']

        package, mod = name.rsplit('.', 1)
        fd, path, description = imp.find_module(mod, [package.replace('.', '/')])

        try:
            return imp.load_module(mod, fd, path, description)
        finally:
            if fd: fd.close()
