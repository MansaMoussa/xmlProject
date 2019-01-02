#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''

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
        self.send_response(200)
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        #print post_data
        if((str(post_data).split(' '))[0]=="Student"):
            print post_data
            print "\n*******************************************************"
            print "**** THE SERVER START CHECKING THE AUTHENTICATION ****\n"
            print "*******************************************************\n"
        elif((str(post_data).split(' '))[0]=="StudentID"):
            studentID = int((str(post_data).split(' '))[1])
            print "The ID ( "+ str(studentID),
            print ") EXIST"
        elif((str(post_data).split(' '))[0]=="StudentPWD"):
            studentPWD = (str(post_data).split(' '))[1]
            print "The PASSWORD ( "+ studentPWD,
            print ") EXIST"



def make_xml():
    impl = getDOMImplementation()
    impl2 = getDOMImplementation()

    # newdocreponse = impl2.createDocument(None, "reponse", None)
    # newrootreponse = newdocreponse.documentElement
    # newnodereponse = newdocreponse.createElement('identifiant')
    # # QUE METTRE EN IDENTIFIANT?????????? mcomment mettre en place avec formation et matiere?
    # text = newdocreponse.createTextNode("test")
    # newnodereponse.appendChild(text)
    # newrootreponse.appendChild(newnodereponse)

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
