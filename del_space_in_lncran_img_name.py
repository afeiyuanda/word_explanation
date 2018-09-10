#-*- coding=utf-8 -*-
#!/usr/bin/env python
import re,os,sys,argparse
from os.path import getsize
import shutil, Image

def convert_pic(path,out,workDir,wMax=1000.):
    try:
        img = Image.open(workDir+'/'+path)
        w,h=img.size
        if w > wMax:
            r=wMax/w*100
            #sys.stdout.write("start: convert -resize %s%%x%s%% %s %s \n" %(r,r,workDir+'/'+path,out))
            os.system("convert -resize %s%%x%s%% %s %s " %(r,r,workDir+'/'+path,out))
        else:
            shutil.copyfile(workDir+'/'+path, out)   
    except IOError:
        #sys.stderr.write("file: %s not find!!! \n"%(workDir+'/'+path))
        #shutil.copyfile(path,out)
        pass

if __name__ == '__main__':
    description = 'Generate small images!\n'
    quick_usage = 'python '+sys.argv[0]+' -web_report path/to/Web_Report/\n'
    newParser = argparse.ArgumentParser( description = description, usage = quick_usage );
    newParser.add_argument( '-web_report', dest='web_report', help='Web_Report path',required=True );
    
    args = newParser.parse_args();
    argsDict = args.__dict__;
    
    web_report = argsDict['web_report']
    

    if os.path.exists(web_report+'/configtest.xml') and getsize( web_report+'/configtest.xml' ) != 0:
        xml = web_report+'/configtest.xml'
    elif os.path.exists(web_report+'/configtest_raw.xml') and getsize( web_report+'/configtest_raw.xml' ) != 0:
        xml = web_report+'/configtest_raw.xml'
    else:
        print "%s/configtest(_raw).xml is not exists, please check!!!" % web_report
        exit(0)
    
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

