#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: MansaMoussa
'''

import urllib
import urllib2

if __name__ == '__main__':
    url = "http://localhost:8282"
    print "######/!\\ Authentification réquise avant de recevoir un QCM /!\\######"
    headerEtu = "Student"
    post_req = urllib2.Request(url, headerEtu)
    response = urllib2.urlopen(post_req)
    response_data = response.read()
    print response_data #Recoir un petit message pour faire beau et montrer l'intéraction avec le serveur contacté

    idEtu = raw_input('Veuillez entrer votre numero étudiant : ')
    post_req = urllib2.Request(url, "StudentID "+str(idEtu))
    response = urllib2.urlopen(post_req)

    pwdEtu = raw_input('Veuillez entrer votre password : ')
    post_req = urllib2.Request(url, "StudentPWD "+str(pwdEtu))
    response = urllib2.urlopen(post_req)

    response.close()
