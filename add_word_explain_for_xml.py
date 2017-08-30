#-*- coding=utf-8 -*-
#!/usr/bin/env python
import re,os,sys,argparse

if __name__ == '__main__':
    description = 'Add word explanation!\n'
    quick_usage = 'python '+sys.argv[0]+' -web_report app_word.txt\n'
    newParser = argparse.ArgumentParser( description = description, usage = quick_usage );
    newParser.add_argument( '-word_db', dest='word_db', help='ref to the word db file, tab separated txt file', default=sys.path[0]+'/all_word_db_app.txt' );
    newParser.add_argument( '-web_report', dest='web_report', help='Web_Report path',required=True );
    newParser.add_argument( '-fenc', dest='fenc', help='xml encoding: utf-8,gbk, default=utf-8',default='utf-8' );
    
    args = newParser.parse_args();
    argsDict = args.__dict__;
    
    wor_db = argsDict['word_db']
    web_report = argsDict['web_report']
    fenc = argsDict['fenc']
    
    #print 'ssh 10.3.129.88 "/share/nas2/genome/biosoft/Python/2.7.8/bin/python '+sys.path[0]+'/add_word_explain_for_xml_core.py -web_report '+web_report+'"'
    #os.system('ssh 10.3.129.88 "/share/nas2/genome/biosoft/Python/2.7.8/bin/python '+sys.path[0]+'/add_word_explain_for_xml_core.py -web_report '+web_report+'"')
    os.system('ssh cloudpub@10.3.1.62 "/share/nas2/genome/biosoft/Python/2.7.8/bin/python '+sys.path[0]+'/add_word_explain_for_xml_core.py -web_report '+web_report+'"')
    #os.system('echo $HOSTNAME')
