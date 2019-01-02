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

    newdocreponse = impl2.createDocument(None, "reponse", None)
    newrootreponse = newdocreponse.documentElement
    newnodereponse = newdocreponse.createElement('identifiant')
    # QUE METTRE EN IDENTIFIANT?????????? mcomment mettre en place avec formation et matiere?
    text = newdocreponse.createTextNode("test")
    newnodereponse.appendChild(text)
    newrootreponse.appendChild(newnodereponse)

    newdoc = impl.createDocument(None, "QCM2", None)
    newroot = newdoc.documentElement
    # creation questionnaire
    newnode = newdoc.createElement('Questionnaire')

    newnode.setAttribute("id", "5")
    newnode.setAttribute("id_formation", "5")
    newnode.setAttribute("id_matiere", "test")
    newroot.appendChild(newnode)
    # creation des différentes questions

    # debut de la boucle while de question
    cpt = 0;
    nbquestion = int(raw_input('Combien de question voulez vous?'))
    newnodecontenureponse = newdoc.createElement("contenu")

    while nbquestion > cpt:
        # creation question pour reponse
        newnodereponse2 = newdoc.createElement("Question")
        newnodereponse2.setAttribute("id", str(cpt))
        # creation question pour questionnaire
        newnode2 = newdoc.createElement("Question")
        newnode2.setAttribute("id", str(cpt))
        # enonce pour questionnaire
        newnode3 = newdoc.createElement("Enonce")
        text = newdoc.createTextNode(raw_input('Entrez une question : '))
        newnode3.appendChild(text)
        newnode2.appendChild(newnode3)

        cpt = cpt + 1
        nbReponse = int(raw_input('Combien de réponse voulez vous ?'))
        cptReponse = 0

        while nbReponse > cptReponse:
            # choix pour les differente reponse
            newnodechoix = newdoc.createElement("choix")
            newnodechoix.setAttribute("id", str(cptReponse))
            text = newdoc.createTextNode(raw_input('Entrez une reponse: '))
            newnodechoix.appendChild(text)
            # creation reponse boucle while et a la fin de la boucle while demandé le numéro de la réponse
            cptReponse = cptReponse + 1
            newnode2.appendChild(newnodechoix)
        # demande de bonne reponse et mise en place de la reponse dans le bon endroit
        newnodereponse2.setAttribute("rep", raw_input('Quelle était l\'id de la bonne reponse? '))
        newnodecontenureponse.appendChild(newnodereponse2)
        newnode.appendChild(newnode2)
    newrootreponse.appendChild(newnodecontenureponse)
    print newdocreponse.toprettyxml()
    #  print newdoc.toxml()
    return newdoc.toprettyxml(), newdocreponse.toprettyxml()


if __name__ == '__main__':
    url = "http://localhost:8282"
    data, dataReoponse = make_xml()
    # print data
    post_dict = {'xmldata': data,'type': "sendQuestionnaire"}

    print post_dict
    param = urllib.urlencode(post_dict)
    print param
    post_req = urllib2.Request(url,param)
    response = urllib2.urlopen(post_req)

    # print post_dict
    # print post_dict
    # params = urllib.urlencode(post_dict)
    # print params
    # params =urllib.parse.urlencode(post_dict, urllib.qu)
    # params = urllib.quote(params,'+')
    # print params
    # bin=params.encode('utf-8')
    # print bin
    # post_req = urllib2.Request(url, bin)

    #    response = urllib2.urlopen(post_req)

    response_data = response.read()
    print response_data
    response.close()
    print response_data
    if response_data == 200:
        # envoie des données au correcteur
        print "a envoyer xml"

    # si ok envoyer les réponses au gestionnaire QCM sinon ne rien faire
