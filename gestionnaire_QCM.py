#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''
import os
import glob
from lxml import etree
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
            # print t["test"]
            # print type(t["xmldata"][0])
            # print xml.dom.minidom.parseString( t["xmldata"][0]).toxml()
            # les donnees qui sont dans la variable data sera un dictionnaire,
            # prendre data pour la suite
            if str(data["type"][0])=="sendQuestionnaire":
                # print "faire verif questionnaire"

                xmla = data["xmldata"][0]
                tree = ET.fromstring(xmla)
                list = tree.find(".//Questionnaire/[@id]").attrib
                id = list["id"]
                if self.verificationQuestionnaire(id):
                    print "creer fichier"
                    fichier = open(id + ".xml", "a")
                    fichier.write(xmla)
                    fichier.close()

                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write("OK")
                else:
                    self.send_header("Content-type", "text/html")

                    self.end_headers()
                    self.wfile.write("KO")


            elif str(data["type"][0])=="authEtudiant":
                print "\n******************************************************"
                print "**** THE SERVER IS WAITING FOR THE AUTHENTICATION ****"
                print "******************************************************\n"
                print "###### Authentication Started ######"
                print "ID : ",
                print data["StudentID"][0]
                print "PASSWORD : ",
                print "*"*len(data["StudentPWD"][0])

                studentID = int(data["StudentID"][0])
                studentPWD = data["StudentPWD"][0]

                # Envoie de la demande d'autentification au serveur dédié
                post_dict = {'type': "authEtudiant", 'StudentID': str(studentID),'StudentPWD':str(studentPWD)}
                param = urllib.urlencode(post_dict)
                post_req = urllib2.Request(url, param)
                response = urllib2.urlopen(post_req)
                response_data = response.read()
                print response_data
                if(len(response_data)>=3):
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    qcm_proposition = ""
                    splited_response_data = response_data.split(' ')
                    id_student = splited_response_data[0]
                    id_formation = splited_response_data[1]
                    xml_files = [f for f in glob.glob("*.xml")]
                    for i in range(len(xml_files)) :
                        prefix_file_name = xml_files[i].split('.xml')[0]
                        if str(prefix_file_name).isdigit() :
                            myfile = etree.parse(str(xml_files[i]))
                            for j in range(2,len(splited_response_data)) :
                                if not not myfile.xpath('/QCM2/Questionnaire[@id=\"'+str(prefix_file_name)+'\"][@id_formation=\"'+str(id_formation)+'\"][@id_matiere=\"'+str(splited_response_data[j])+'\"]'):
                                    # l'id du questionnaire + l'id de la matiere
                                    qcm_proposition =qcm_proposition+str(prefix_file_name)+" "+str(splited_response_data[j])+";"
                    # Une proposition de qcm est envoyé à l'étudiant
                    self.wfile.write(qcm_proposition)
                else :
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("KO")
                response.close()
                print "###### Authentication Ended ######"
            else:
                print "Ne rien faire"



        # print xml.dom.minidom.parseString(test).toxml()
        # print xml.dom.minidom.parseString(post_data).toxml()
        # faire la difference sur qui envoie le fichier pour savoir l'action a faire
        # test si ID existe puis si unique enregistrer le XML
        # verification avec xpath

        #envoie OK OU KO au redacteur

    def verificationQuestionnaire(self,id):
        for i in os.listdir(os.getcwd()):
            if i == (str(id)+".xml"):
                print "deja connu"
                return False

        return True

if __name__ == '__main__':
    print "Gestionnaire QCM Server Started"
    httpd = HTTPServer(('localhost', 8282), SimpleHTTPRequestHandler)
    httpd.serve_forever()
