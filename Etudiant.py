#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''

import urllib
import urllib2
import pika
import time
import xml.sax
from xml.sax import saxutils
from xml.dom.minidom import getDOMImplementation



class InkscapeSvgHandler(xml.sax.ContentHandler):

    #Creation des differente composante dom pour envoyer la copie de l'etudiant
    impl = getDOMImplementation()
    newdocreponse = impl.createDocument(None, "Reponse", None)
    newrootreponse = newdocreponse.documentElement
    newrootreponse.setAttribute("type", "copie")
    newnodereponse2 = None;
    newnodecontenureponse=None


    def startDocument(self):
        #creation de la balise etudiant pour sauvegarder l id de l etudiant
        newnodecontenureponse3 = self.newdocreponse.createElement("Etudiant")
        newnodecontenureponse3.setAttribute("id", idEtu)
        self.newrootreponse.appendChild(newnodecontenureponse3)
        self.newnodecontenureponse = self.newdocreponse.createElement("contenu")
        pass

    def endDocument(self):
        #envoie de la copie a l'etudiant via rabbitMQ
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
        #Lecture de chaqua balise avec le parser sax
        if name == "Questionnaire":
            idQuestionnaire = attrs.getValue("id")
            print 'id Questionnaire :' + idQuestionnaire
            newnodereponse = self.newdocreponse.createElement('Identifiant')
            text = self.newdocreponse.createTextNode(idQuestionnaire)
            newnodereponse.appendChild(text)
            self.newrootreponse.appendChild(newnodereponse)

        if name == "Question":
            #creation d'une balise question pour chaque question
            self.newnodereponse2 = self.newdocreponse.createElement("Question")
            idQuestion = attrs.values()
            print 'id question :' + idQuestion[0]
            self.newnodereponse2.setAttribute("id", str(idQuestion[0]))

        if name == "choix":
            #affichage de la reponse et de son text via characters(content)
            idReponse = attrs.values()
            print "id = " + idReponse[0] + " reponse=",


    def endElement(self, name):
        #a chaque question, demande a l'utilisateur de rentrer la réponse
        if name == "Question":
            num = raw_input('Veuillez entrer l\'id de la reponse (0.1.2...)')
            self.newnodereponse2.setAttribute("rep", num)
            self.newnodecontenureponse.appendChild(self.newnodereponse2)
            self.newrootreponse.appendChild(self.newnodecontenureponse)


    def characters(self, content):
        #n'affiche que du text non vide
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

    if ((str(response_data)!="KO" and str(response_data.split(' ')[0]).isdigit()) or str(response_data)=="OK") :
        print "Authentication succeded"
        #print response_data
        # A list that contains the id of the qcm and the id of the matiere
        list_response_received = response_data
        qcm_choix = ""
        matiere_choix = ""

        info_score = str(raw_input('souhaitez-vous connaître vos scores précedents ? :[Oui] ou [Non] '))

        if(info_score=="Oui" or info_score=="O" or info_score=="oui" or info_score=="o" or info_score=="Yes" or info_score=="yes" or info_score=="y"):
            post_dict = {'type': "info_score", 'StudentID': str(idEtu)}

            # Envoie de la demande des scores
            param = urllib.urlencode(post_dict)
            post_req = urllib2.Request(url, param)
            response = urllib2.urlopen(post_req)
            response_data = response.read()

            id_qcm = ""
            id_score = ""

            print "####################################"
            print "############ SCOREBOARD ############"
            print "####################################"
            if str(response_data)!="Vous n'avez fait aucun QCM :(" or str(response_data)!="Aucun QCM n'a encore été effectué :)":
                for i in range(response_data.count(';')):
                    tmp = response_data.split(';')[i]
                    #print tmp
                    id_qcm = str(tmp.split()[0])
                    id_score = str(tmp.split()[1])
                    print "Vous avez obtenu un score de "+id_score+" au QCM ayant l'ID "+id_qcm
            else :
                print response_data
            time.sleep(1)
            print "####################################\n"



        for i in range(list_response_received.count(';')):
            tmp = list_response_received.split(';')[i]
            #print tmp
            qcm_choix = str(tmp.split()[0])
            matiere_choix = str(tmp.split()[1])
            print "Vous avez la possibilité de choisir le QCM ayant l'ID "+qcm_choix+" correspondant à la matière "+matiere_choix

        qcm_choix = raw_input('Veuillez choisir l\'ID du QCM que souhaitez faire : ')
        #init et lancement du parser sur le questionnaire qcm
        parser = xml.sax.make_parser()
        parser.setContentHandler(InkscapeSvgHandler())
        parser.parse(open(qcm_choix+".xml", "r"))
    elif (str(response_data)=="KO"):
        print "Authentication failed"
    else :
        print "/!\\ Aucun QCM destiné à vous n'a été créé ! :( /!\\"

    response.close()
