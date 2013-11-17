import os
from subprocess import Popen
import cherrypy

class Root(object):
    def index(self):
        Popen(['python', 'model.py'])
        return 'Hooray! Generating the next tweet as a subprocess.'
    index.exposed = True

cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
cherrypy.quickstart(Root())
