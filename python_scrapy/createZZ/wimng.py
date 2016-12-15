#! /usr/bin/env python
#coding=utf-8

import sys
from function import *

def create_wimng_backup(project = '',version = ''):
    wimng_para = CLID_DATA_PATH +'%sBACKUP_SW_%s' %(get_clid_data_path(project),version)
    wimng_url = WEB_URL + 'create_wimng_auto.php?version_path=%s' %(wimng_para)
    print wimng_url

    br = login()
    br.open(wimng_url)
    return br.response().read()
    
if __name__ == '__main__':
#    create_wimng_backup('idol3cn','7T1Z')
    print str(sys.argv) + 'BEGIN'
    if len(sys.argv)==3:
        create_wimng_backup(sys.argv[1],sys.argv[2])
    else:
        print 'Parameters error!'
    print str(sys.argv) + 'END'
