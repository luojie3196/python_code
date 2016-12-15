#! /usr/bin/env python
#coding=utf-8

import sys
import re
from function import *
from diff import *

def build(project = '',version = '',pre_version = '',email = ''):
    #Get clid user
    user = get_clid_username(email)
    #Compare version
    ret = diff(project,version,pre_version)
    if not ret:
       exit('Version compare failed!')

    #Login
    br = login()
    version_para = 'path=' + CLID_DATA_PATH + '%sBACKUP_SW_%s' % (get_clid_data_path(project),version)
    version_url = WEB_URL + 'main.php?%s' % (version_para)
    print version_url
    br.open(version_url)

    #export zip
    export_para = 'family=%s&project=%s&version=%s' %(get_family_name(project),project.upper(),version)
    export_url = WEB_URL + 'create_zz_output_auto.php?%s' %(export_para)
    print export_url
    br.open(export_url)
    export_info=br.response().read()

    #get export zip file path
    for line in export_info.split('\n'):
        if re.search(r'^X:/MOD_\S+_NEW/BACKUP_SW_\S+/\S+ZZ/zz_\S+',line):
            zipname_path=line
            break
    if not zipname_path:
        exit('Can not find export zip file!')

    #submit zip to bigbrother
    submit_para = 'user=%s&zipname=%s' %(user,zipname_path)
    submit_url = WEB_URL + "submit_perso.php?%s" %(submit_para)
    print submit_url
    br.open(submit_url)
    br.select_form(nr = 0)
    br.submit()
    
if __name__ == '__main__':
#    build('idol3cn','7TM6','7TM5','jieluo@tcl.com')
    print str(sys.argv) + 'BEGIN'
    if len(sys.argv)==5:
        build(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        print 'Parameters error!'
    print str(sys.argv) + 'END'





