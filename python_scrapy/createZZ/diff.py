#! /usr/bin/env python
#coding=utf-8

import sys
from function import *


def diff(project = '',version = '',pre_version = ''):
    pid = get_createzz_id(project.upper(), version)
    if not check_createzz_status(pid):
        exit('CreateZZ status not ready!')

    if not check_diff_status(pid):
        clid_data_path = get_clid_data_path(project)
        product_para = 'path=' + CLID_DATA_PATH + '%s' % (clid_data_path)
        product_url = WEB_URL + 'main.php?%s' % (product_para)
        print product_url

        br = login()
        br.open(product_url)

        diff_para = 'soft1=%sBACKUP_SW_%s&soft2=%sBACKUP_SW_%s&pid=%s' % (clid_data_path,version,clid_data_path,pre_version,pid)
        diff_url = WEB_URL + 'main_print_soft_diff.php?%s' % (diff_para)
        print diff_url
        br.open(diff_url)
        if check_diff_status(pid):
            print 'Version compare successfully.'
            return True
        else:
            return False
    else:
        print 'Version compare exist!'
        return True
    
if __name__ == '__main__':
#    diff('idol3','7SSX','7SSW')
    print str(sys.argv) + 'BEGIN'
    if len(sys.argv)==4:
        diff(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        print 'Parameters error!'
    print str(sys.argv) + 'END'
