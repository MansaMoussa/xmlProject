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

        # reception de la correction et enregistrement dans un fichier
        if data["type"][0] == "sendCorrection":
            print "creer fichier correct"
            xmla = data["xmldata"][0]

            tree = ET.fromstring(xmla)

            id = tree.find(".//Identifiant").text

            fichier = open(id + "correc.xml", "w")
            fichier.write(xmla)
            fichier.close()

            # print xml.dom.minidom.parseString(post_data).toxml()


# Classe qui va permettre la gestion de la correction d'une copie
class InkscapeSvgHandler(xml.sax.ContentHandler):
    id = False #permet de detecter le moment ou le programme recupera l'id du questionnaire
    numId = ""# l'id du questionnaire
    fichier = "" #le fichier de correction
    score = 0 #le score de l'étudiant
    total = 0 #le nombre total de question
    idEtu = "" #l'id de l'etudiant

    def startDocument(self):
        pass

    def endDocument(self):

        ##creation du xml a envoyer
        impl = getDOMImplementation()
        newdocreponse = impl.createDocument(None, "Resultat", None)
        newrootreponse = newdocreponse.documentElement
        newnodecontenureponse3 = newdocreponse.createElement("Etudiant")
        newnodecontenureponse3.setAttribute("id", self.idEtu)
        newnodecontenureponse3.setAttribute("score", str(self.score) + "/" + str(self.total))
        newnodecontenureponse3.setAttribute("idQuestionnaire", self.numId)
        newrootreponse.appendChild(newnodecontenureponse3)

        print newdocreponse.toprettyxml()
        # newrootreponse.appendChild(newnodecontenureponse)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='result')
        channel.basic_publish(exchange='',
                              routing_key='result',
                              body=newdocreponse.toprettyxml())
        connection.close()
        pass

    def startElement(self, name, attrs):
        if name == "Etudiant":
            self.idEtu = attrs.getValue("id")
        if name == "Identifiant":
            # detecte que le prochain charactere sera l'id du questionnaire
            self.id = True
        if name == "Question":
            #gestion de la correction
            idQuestion = attrs.getValue("id")
            idRepCopie = attrs.getValue("rep")
            # faire requete xpath et verifier la repcopie et repcorrection
            reponse = self.fichier.xpath(
                "./contenu/Question[@id=\'" + idQuestion + "\' and @rep=\'" + idRepCopie + "\']")
            if reponse != []:
                self.score = self.score + 1

            self.total = self.total + 1

    # print attrs
    def characters(self, content):
        content = content.strip('\n')
        content = saxutils.unescape(content)
        content = content.strip('\t')
        if len(content) > 0:
            if id:
                self.id = False
                self.numId = content
                self.fichier = etree.parse(self.numId + "correc.xml")


# Classe qui va être utilisé pour faire un thread pour la gestion du rabbitMQ
class Thread(threading.Thread):

    def __init__(self):
        super(Thread, self).__init__()
        self.start()


    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='xml')

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            # gestion correction
            xml.sax.parseString(body, InkscapeSvgHandler())

        channel.basic_consume(callback,
                              queue='xml',
                              no_ack=True)

        print(' [*] Waiting for messages(RabbitMQ).')

        channel.start_consuming()


if __name__ == '__main__':
    print "Gestionnaire Correction Server Started(HTTP)"
    # creation d'un thread car 2 fonction bloquante(httpserver et rabbitmq)
    th1 = Thread()

    httpd = HTTPServer(('127.0.0.1', 8383), SimpleHTTPRequestHandler)
    httpd.serve_forever()

    print "apres"
