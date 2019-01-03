#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''

import xml.sax
from lxml import etree
import xml.etree.ElementTree as ET
from xml.dom.minidom import getDOMImplementation
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import parse_qs
import urllib
import urllib2


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
        myDB = make_xml()
        myfile = etree.parse("auth.xml")



        if str(data["type"][0])=="authEtudiant":
            print "\n*******************************************************"
            print "**** THE SERVER START CHECKING THE AUTHENTICATION ****\n"
            print "*******************************************************\n"
            print myfile.xpath('./Student[@id=\"'+str(data["StudentID"][0])+'\"][@pwd=\"'+str(data["StudentPWD"][0])+'\"]').values()
            # Envoie de la demande d'autentification au serveur dédié
            if not not myfile.xpath('./Student[@id=\"'+str(data["StudentID"][0])+'\"][@pwd=\"'+str(data["StudentPWD"][0])+'\"]'):
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #id formation mat1 mat2 ...
                self.wfile.write(str(data["StudentID"][0])+" "+myfile.xpath('/EtudiantsIsncrits/Student[@id_formation]')+" "+mat)
                #self.wfile.write("OK")
                print "The ID ",
                print data["StudentID"],
                print " AND The PASSWORD ",
                print data["StudentPWD"],
                print " EXIST"
            else :
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("KO")
                print "The ID ",
                print data["StudentID"],
                print " OR The PASSWORD ",
                print data["StudentPWD"],
                print " DOES NOT EXIST"

            print "#########################################"

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
    myfile = open("auth.xml", "w")
    myfile.write(newdoc.toprettyxml())

    return newdoc.toprettyxml()


if __name__ == '__main__':
    print "Authentication Server Started"
    httpd = HTTPServer(('localhost', 4242), SimpleHTTPRequestHandler)
    # myDB = make_xml()
    # print "iciciciciic"
    # me = etree.parse("auth.xml")
    # print me.xpath('/EtudiantsIsncrits/Student[@id="1"][@pwd="topSecret"]')
    # print "iciciciciic"
    httpd.serve_forever()
