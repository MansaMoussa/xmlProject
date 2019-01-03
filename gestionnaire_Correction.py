#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''
import threading
import time
from SocketServer import ThreadingMixIn
from urlparse import parse_qs
import xml.sax
from xml.dom.minidom import getDOMImplementation
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import xml.etree.ElementTree as ET
from xml.sax import saxutils

import pika
from lxml import etree
from pika import callback



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
        print data
        print type(data)
        #reception de la correction et enregistrement a faire dans un fichier
        #faire la difference sur qui envoie le fichier pour savoir l'action a faire
        if data["type"][0] == "sendCorrection":
            print "creer fichier correct"
            xmla = data["xmldata"][0]

            tree = ET.fromstring(xmla)

            id = tree.find(".//Identifiant").text

            fichier = open(id + "correc.xml", "w")
            fichier.write(xmla)
            fichier.close()


            #print xml.dom.minidom.parseString(post_data).toxml()


class InkscapeSvgHandler(xml.sax.ContentHandler):
    id=False
    numId=""
    fichier=""
    #contenuFichier=""
    score=0
    total=0
    idEtu=""
    def startDocument(self):

        pass

    def endDocument(self):

        ##creation du xml a envoyer
        impl = getDOMImplementation()
        newdocreponse = impl.createDocument(None, "Resultat", None)
        newrootreponse = newdocreponse.documentElement
        newnodecontenureponse3 = newdocreponse.createElement("Etudiant")
        newnodecontenureponse3.setAttribute("id", self.idEtu)
        newnodecontenureponse3.setAttribute("score", str(self.score)+"/"+str(self.total))
        newnodecontenureponse3.setAttribute("idQuestionnaire", self.numId)
        newrootreponse.appendChild(newnodecontenureponse3)

        #<student  id="idStudent" score="score/total" idQuestionnaire="numId">
        print newdocreponse.toprettyxml()
        # newrootreponse.appendChild(newnodecontenureponse)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='result')
        channel.basic_publish(exchange='',
                              routing_key='result',
                              body=newdocreponse.toprettyxml())
        connection.close()
        print "fin"
        pass

    def startElement(self, name, attrs):
        if name == "Etudiant":
            self.idEtu=attrs.getValue("id")
        if name == "Identifiant":
            self.id=True
            #regarder dans charater l'id
            #prendre l'identifiant pour pouvoir ouvrir le bon fichier
        if name == "Question":
            idQuestion=attrs.getValue("id")
            idRepCopie = attrs.getValue("rep")
            #faire requete xpath et verifier la repcopie et repcorrection
            reponse=self.fichier.xpath("./contenu/Question[@id=\'"+idQuestion+"\' and @rep=\'"+idRepCopie+"\']")
            if reponse!=[]:
                self.score=self.score+1

            self.total=self.total+1
            print "test"


    # print attrs
    def characters(self, content):
        content = content.strip('\n')
        content = saxutils.unescape(content)
        content = content.strip('\t')
        if len(content) > 0:
            if id:
                self.id=False
                self.numId=content
                print content
                self.fichier = etree.parse(self.numId+"correc.xml")





class Thread(threading.Thread):

    def __init__(self,i):
        super(Thread,self).__init__()
        self.start()
        i=i


    def run(self):


        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='xml')

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            #gestion correction
            print type(body)
            parser = xml.sax.make_parser()
            xml.sax.parseString(body, InkscapeSvgHandler())
            #parser.setContentHandler(InkscapeSvgHandler())
            #parser.parseString(body)

        channel.basic_consume(callback,
                              queue='xml',
                              no_ack=True)



        print(' [*] Waiting for messages. To exit press CTRL+C')

        channel.start_consuming()



if __name__ == '__main__':
    print "test"
    th1 = Thread(10)

    httpd = HTTPServer(('127.0.0.1', 8383), SimpleHTTPRequestHandler)
    httpd.serve_forever()

    print "apres"
