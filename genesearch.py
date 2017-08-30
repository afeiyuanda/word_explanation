#!/usr/bin/python
# -*-coding:utf-8-*-

#python 字符串操作方法合集 https://my.oschina.net/golang/blog/209208,http://www.runoob.com/python/python-strings.html
#字符串的操作可以引入 string 这个模块

"""这是一个命令行程序，该程序主要是更gene_id（基因ID）或者target_id（目标基因）来获取数据

Usage:

python genesearch.py FILE_PATH KEY OUTPUT_PATH [CLICK_TYPE]
python genesearch.py --file-path FILE_PATH --key KEY --output-path OUTPUT_PATH [--click-type CLICK_TYPE]

--file-path 结题报告根目录绝对路径（Web_Report目录）
--key 基因id或者是目标基因，搜索关键字
--output-path 结果输出目录，文件内容为json字符串
--click-type [可选参数]默认值为id，表示更加基因id搜索

"""

import fire
import csv
import json

def parameter(file_path, key, output_path, click_type='id'):
  if click_type == 'id':
    search_id(file_path, key, output_path)
  else:
    search_target_gene(file_path, key, output_path)



# 使用 ID 搜索小RNA数据
def search_id(file_path, key, outputpath):
  result = {}
  with open(file_path + '/miRNA_pos.list', 'r') as f:
    line = __getline(f, '#miRNA_ID', key)
    result['locatoin_info'] = line

  with open(file_path + '/miRNA_mature.fa', 'r') as f:
    flag = False
    sequence_result = {}
    for line in f:
      if not flag and line.startswith('>') and line[1:].strip().lstrip() == key:
        flag = True
        sequence_result['id'] = line
      elif flag:
        sequence_result['sequence'] = line
        break
    result['sequence_info'] = sequence_result

  write_result(outputpath, json.dumps(result))



# 匹配列并得到结果
def __getline(f, keyword, key):
  lines = csv.DictReader(f, delimiter='\t')
  for line in lines:
    if line[keyword] == key:
      return line



# Target_gene （目标基因）搜索srna数据
def search_target_gene(file_path, key, outputpath):
  result = {}
  with open(file_path + '/gene_pos.list', 'r') as f:
    line = __getline(f, '#Gene', key)
    result['location_info'] = line

  with open(file_path + '/Target_Predict/All.target_gene.fa', 'r') as f:
    flag = False
    sequence_result = {}
    for line in f:
      if not flag and line.startswith('>') and key in line:
        flag = True
        sequence_result['id'] = line
      elif flag:
        sequence_result['sequence'] = line
        break
    result['sequence_info'] = sequence_result

  with open(file_path + '/Target_Anno/Integrated_Function.annotation.xls', 'r') as f:
    line = __getline(f, '#GeneID', key)
    result['anno_info'] = line

  write_result(outputpath, json.dumps(result))



# 将结果文件写入指定文件
def write_result(outputpath, json):
  f = open(outputpath, 'w')
  f.write(json)
  f.close()



def main():
  fire.Fire(parameter)

if __name__ == '__main__':
  main()