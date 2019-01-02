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
        url = "http://localhost:4242"
        self.send_response(200)
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        #print post_data
        if(str(post_data)=="Student"):
            print "\n***************************************************"
            print "**** THE SERVER IS WAITING FOR THE AUTHENTICATION ****"
            print "***************************************************\n"

            post_req = urllib2.Request(url, "Student")
            response = urllib2.urlopen(post_req)
        elif((str(post_data).split(' '))[0]=="StudentID"):
            print "###### Authentication Started ######"
            print "ID : ",
            print str((str(post_data).split())[1])
            studentID = int(str((str(post_data).split())[1]))

            post_req = urllib2.Request(url, "StudentID "+str(studentID))
            response = urllib2.urlopen(post_req)
        elif((str(post_data).split(' '))[0]=="StudentPWD"):
            print "PASSWORD : ",
            print str((str(post_data).split())[1])
            print "###### Authentication Ended ######"
            studentPWD = (str(post_data).split())[1]

            #Envoie de la demande d'autentification au serveur dédié
            post_req = urllib2.Request(url, "StudentPWD "+studentPWD)
            response = urllib2.urlopen(post_req)



        # self.send_header("Content-type", "text/html")
        #
        # self.end_headers()
        #
        # self.wfile.write("<html><head><title>Title goes here.</title></head>")
        #
        # self.wfile.write("<body><p>This is a test.</p>")
        #
        # self.wfile.write("<p>You accessed path: %s</p>" % self.path)
        #
        # self.wfile.write("</body></html>")
        # print xml.dom.minidom.parseString(post_data).toxml()
        # faire la difference sur qui envoie le fichier pour savoir l'action a faire
        # test si ID existe puis si unique enregistrer le XML
        # verification avec xpath

        #envoie OK OU KO au redacteur




if __name__ == '__main__':
    print "Gestionnaire QCM Started"
    httpd = HTTPServer(('localhost', 8282), SimpleHTTPRequestHandler)
    httpd.serve_forever()
