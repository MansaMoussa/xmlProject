#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''
import os
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
import xml.etree.ElementTree as ET

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h1>Hello, world!</h1>")

    def do_POST(self):

            url = "http://localhost:4242"
            self.send_response(200)
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data[0:])

            # print post_data
            #  print t["test"]
            # print type(t["xmldata"][0])
            #print xml.dom.minidom.parseString( t["xmldata"][0]).toxml()
            #les donnees qui sont dans la variable data sera un dictionnaire,
            # prendre data pour la suite
            if data["type"][0]=="sendQuestionnaire":
                print "faire verif questionnaire"

                xmla= data["xmldata"][0]
                print xmla
                tree = ET.fromstring(xmla)
                list = tree.find(".//Questionnaire/[@id]").attrib
                id = list["id"]
                if(self.verificationQuestionnaire(id)):
                    print "creer fichier"
                    fichier = open(id+".xml", "a")
                    fichier.write(xmla)
                    fichier.close()

            elif data["type"][0]=="authEtudiant":
                print "faire verif login"
            else:
                print "ne rien faire"




        #print xml.dom.minidom.parseString(test).toxml()
       # print xml.dom.minidom.parseString(post_data).toxml()
        #faire la difference sur qui envoie le fichier pour savoir l'action a faire
        #test si ID existe puis si unique enregistrer le XML
        #verification avec xpath

        #envoie OK OU KO au redacteur

    def verificationQuestionnaire(self,id):
        for i in os.listdir(os.getcwd()):
            if i == (str(id)+".xml"):
                print "deja connu"
                return False

        return True

if __name__ == '__main__':
    print "test"
    httpd = HTTPServer(('localhost', 8282), SimpleHTTPRequestHandler)
    httpd.serve_forever()
