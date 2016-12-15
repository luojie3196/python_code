#! /usr/bin/env python
#coding=utf-8

import sys
import re
from function import *
from wimng import *

def check_para(project = '',version = '',pre_version = '',email = ''):
    #Get clid user
    user=get_clid_username(email)
    #check perso product name if exist
    if not get_product_id(project):
        print project + ' project does not exist!'
        exit(0)
    #check version and pre_version if match
    if pre_version != '' and version != '':
        pre_2s = pre_version[:2]
        ver_2s = version[:2]
        if pre_2s != ver_2s:
            print 'Please check ' + version + ' and ' + pre_version + ' if match!'
    #check user if exist
    if not is_user_exist(user):
        print user + ' is invalid!'

def create_zz_perso(project = '',version = '',pre_version = '',email = ''):
    user=get_clid_username(email)
    p_type = get_perso_type(project.upper(),version)
    perso_num = version[-1]
    current_name = 'current'
    family_name = get_family_name(project)

    command = ''
    if p_type == 'update':
        current_name = ''
        perso_num = ''
        command = command + '-update '
        command = command + '-soft ' + version + ' -f ' + family_name

    if p_type == 'new':
	    command = command + '-new '
	    command = command + '-soft ' + version + ' -f ' + family_name

	    if pre_version != '' and version != '':
		    pre_3s = pre_version[:3]		
		    ver_3s = version[:3]
		    if pre_3s != ver_3s:
			    command = command + ' -p ' + pre_version
			
	    if current_name != 'current' and current_name != '':
		    command = command + ' -c ' + current_name

    pattern = r'^-new\s-soft\s+\S+.-f\s\S+family\s*|^-update\s-soft\s+\S+.-f\s\S+family'
    if re.search(pattern,command):
        if not is_version_exist(project.upper(),version,perso_num):
            product_id = get_product_id(project)
            if product_id:
                insert_id = insert_create_table(project.upper(),version,perso_num,user,'2',current_name,pre_version,product_id,command)
                if insert_id:
                    modid = ''
                    msg_r = 'project:' + project.upper() + ',modid:' + modid + ',command:' + command + ',create_perso_id:'+ str(insert_id) + '.'
                    repo_msg = 'env:' + msg_r
                    msg_w = create_wimng_backup(project,version)
                    wim_msg = 'wimng:' + msg_w
                    msg = wim_msg + '+' + repo_msg
                    print 'msg: ' + msg
                    update_table_msg(insert_id,msg)
                else:
                    print 'insert table error!'
            else:
                print 'the project does not find!'    
        else:
            print 'the perso is compiling by someone!'       
    else:
        print 'the cmd error!'
    
if __name__ == '__main__':
    #create_zz_perso('idol3cn','7T1Z','7T1I','jieluo@tcl.com')
    print str(sys.argv) + 'BEGIN'
    if len(sys.argv)==5:
        check_para(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
        create_zz_perso(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        print 'Parameters are not expected to match!'
    print str(sys.argv) + 'END'





