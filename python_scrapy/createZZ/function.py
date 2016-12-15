#! /usr/bin/env python
#coding=utf-8

import cookielib
import mechanize
import MySQLdb
from warnings import filterwarnings
import MySQLdb as Database
from datetime import *


#define constant 
WEB_URL = 'http://172.16.11.176/clid/software/clid/php/'
CLID_DATA_PATH = '/web/data/htdocs/clid/data/clid_data/'

def connection_db(db_name='bigbrother'):
    filterwarnings('ignore',category = Database.Warning)
    try:
        mysqlConn = MySQLdb.connect(host = '172.16.11.176',
                                    user = 'toolsng',
                                    passwd = 'cnep1m2ppMSbsm',
                                    db = db_name,
                                    port = 3306,
                                    charset = 'utf8')
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    cur = mysqlConn.cursor()
    return cur

def login():
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    #Browser
    br = mechanize.Browser()
    br.set_cookiejar(cj)

    #options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    #Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #User-Agent 
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11')] 

    br.open(WEB_URL + 'post.php')
    br.select_form(nr = 0)
    br.form['login'] = 'clid_auto'
    br.form['password'] = ''
    resp = br.submit()
    return br

def get_perso_type(project = '',version = ''):
    cur = connection_db()
    try:
        query = "SELECT * FROM t_web_create_perso WHERE project = '%s' \
                                                  and version = '%s' \
                                                  and (state = '7' \
                                                  or isdone='1')" \
                                                  % (project,version);
        cur.execute(query)
        fetchList = cur.fetchone()
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    if not fetchList:
        return 'new'
    else:
        return 'update'

def get_family_name(project = ''):
    cur = connection_db()
    try:
        query = "SELECT clid_data_path FROM t_web_project_conf WHERE project_name = '%s'" % (project);
        cur.execute(query)
        fetchList = cur.fetchone()
        clid_data_path = str(fetchList[0])
        famuly_name = clid_data_path.split('/')[0]
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    return famuly_name

def is_version_exist(project = '',version = '',perso_num = ''):
    cur = connection_db()
    try:
        query = "SELECT id FROM t_web_create_perso WHERE project='%s' \
                                                   and version='%s' \
                                                   and perso_num='%s' \
                                                   and isdone=0" \
                                                   % (project,version,perso_num);
        cur.execute(query)
        fetchList = cur.fetchone()
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    if fetchList:
        return True
    return False

def is_user_exist(user = ''):
    cur = connection_db()
    try:
        query = "SELECT * FROM t_web_user where user='%s'" % (user);
        cur.execute(query)
        fetchList = cur.fetchone()
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    if fetchList:
        return True
    return False

def get_clid_username(email = ''):
    cur = connection_db('db_clid')
    try:
        query = "SELECT user_name FROM t_user where email='%s'" % (email);
        cur.execute(query)
        fetchList = cur.fetchone()
        user_name = str(fetchList[0])
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    return user_name

def get_product_id(product_name = ''):
    cur = connection_db()
    try:
        product_name = product_name.lower()
        query = "SELECT ID_product FROM t_product WHERE product_name='%s'" % (product_name);
        cur.execute(query)
        fetchList = cur.fetchone()
        if not fetchList:
            return False
        product_id = str(fetchList[0])
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    return product_id            

def insert_create_table(project = '',version='',perso_num='',user = '',step = 0,current='',pre_version='',product_id='',command=''):
    if step:
        lock_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur = connection_db()
        try:
            query = "INSERT INTO t_web_create_perso (project,\
                                                     version,\
                                                     perso_num,\
                                                     operator,\
                                                     step,\
                                                     islocked,\
                                                     locked_time,\
                                                     current,\
                                                     pre_version,\
                                                     product_id,\
                                                     creatzz_command)\
                    VALUES('%s','%s','%s','%s',%s,'1','%s','%s','%s','%s','%s')"\
                           %(project,\
                             version,\
                             perso_num,\
                             user,\
                             step,\
                             lock_time,\
                             current,\
                             pre_version,\
                             product_id,\
                             command);
            print 'query: ' + ' '.join(query.split())
            result = cur.execute(query)
            insert_id = int(cur.lastrowid)
            cur.close()
        except MySQLdb.Error, e:
            try:
                sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error:%s" % str(e)
        if result:
            return insert_id
        else:
            return 0
    else:
        return 0

def update_table_msg(t_id = '0',msg = ''):
    if t_id != 0:
        try:
            cur = connection_db()
            query = "UPDATE t_web_create_perso SET comments='%s' where id='%s'" %(msg,t_id);
            cur.execute(query)
            cur.close()
        except MySQLdb.Error, e:
            try:
                sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error:%s" % str(e)

def get_clid_data_path(project = ''):
    cur = connection_db()
    try:
        query = "SELECT clid_data_path FROM t_web_project_conf WHERE project_name='%s'" % (project);
        cur.execute(query)
        fetchList = cur.fetchone()
        clid_data_path = str(fetchList[0])
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    return clid_data_path

def get_createzz_id(project = '',version = ''):
    cur = connection_db()
    try:
        query = "SELECT id FROM t_web_create_perso WHERE project='%s' \
                                                   and version='%s' \
                                                   ORDER BY id DESC" \
                                                   % (project,version);
        cur.execute(query)
        fetchList = cur.fetchone()
        createzz_id = str(fetchList[0])
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    return createzz_id

def check_createzz_status(createzz_id = ''):
    cur = connection_db()
    try:
        query = "SELECT isdone,state FROM t_web_create_perso WHERE id='%s'" % (createzz_id);
        cur.execute(query)
        fetchList = cur.fetchone()
        isdone = str(fetchList[0])
        state = str(fetchList[1])
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    print 'isdone: ' + isdone + ' state: ' + state
    if isdone == '1' and state == '3':
        return True
    return False

def check_diff_status(createzz_id = ''):
    cur = connection_db()
    try:
        query = "SELECT compare_version FROM t_web_create_perso WHERE id='%s'" % (createzz_id);
        cur.execute(query)
        fetchList = cur.fetchone()
        compare_version = str(fetchList[0])
        cur.close()
    except MySQLdb.Error, e:
        try:
            sqlError =  "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error:%s" % str(e)
    if compare_version == 'None':
        return False
    return True
