#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''

import urllib
import urllib2
import pika
import xml.sax
from xml.sax import saxutils
from xml.dom.minidom import getDOMImplementation



class InkscapeSvgHandler(xml.sax.ContentHandler):
    enonce = False

    #POUR POUVOIR LE DOM DANS LE SAX
    impl = getDOMImplementation()
    newdocreponse = impl.createDocument(None, "Reponse", None)
    newrootreponse = newdocreponse.documentElement
    newrootreponse.setAttribute("type", "copie")
    newnodereponse2 = None;
    newrootreponse=None
    newnodecontenureponse=None


    def startDocument(self):
        self.newrootreponse = self.newdocreponse.documentElement
        a=idEtu
        newnodecontenureponse3 = self.newdocreponse.createElement("Etudiant")
        newnodecontenureponse3.setAttribute("id", idEtu)
        self.newrootreponse.appendChild(newnodecontenureponse3)
        self.newnodecontenureponse = self.newdocreponse.createElement("contenu")
        pass

    def endDocument(self):
        # newrootreponse.appendChild(newnodecontenureponse)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='xml')
        channel.basic_publish(exchange='',
                              routing_key='xml',
                              body=self.newdocreponse.toprettyxml())
        connection.close()
        print self.newdocreponse.toprettyxml()
        pass

    def startElement(self, name, attrs):
        # print "oui"
        # print type(name)
        # print type(attrs)

        # prendre id questionnaire aussi
        if name == "Questionnaire":
            # print "question"
            # print attrs._attrs
            idQuestionnaire = attrs.getValue("id")
            print 'id Questionnaire :' + idQuestionnaire
            # print idQuestionnaire
            # mettre dans le DOM l'identifiant
            newnodereponse = self.newdocreponse.createElement('Identifiant')
            text = self.newdocreponse.createTextNode(idQuestionnaire)
            newnodereponse.appendChild(text)
            self.newrootreponse.appendChild(newnodereponse)

        if name == "Question":
            self.newnodereponse2 = self.newdocreponse.createElement("Question")
            # newnodereponse2 = newdocreponse.createElement("Question")
            # print "question"
            # print attrs._attrs
            idQuestion = attrs.values()
            print 'id question :' + idQuestion[0]
            self.newnodereponse2.setAttribute("id", str(idQuestion[0]))

        if name == "choix":
            idReponse = attrs.values()
            print "id = " + idReponse[0] + " reponse=",
            # self.characters(name)

    # print attrs

    def endElement(self, name):
        if name == "Question":
            #print "fin de question"
            num = raw_input('Veuillez entrer l\'id de la reponse (0.1.2...)')
            #print self.newrootreponse.toprettyxml()
            self.newnodereponse2.setAttribute("rep", num)
            #print self.newrootreponse.toprettyxml()
            self.newnodecontenureponse.appendChild(self.newnodereponse2)
            #print self.newrootreponse.toprettyxml()
            self.newrootreponse.appendChild(self.newnodecontenureponse)
        # newnodereponse2 = newdocreponse.createElement("Question")
        # newnodereponse2 = newdocreponse.createElement("Question")

    def characters(self, content):
        content = content.strip('\n')
        content = saxutils.unescape(content)
        content = content.strip('\t')
        if len(content) > 0:
            print content

if __name__ == '__main__':
    url = "http://localhost:8282"
    print "######/!\\ Authentification réquise avant de recevoir un QCM /!\\######"


    idEtu = raw_input('Veuillez entrer votre numero etudiant : ')
    pwdEtu = raw_input('Veuillez entrer votre password : ')
    post_dict = {'type': "authEtudiant", 'StudentID': str(idEtu),'StudentPWD':str(pwdEtu)}

    param = urllib.urlencode(post_dict)
    post_req = urllib2.Request(url, param)
    response = urllib2.urlopen(post_req)
    response_data = response.read()

    if (str(response_data)!="KO" and str(response_data.split(' ')[0]).isdigit()) or str(response_data)!="OK" :
        print "Authentication succeded"
        print response_data
        # A list that contains the id of the qcm and the id of the matiere
        list_response_received = response_data
        qcm_choix = ""
        matiere_choix = ""

        for i in range(list_response_received.count(';')):
            tmp = list_response_received.split(';')[i]
            print tmp
            qcm_choix = str(tmp.split()[0])
            matiere_choix = str(tmp.split()[1])
            print "Vous avez la possibilité de choisir le QCM ayant l'ID "+qcm_choix+" correspondant à la matière "+matiere_choix

        qcm_choix = raw_input('Veuillez choisir l\'ID du QCM souhaitez faire : ')


        # parser = xml.sax.make_parser()
        # parser.setContentHandler(InkscapeSvgHandler())
        # parser.parse(open("1.xml", "r"))
    elif (str(response_data)=="KO"):
        print "Authentication failed"
    else :
        print "/!\\ Aucun QCM destiné à vous n'a été créé ! :( /!\\"

    response.close()
