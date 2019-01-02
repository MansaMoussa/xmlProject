#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''
from urlparse import parse_qs
import xml.sax
from xml.dom.minidom import getDOMImplementation
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import xml.etree.ElementTree as ET

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h1>Hello, world!</h1>")

    def do_POST(self):
        self.send_response(200)
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data[0:])
        print type(data)
        #reception de la correction et enregistrement a faire dans un fichier
        #faire la difference sur qui envoie le fichier pour savoir l'action a faire
        if data["type"][0] == "sendCorrection":
            print "creer fichier correct"
            xmla = data["xmldata"][0]

            tree = ET.fromstring(xmla)

            id = tree.find(".//Identifiant").text

            fichier = open(id + "correc.xml", "a")
            fichier.write(xmla)
            fichier.close()

        #print xml.dom.minidom.parseString(post_data).toxml()




if __name__ == '__main__':
    print "test"
    httpd = HTTPServer(('localhost', 8383), SimpleHTTPRequestHandler)
    httpd.serve_forever()
