#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''

import xml.sax
from xml.dom.minidom import getDOMImplementation
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h1>Hello, world!</h1>")

    def do_POST(self):
        self.send_response("test")
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        #reception de la correction et enregistrement a faire dans un fichier
        #faire la difference sur qui envoie le fichier pour savoir l'action a faire
        print xml.dom.minidom.parseString(post_data).toxml()




if __name__ == '__main__':
    print "test"
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
