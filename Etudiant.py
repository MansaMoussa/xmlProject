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


    idEtu = raw_input('Veuillez entrer votre numero etudiant : ')
    pwdEtu = raw_input('Veuillez entrer votre password : ')
    post_dict = {'type': "authEtudiant", 'StudentID': str(idEtu),'StudentPWD':str(pwdEtu)}

    param = urllib.urlencode(post_dict)
    post_req = urllib2.Request(url, param)
    response = urllib2.urlopen(post_req)

    #post_req = urllib2.Request(url, "StudentID "+str(idEtu))
    #response = urllib2.urlopen(post_req)


    #post_req = urllib2.Request(url, "StudentPWD "+str(pwdEtu))
    #response = urllib2.urlopen(post_req)

    response.close()
