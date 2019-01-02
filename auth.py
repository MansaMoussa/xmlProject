#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''

import urllib
import xml.sax
from xml.dom.minidom import getDOMImplementation
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import parse_qs
import urllib
import urllib2
import xml.sax
from xml.dom.minidom import getDOMImplementation
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h1>Hello, world!</h1>")

    def do_POST(self):
        url = "http://localhost:8282"
        self.send_response(200)
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data[0:])


        if str(data["type"][0])=="authEtudiant":
            print "\n*******************************************************"
            print "**** THE SERVER START CHECKING THE AUTHENTICATION ****\n"
            print "*******************************************************\n"
            print "The ID ",
            print data["StudentID"],
            print " EXIST"
            print "The PASSWORD ",
            print data["StudentPWD"],
            print " EXIST"
            studentID = int(data["StudentID"][0])
            studentPWD = data["StudentPWD"][0]
            print "#########################################"
            # Envoie de la demande d'autentification au serveur dédié
            if True:
                post_dict = {'type': "authAnswer", 'studentSubscription': "True"}
                param = urllib.urlencode(post_dict)
                post_req = urllib2.Request(url, param)
                response = urllib2.urlopen(post_req)
            else :
                post_dict = {'type': "authAnswer", 'studentSubscription': "False"}
                param = urllib.urlencode(post_dict)
                post_req = urllib2.Request(url, param)
                response = urllib2.urlopen(post_req)



def make_xml():
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "EtudiantsIsncrits", None)
    newroot = newdoc.documentElement
    # creation de la base de donnée des étudiants inscrits
    etu1 = newdoc.createElement('Student')

    etu1.setAttribute("id", "1")
    etu1.setAttribute("pwd", "topSecret")
    etu1.setAttribute("id_formation", "3")
    etu1.setAttribute("id_matiere", "PenTest")
    newroot.appendChild(etu1)

    etu2 = newdoc.createElement('Student')

    etu2.setAttribute("id", "7")
    etu2.setAttribute("pwd", "Secretdefense")
    etu2.setAttribute("id_formation", "5")
    etu2.setAttribute("id_matiere", "Network")
    newroot.appendChild(etu2)

    etu3 = newdoc.createElement('Student')

    etu3.setAttribute("id", "42")
    etu3.setAttribute("pwd", "gr4ndR3ims")
    etu3.setAttribute("id_formation", "3")
    etu3.setAttribute("id_matiere", "PenTest")
    newroot.appendChild(etu3)

    print newdoc.toprettyxml()

    return newdoc.toprettyxml()


if __name__ == '__main__':
    print "Authentication Server Started"
    httpd = HTTPServer(('localhost', 4242), SimpleHTTPRequestHandler)
    myDB = make_xml()
    httpd.serve_forever()
