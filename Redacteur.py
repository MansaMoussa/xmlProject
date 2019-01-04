#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''

import urllib
import urllib2
from xml.dom.minidom import getDOMImplementation


def make_xml():
    impl = getDOMImplementation()
    impl2 = getDOMImplementation()
    #creation du document reponse correction qui sera envoyé a gestionnaire_Correction
    documentCopieReponse = impl2.createDocument(None, "Reponse", None)
    rootNodeReponse = documentCopieReponse.documentElement
    rootNodeReponse.setAttribute("type", "correction")
    idNodeReponse = documentCopieReponse.createElement('Identifiant')
    idQuestionnaire = raw_input('Quelle id voulez vous mettre a ce questionnaire?')

    idQuestionnaireText = documentCopieReponse.createTextNode(idQuestionnaire)
    idNodeReponse.appendChild(idQuestionnaireText)
    rootNodeReponse.appendChild(idNodeReponse)

    # creation du document Questionnaire qui sera envoyé a gestionnaire_QCM
    documentQuestionnaire = impl.createDocument(None, "QCM", None)
    rootNodeQuestionnaire = documentQuestionnaire.documentElement
    NodeQuestionnaire = documentQuestionnaire.createElement('Questionnaire')
    NodeQuestionnaire.setAttribute("id", idQuestionnaire)
    NodeQuestionnaire.setAttribute("id_formation",  raw_input('Quelle id de formation voulez vous mettre pour ce questionnaire?'))
    NodeQuestionnaire.setAttribute("id_matiere", raw_input('Quelle id de matiere voulez vous mettre pour ce questionnaire?') )
    rootNodeQuestionnaire.appendChild(NodeQuestionnaire)

    try:
        nbquestion = int(raw_input('Combien de question voulez vous?'))
        while True:
            if nbquestion > 0:
                break
            else:
                nbquestion = int(raw_input('Réponse non approprié, combien de question voulez vous?'))
    except ValueError:
       print "Veuillez choisir un nombre pour le prochain test"
       exit(-1)


    contenuNodeReponse = documentQuestionnaire.createElement("contenu")

    # creation des différentes questions

    # debut de la boucle while de question
    cpt = 0;
    while nbquestion > cpt:
        # creation question pour reponse
        questionNodeReponse = documentQuestionnaire.createElement("Question")
        questionNodeReponse.setAttribute("id", str(cpt))
        # creation question pour questionnaire
        questionNodeQuestionnaire = documentQuestionnaire.createElement("Question")
        questionNodeQuestionnaire.setAttribute("id", str(cpt))
        # enonce pour questionnaire
        newnode3 = documentQuestionnaire.createElement("Enonce")
        text = documentQuestionnaire.createTextNode(raw_input('Entrez une question : '))
        newnode3.appendChild(text)
        questionNodeQuestionnaire.appendChild(newnode3)

        cpt = cpt + 1


        try:
            nbReponse = int(raw_input('Combien de réponse voulez vous ?'))
            while True:
                if nbReponse > 0:
                    break
                else:
                    nbReponse = int(raw_input('Réponse non approprié, combien de réponse voulez vous ?'))
        except ValueError:
            print "Veuillez choisir un nombre pour le prochain test"
            exit(-1)

        cptReponse = 0

        while nbReponse > cptReponse:
            # choix pour les differente reponse
            choixNode = documentQuestionnaire.createElement("choix")
            choixNode.setAttribute("id", str(cptReponse))
            textChoix = documentQuestionnaire.createTextNode(raw_input('Entrez une reponse: '))
            choixNode.appendChild(textChoix)

            cptReponse = cptReponse + 1
            questionNodeQuestionnaire.appendChild(choixNode)

        # demande de bonne reponse et mise en place de la reponse dans le bon endroit
        questionNodeReponse.setAttribute("rep", raw_input('Quelle était l\'id de la bonne reponse? (La première réponse est l\id est égale à 0, la deuxième réponse l\'id est égale à  1'))
        contenuNodeReponse.appendChild(questionNodeReponse)
        NodeQuestionnaire.appendChild(questionNodeQuestionnaire)
    rootNodeReponse.appendChild(contenuNodeReponse)
    return documentQuestionnaire.toprettyxml(), documentCopieReponse.toprettyxml()


if __name__ == '__main__':
    url = "http://localhost:8282"
    urlCorrection ="http://localhost:8383"
    data, dataReoponse = make_xml()

    post_dict = {'type': 'sendQuestionnaire','xmldata': data}
    param = urllib.urlencode(post_dict)
    post_req = urllib2.Request(url,param)
    response = urllib2.urlopen(post_req)
    response_data = response.read()
    response.close()
   # print response_data
    if response_data == "OK":
        # envoie des données au correcteur
        post_dict = {'xmldata': dataReoponse, 'type': "sendCorrection"}
        #print post_dict
        param = urllib.urlencode(post_dict)
        #print param
        post_req = urllib2.Request(urlCorrection, param)
        response = urllib2.urlopen(post_req)
        #   print "a envoyer xml"
    else:
        print "L'id envoyé existe déjà dans notre base de donnée"
    # si ok envoyer les réponses au gestionnaire QCM sinon ne rien faire
