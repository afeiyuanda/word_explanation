#-*- coding=utf-8 -*-
#!/usr/bin/env python
import re,os,sys,argparse
from collections import OrderedDict
from os.path import getsize
import shutil, Image

# f = open('2017-3-3-All_data_chinese_English.txt')
# lines = f.readlines()
# f.close()
#
# newf = open('all_word_db.txt', 'w')
# for line in lines:
#     line_list = (line.decode('gbk').encode('utf-8')).rstrip().split('\t')
#     newf.write('\t'.join([i.strip() for i in line_list[0:4]])+'\n')
# newf.close()

def format_txt_word_db(word_db='2017-3-3-All_data_chinese_English_app.csv'):
    newf = open('all_word_db_app.txt', 'w')
    for line in open(word_db):
        line_list = line.split('\t')
        newf.write('\t'.join([i.strip() for i in line_list[0:4]])+'\n')
    newf.close()

#format_txt_word_db()

def read_word_db(db_url):
    en_db_dic = {}
    zh_db_dic = {}
    for line in open(db_url):
        #print line
        line_list = line.rstrip('\n').split('\t')
        en = line_list[0]
        zh = line_list[1]
        en_exp = line_list[2]
        try:
            zh_exp = line_list[3]
        except:
            zh_exp = ''

        #zh_exp = line_list[3]
        #if en != '' and en.islower()==False and en.isupper()==False:
            #en_db_dic.setdefault(en, []).append([en, en_exp, zh, zh_exp])
            #en_db_dic.setdefault(en.lower(), []).append([en, en_exp, zh, zh_exp])
            #en_db_dic.setdefault(en.upper(), []).append([en, en_exp, zh, zh_exp])
        #if en != '' and en.islower()==True:
            #en_db_dic.setdefault(en, []).append([en, en_exp, zh, zh_exp])
            #en_db_dic.setdefault(en.upper(), []).append([en, en_exp, zh, zh_exp])
            #en_db_dic.setdefault(en.capitalize(), []).append([en, en_exp, zh, zh_exp])
        #if en != '' and en.upper()==True:
            #en_db_dic.setdefault(en, []).append([en, en_exp, zh, zh_exp])
            #en_db_dic.setdefault(en.lower(), []).append([en, en_exp, zh, zh_exp])
            #en_db_dic.setdefault(en.capitalize(), []).append([en, en_exp, zh, zh_exp])
        if en != '' and '|' in en:
            for i in en.strip().split('|'):
                en_db_dic.setdefault(i, []).append([i, en_exp, zh, zh_exp])
        elif en != '':
            en_db_dic.setdefault(en, []).append([en, en_exp, zh, zh_exp])
        
        if zh != '' and '|' in zh:
            for i in zh.strip().split('|'):
                zh_db_dic.setdefault(i, []).append([i, zh_exp, en, en_exp])
        elif zh != '':
            zh_db_dic.setdefault(zh, []).append([zh, zh_exp, en, en_exp])

    return en_db_dic, zh_db_dic
#英文	中文	英文	中文
def generate_word_dic(db_url):
    (en_db_dic, zh_db_dic) = read_word_db(db_url)
    #print en_db_dic['Nanodrop']
    en_word_dic = {}
    for k,v in en_db_dic.items():
        if len(v) == 1:
            if v[0][1]!='':
                s1 = '&lt;p&gt;'+v[0][1]+'&lt;/p&gt;'
            else:
                s1 = ''
            if v[0][2]!='':
                s2 = '&lt;h3&gt;'+v[0][2]+'&lt;/h3&gt;'
            else:
                s2 = ''
            if v[0][3]!='':
                s3 = '&lt;p&gt;'+v[0][3]+'&lt;/p&gt;'
            else:
                s3 = ''

            if s2 != '':
                title = k+'/'+v[0][2]
                en_word_dic[k] = '&lt;a class=&quot;fa&quot; data-toggle=&quot;popover&quot; tabindex=&quot;0&quot; role=&quot;button&quot; data-placement=&quot;auto bottom&quot; data-container=&quot;body&quot; data-content=&quot;'+s1+s3+'&quot; data-original-title=&quot;'+title+'&quot;  data-html=&quot;true&quot; data-trigger=&quot;focus&quot;&gt;'+k+'&lt;/a&gt;'
            else:
                en_word_dic[k] = '&lt;a class=&quot;fa&quot; data-toggle=&quot;popover&quot; tabindex=&quot;0&quot; role=&quot;button&quot; data-placement=&quot;auto bottom&quot; data-container=&quot;body&quot; data-content=&quot;'+s1+s3+'&quot; data-original-title=&quot;'+k+'&quot;  data-html=&quot;true&quot; data-trigger=&quot;focus&quot;&gt;'+k+'&lt;/a&gt;'  
        else:
            flag = 1
            zh = v[0][2]
            en_exp = ''
            for vv in v:
                if vv[1] != '':
                    en_exp += str(flag)+'.'+vv[1]+'**'
                    flag += 1
                else:
                    en_exp += ''
            flag = 1
            zh_exp = ''
            for vv in v:
                if vv[3] != '':
                    zh_exp += str(flag)+'.'+vv[3]+'**'
                    flag += 1
                else:
                    zh_exp += ''
            exp = [k, en_exp, zh, zh_exp]
            #en_word_dic[k] = '\t'.join([i for i in exp if i!=''])
            #'<a class="fa" data-toggle="popover" tabindex="0" role="button" data-placement="auto bottom" data-container="body" data-content="<p>english</p><h3>GTP酶激活蛋白</h3><p>中文内容</p>" data-original-title="english title"  data-html="true" data-trigger="focus">englishTitle</a>'
            en_word_dic[k] = '&lt;a class=&quot;fa&quot; data-toggle=&quot;popover&quot; tabindex=&quot;0&quot; role=&quot;button&quot; data-placement=&quot;auto bottom&quot; data-container=&quot;body&quot; data-content=&quot;&lt;p&gt;'+en_exp+'&lt;/p&gt;&lt;h3&gt;'+zh+'&lt;/h3&gt;&lt;p&gt;'+zh_exp+'&lt;/p&gt;&quot; data-original-title=&quot;'+k+'&quot;  data-html=&quot;true&quot; data-trigger=&quot;focus&quot;&gt;'+k+'&lt;/a&gt;'

    zh_word_dic = {}
    for k,v in zh_db_dic.items():
        if len(v) == 1:
            if v[0][1]!='':
                s1 = '&lt;p&gt;'+v[0][1]+'&lt;/p&gt;'
            else:
                s1 = ''
            if v[0][2]!='':
                s2 = '&lt;h3&gt;'+v[0][2]+'&lt;/h3&gt;'
            else:
                s2 = ''
            if v[0][3]!='':
                s3 = '&lt;p&gt;'+v[0][3]+'&lt;/p&gt;'
            else:
                s3 = ''
            
            if s2 != '':
                title = k+'/'+v[0][2]
                zh_word_dic[k] = '&lt;a class=&quot;fa&quot; data-toggle=&quot;popover&quot; tabindex=&quot;0&quot; role=&quot;button&quot; data-placement=&quot;auto bottom&quot; data-container=&quot;body&quot; data-content=&quot;'+s1+s3+'&quot; data-original-title=&quot;'+title+'&quot;  data-html=&quot;true&quot; data-trigger=&quot;focus&quot;&gt;'+k+'&lt;/a&gt;'
            else:
                zh_word_dic[k] = '&lt;a class=&quot;fa&quot; data-toggle=&quot;popover&quot; tabindex=&quot;0&quot; role=&quot;button&quot; data-placement=&quot;auto bottom&quot; data-container=&quot;body&quot; data-content=&quot;'+s1+s3+'&quot; data-original-title=&quot;'+k+'&quot;  data-html=&quot;true&quot; data-trigger=&quot;focus&quot;&gt;'+k+'&lt;/a&gt;'               

        else:
            flag = 1
            en = v[0][2]
            en_exp = ''
            for vv in v:
                if vv[3] != '':
                    en_exp += str(flag)+'.'+vv[3]+'**'
                    flag += 1
                else:
                    en_exp += ''
            flag = 1
            zh_exp = ''
            for vv in v:
                if vv[1] != '':
                    zh_exp += str(flag)+'.'+vv[1]
                    flag += 1
                else:
                    zh_exp += ''
            exp = [k, zh_exp, en, en_exp]
            #zh_word_dic[k] = '\t'.join([i for i in exp if i!=''])
            zh_word_dic[k] = '&lt;a class=&quot;fa&quot; data-toggle=&quot;popover&quot; tabindex=&quot;0&quot; role=&quot;button&quot; data-placement=&quot;auto bottom&quot; data-container=&quot;body&quot; data-content=&quot;&lt;p&gt;'+zh_exp+'&lt;/p&gt;&lt;h3&gt;'+en+'&lt;/h3&gt;&lt;p&gt;'+en_exp+'&lt;/p&gt;&quot; data-original-title=&quot;'+k+'&quot;  data-html=&quot;true&quot; data-trigger=&quot;focus&quot;&gt;'+k+'&lt;/a&gt;'

    return en_word_dic, zh_word_dic

#(en_word_dic, zh_word_dic) = generate_word_dic('all_word_db_app.txt')

def write_dic_to_file(d,out_url):
    en_exp = open(out_url, 'w')
    for k,v in d.items():
        en_exp.write(k+' : '+v+'\n')
    en_exp.close()

#write_dic_to_file(en_word_dic, 'en_exp.txt')
#write_dic_to_file(zh_word_dic, 'zh_exp.txt')

#def multiple_replace(text, adict):
    #rx = re.compile('|'.join(map(re.escape, adict)))
    ##rx = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, adict)))
    #def one_xlat(match):
        ##k = match.group(0)
        ##print k
        #global k
        #k = match.group(0)
        #v = adict[match.group(0)]
        ##print k
        #del adict[k]
        #return v
    #return rx.sub(one_xlat, text)

def multiple_replace(text, all_word_dic):
    rx = re.compile('|'.join( ['(?<!\w)'+i+'(?!\w)' for i in all_word_dic]) )
    #rx = re.compile('|'.join(map(re.escape, all_word_dic)))
    #rx = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, adict)))
    global k
    def one_xlat(match):
        #global all_word_dic
        k = match.group(0)
        #print k
        try:
            v = all_word_dic[match.group(0)]
            del all_word_dic[k]
        except:
            v = k
        return v
    return rx.sub(one_xlat, text)

def convert_pic(path,out,workDir,wMax=1000.):
    try:
        img = Image.open(workDir+'/'+path)
        w,h=img.size
        if w > wMax:
            r=wMax/w*100
            #sys.stdout.write("start: convert -resize %s%%x%s%% %s %s \n" %(r,r,workDir+'/'+path,out))
            os.system("convert -resize %s%%x%s%% %s %s " %(r,r,workDir+'/'+path,out))
        else:
            #shutil.copyfile(workDir+'/'+path, out)   
            pass
    except IOError:
        #sys.stderr.write("file: %s not find!!! \n"%(workDir+'/'+path))
        #shutil.copyfile(path,out)
        pass
        
def add_word_exp(xml, fenc):
    xml_bak = xml+'.bak_for_word_exp'
    if os.path.exists(xml_bak):
        pass
    else:
        os.system('mv ' + xml + ' '+xml_bak)
        new_xml = open(xml, 'w')
        (en_word_dic, zh_word_dic) = generate_word_dic(wor_db)
        #print en_word_dic['Nanodrop']
        all_word_dic_no_order = dict(en_word_dic, **zh_word_dic)
        all_word_dic = OrderedDict(sorted(all_word_dic_no_order.items(), key=lambda all_word_dic_no_order:len(all_word_dic_no_order[0]), reverse=True))
        k = ''
        p = re.compile('(.*desc=\")(.*?)(\".*)')
        for line1 in open(xml_bak):
            if fenc == 'utf-8':
                line = line1
            else:
                line = (line1.decode(fenc).encode('utf-8'))
            if p.match(line.rstrip()) and 'pic' not in line and not line.strip().startswith('<h'):
                #print line
                line_parts = p.match(line).groups()
                new_desc = multiple_replace(line_parts[1], all_word_dic)
                try:
                    del all_word_dic[k]
                except:
                    pass
                #print new_desc+'\n'
                new_xml.write(''.join([line_parts[0], new_desc, line_parts[2]])+'\n')
            elif 'report_abstract' in line:
                new_xml.write(multiple_replace(line, all_word_dic))
                
            else:
                new_xml.write(line)
        new_xml.close()
    
#/share/bioCloud/dev/dev_user_data/gy_dev/Personal_data/biomarker_project/reftrans_Actinidia_chinensis_20160908154625/Web_Report
#/share/bioCloud/dev/dev_user_data/gy_dev/Personal_data/biomarker_project/BMK161102-D570
#/share/bioCloud/dev/dev_user_data/gy_dev/Personal_data/biomarker_project/sRNAtrans_cucumis_20161228110247/Web_Report
#/share/bioCloud/dev/dev_user_data/gy_dev/Personal_data/biomarker_project/microbial_20170327/Web_Report
#/share/bioCloud/dev/dev_user_data/gy_dev/Personal_data/biomarker_project/BMK151117_A265-01/Web_Report  长链
#/share/bioCloud/dev/dev_user_data/gy_dev/Personal_data/biomarker_project/HumanReseq_20160525190359/Web_Report
#/share/bioCloud/dev/dev_user_data/gy_dev/Personal_data/biomarker_project/exon_20160611105726/Web_Report 外显子
if __name__ == '__main__':
    description = 'Add word explanation!\n'
    quick_usage = 'python '+sys.argv[0]+' -word_db app_word.txt -xml template.xml -outdir outpud_dir\n'
    newParser = argparse.ArgumentParser( description = description, usage = quick_usage );
    newParser.add_argument( '-word_db', dest='word_db', help='ref to the word db file, tab separated txt file', default=sys.path[0]+'/all_word_db_app.txt' );
    newParser.add_argument( '-web_report', dest='web_report', help='Web_Report path',required=True );
    newParser.add_argument( '-fenc', dest='fenc', help='xml encoding: utf-8,gbk, default=utf-8',default='utf-8' );
    #newParser.add_argument( '-outdir', dest='outdir', help='output directory, default=./',default=os.getcwd() );
    #newParser.add_argument( '-prefix', dest='prefix', help='output file prefix, defalut=configtest',default='configtest' );
    
    args = newParser.parse_args();
    argsDict = args.__dict__;
    
    wor_db = argsDict['word_db']
    web_report = argsDict['web_report']
    fenc = argsDict['fenc']
    #outdir = argsDict['outdir']
    #prefix = argsDict['prefix']
    
    if os.path.exists(web_report+'/configtest_raw.xml') and getsize( web_report+'/configtest_raw.xml' ) != 0:
        xml = web_report+'/configtest_raw.xml'
        add_word_exp(xml, fenc)
    
    if os.path.exists(web_report+'/configtest.xml') and getsize( web_report+'/configtest.xml' ) != 0:
        xml = web_report+'/configtest.xml'
        add_word_exp(xml, fenc)
    
    img_pattern = re.compile(r'(.*path=\")(.*?)(\.(png|jpg))(\".*)')
    for line in open(xml).readlines():
        try:
            img_path = img_pattern.match(line).groups()[1]+img_pattern.match(line).groups()[2]
            img_dir = web_report+'/'+os.path.dirname(img_path)
            #print 'img_dir %s\n' % img_dir
            img_name = os.path.basename(img_pattern.match(line).groups()[1])
            new_img_name = img_name+'_small'+img_pattern.match(line).groups()[2]
            new_img_path = img_dir+'/'+new_img_name
            #print 'new_img_path %s' % new_img_path
            if os.path.exists(new_img_path):
                #print "%s has exists, so don't need to convert!!" % new_img_path
                pass
            else:
                convert_pic(img_path, new_img_path, web_report, wMax=1000.)
        except:
            pass
