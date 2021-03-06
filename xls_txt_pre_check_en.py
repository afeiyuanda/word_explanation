#!/usr/bin/python  
#-*-coding:utf-8-*-
'''
Author:	Liu wei
Data:	2017.05.26
'''

import os,sys,re
import argparse,subprocess
from collections import defaultdict
from string import letters, digits
import xlrd
import chardet,struct

reload(sys)
sys.setdefaultencoding('utf-8')
check_lines = 3001

# 支持文件类型  
# 用16进制字符串的目的是可以知道文件头是多少字节  
# 各种文件头的长度不一样，少则2字符，长则8字符  
#wps xlsx:504B03040A00
#ms  xlsx:504B030414000
#mac xlsx:504B03041400
def type_list():
	return {
	'D0CF11E0':'xls or doc',
	'504B0304':'xlsx',
	'1F8B0804':'BAM (bam)'}

# 字节码转16进制字符串
def bytes2hex(bytes):  
	num = len(bytes)
	hexstr = u""
	for i in range(num):
		t = u"%x" % bytes[i]
		if len(t) % 2:
			hexstr += u"0"  
		hexstr += t
	return hexstr.upper()
  
# 获取文件类型  
def get_file_type(filename):
	binfile = open(filename, 'rb') # 必需二制字读取
	tl = type_list()
	ftype = 'txt'
	for hcode in tl.keys():  
		numOfBytes = len(hcode) / 2 # 需要读多少字节  
		binfile.seek(0) # 每次读取都要回到文件头，不然会一直往后读取
		try:
			hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节
			#print 'File hbytes is %s' % str(hbytes)
		except:
			#return 'txt'
			pass
		f_hcode = bytes2hex(hbytes)
		#print 'hcode is %s' % str(hcode)
		#print 'File f_hcode is %s' % str(f_hcode)
		#print '=================='
		if f_hcode == hcode:
			ftype = tl[hcode]
			break  
	binfile.close()
	#print ftype
	return ftype

def items_not_all_empty(l):
	flag = 0
	for i in l:
		if i != '':
			flag = 1
			break
	return flag

def shorten_list(l):
	if len(l)>3:
		l = l[0:3]
		l.append('...')
	else:
		l = l
	return l
	
def convert_excel_to_txt(excel_file, logs):
	excel_file_name = os.path.basename(excel_file)
	txt_file = excel_file+'.txt'
	f = open( txt_file, 'w' )
	data = xlrd.open_workbook( excel_file )
	sheets = data.sheets()
	target_sheet = ''
	if len(sheets) == 1:
		target_sheet = sheets[0]
	else:
		for sheet in sheets:
			if excel_file_name == sheet.name:
				target_sheet = sheet
		if 	target_sheet == '':
			target_sheet = sheets[0]
	#print target_sheet.name
	table = data.sheet_by_name( target_sheet.name )
	for row in range(table.nrows):
		line_list = []
		for col in range(table.ncols):
			#try:
			cell_value = str(table.row(row)[col].value).strip()
			line_list.append( cell_value.replace('\t', ' '))
			#except AttributeError:
			#	break
		if items_not_all_empty(line_list):
			f.write( '\t'.join(line_list) + '\n' )
		else:
			pass
	logs.append('We have changed your excel file %s to txt file.' % (excel_file))
	f.close()
	os.system('mv '+excel_file+' '+excel_file+'.xls.bak')
	os.system('mv '+txt_file+' '+excel_file)
	return excel_file

def check_file_encode(file_url):
	f = open(file_url, 'rb')
	result = chardet.detect(f.read())
	return result['encoding']

def check_is_utf8(file_url, logs, errors):
	f = open(file_url)
	try:
		f.read().decode('utf-8')
		utf8_flag = 1
	except:
		utf8_flag = 0
	if utf8_flag == 0:
		#errors.append('%s encoding is not utf8, please modify!' % os.path.basename(file_url))
		errors.append('Input encoding is not utf8, please modify!')
	else:
		logs.append('%s encoding is utf8.' % file_url)
	return logs, errors

def check_chinese_char(input_file, logs, errors):
	china_pattern = re.compile(u'([\u4e00-\u9fa5]+)')
	china_flag = 0
	all_lines = open(input_file).readlines()
	if len(all_lines) < check_lines:
		lines = all_lines
	else:
		lines = all_lines[:check_lines-1]
	for line in lines:
		line = line.strip().decode('utf-8')
		if china_pattern.findall(line):
			#print china_pattern.findall(line)
			china_flag = 1
			break
	if china_flag == 1:
		#errors.append('%s contains chinese character, please modify!' % os.path.basename(input_file))
		errors.append('Chinese character is forbidden!')
	else:
		logs.append('%s does not contain chinese character.' % input_file)
	return logs, errors

def is_empty(input_file, logs, errors):
	if not os.path.exists( input_file ):
		#errors.append('%s does not exists!' % os.path.basename(input_file))
		errors.append('File does not exist!')
	elif os.path.getsize( input_file ) == 0:
		#errors.append('%s is empty!' % os.path.basename(input_file))
		errors.append('Empty file is forbidden!')
	else:
		all_anno_flag = 1
		for line in open(input_file):
			if (not line.startswith('#')) and  not line.startswith(' '):
				all_anno_flag = 0
		if all_anno_flag == 1:
			#errors.append('%s exists, but all lines startswith # or space!' % os.path.basename(input_file))
			errors.append('All lines startswith # or space is forbidden!')
		else:
			logs.append('%s exists, and not empty, not all startswith # or space.' % input_file)
	return logs, errors

def get_duplicates(fields):
	""" Returns duplicates out of a list
	fields:  list of elements to check for duplicates
	"""
	cnt = {}
	for field in fields:
		try:
			cnt[field] += 1
		except KeyError:
			cnt[field] = 1
	return [key for key in cnt.keys() if cnt[key]> 1]

def duplicates_indices(fields):
	""" Gets dictionary of duplicates:locations in a list
	fields:  list of elements to check for duplicates
	"""
	dup, ind = get_duplicates(fields), defaultdict(list)
	for i, v in enumerate(fields):
		if v in dup: ind[v].append(i)
	return ind

def del_empty_lines(lines, logs):
	""" 1. Del empty lines """
	new_lines=[]
	empty_lines_ix = []
	ix_correction = 1
	for line_ix in range(len(lines)):
		if lines[line_ix].strip() == '':
			empty_lines_ix.append(line_ix)
		else:
			new_lines.append(lines[line_ix])
	if not empty_lines_ix:
		logs.append('Do not have empty line in file.')
	else:
		logs.append('Row (%s) is empty, we have delete for you.' % ','.join([str(i+ix_correction) for i in empty_lines_ix]))
	return new_lines, logs

def judge_startswith_tabs_spaces(lines, errors):
	""" 1. 判断每行开头是否为空字符 """
	empty_starts_line_ix = []
	ix_correction = 1
	for line_ix in range(len(lines)):
		if lines[line_ix][0] == ' ' or lines[line_ix][0] == '\t':
			empty_starts_line_ix.append(line_ix)
	if empty_starts_line_ix:
		errors.append('Line(s) %s startswith space!' % ','.join([str(i+ix_correction) for i in shorten_list(empty_starts_line_ix)]))
	return errors

def count_elements(fields):
	""" l = ['a', 'b', 'a']
		d = {'a': 2, 'b': 1}
	"""
	cnt = {}
	for field in fields:
		try:
			cnt[field] += 1
		except KeyError:
			cnt[field] = 1
	return cnt

def judge_line_have_same_cells(lines, sep_char):
	"""如果按照设定分割符分割后，所有行元素数一样，则返回1,否则返回0"""
	if len(lines) == 1:
		return [1]
	elif len(lines) == 2:
		l1_num = len(re.split(sep_char, lines[0].rstrip('\n')))
		l2_num = len(re.split(sep_char, lines[1].rstrip('\n')))
		if l1_num == l2_num:
			return [1]
		else:
			return [0]
	else:
		line_cell_num_list = []
		for line in lines:
			col_num = len(re.split(sep_char, line.rstrip('\n')))
			line_cell_num_list.append(col_num)
		#line_cell_num_list = [3,4,3,3,3]
		#elements_num_dic = {3:4, 4:1}
		elements_num_dic = count_elements(line_cell_num_list)
		normal_line_num = max(elements_num_dic.values())#记录列数正常的行数
		for k,v in elements_num_dic.items():
			if v == normal_line_num:
				col_num = k # 记录正常的列数
				break
		abnormal_line_num = [key for key in elements_num_dic.keys() if elements_num_dic[key]!=normal_line_num]
		#print 'col_num is %s' % col_num
		#print abnormal_line_num
		
		if abnormal_line_num==[]:
			#print "lines have same cells"
			return [1]
		else:
			abnormal_line_ids = []
			for i in range(len(line_cell_num_list)):
				if line_cell_num_list[i] != col_num:
					abnormal_line_ids.append(i+1)
			abnormal_line_ids = shorten_list(abnormal_line_ids)
			return [0, abnormal_line_ids]

def separate_char_is_tab(all_lines, logs, errors):
	""" 1.判断分割符是否为\t，如果不是需要替换为\t	"""
	if len(all_lines) < check_lines:
		lines = all_lines
	else:
		lines = all_lines[:check_lines-1]
		
	if judge_line_have_same_cells(lines, r'\t')[0] and judge_line_have_same_cells(lines, r'[\t]+')[0]:
		logs.append('All lines separeted by tab(s), and do not have empty cells.')
		new_lines = [re.sub(r'[\t]+', '\t', line) for line in all_lines]
		#new_lines.sort()
		return new_lines, logs, errors
	elif judge_line_have_same_cells(lines, r'\t')[0] and not judge_line_have_same_cells(lines, r'[\t]+')[0]:
		errors.append('Split by single tab, line(s) %s contain blank cell！' % ','.join([str(i) for i in judge_line_have_same_cells(lines, r'[\t]+')[1]]))
		#errors.append('用单个Tab分列后所有行的列数相同，但第 %s 行包含空元素！' % ','.join([str(i) for i in judge_line_have_same_cells(lines, r'[\t]+')[1]]))
		return [], logs, errors
		#return [re.sub(r'[\t]+', '\t', line) for line in lines], logs, errors
	elif not judge_line_have_same_cells(lines, r'\t')[0] and judge_line_have_same_cells(lines, r'[\t]+')[0]:
		logs.append('Some lines separeted by multiple tab, we have replaced by single tab for you.')
		new_lines = [re.sub(r'[\t]+', '\t', line) for line in all_lines]
		#new_lines.sort()
		return new_lines, logs, errors
	elif not judge_line_have_same_cells(lines, r'\t')[0] and not judge_line_have_same_cells(lines, r'[\t]+')[0]:
		errors.append('Split by tab(s), line(s) %s have different columns！'% ','.join([str(i) for i in judge_line_have_same_cells(lines, r'\t')[1]]))
		#errors.append('用Tab(s)对所有行进行分列后，第 %s 行的列数不一致！'% ','.join([str(i) for i in judge_line_have_same_cells(lines, r'\t')[1]]))
		return [], logs, errors

def separate_char_is_space(all_lines, logs, errors):
	""" 1.判断分割符是否为space，如果是，则替换为\t	"""
	if len(all_lines) < check_lines:
		lines = all_lines
	else:
		lines = all_lines[:check_lines-1]
	if judge_line_have_same_cells(lines, r'[ ]')[0] and judge_line_have_same_cells(lines, r'[ ]+')[0]:
		logs.append('All lines separeted by space(s), and do not have empty cells.')
		new_lines = [re.sub(r'[ ]+', '\t', line) for line in all_lines]
		#new_lines.sort()
		return new_lines, logs, errors
	elif judge_line_have_same_cells(lines, r'[ ]')[0] and not judge_line_have_same_cells(lines, r'[ ]+')[0]:
		errors.append('Split by single space, line(s) %s contain blank cell！' % ','.join([str(i) for i in judge_line_have_same_cells(lines, r'[ ]+')[1]]))
		#errors.append('用单个空格分列后所有行的列数相同，但第 %s 行包含空元素！' % ','.join([str(i) for i in judge_line_have_same_cells(lines, r'[ ]+')[1]]))
		return [], logs, errors
		#return [re.sub(r'[ ]+', '\t', line) for line in lines], logs, errors
	elif not judge_line_have_same_cells(lines, r'[ ]')[0] and judge_line_have_same_cells(lines, r'[ ]+')[0]:
		logs.append('Some lines separeted by multiple space, we have replaced by single space for you.')
		new_lines = [re.sub(r'[ ]+', '\t', line) for line in all_lines]
		#new_lines.sort()
		return new_lines, logs, errors
	elif not judge_line_have_same_cells(lines, r'[ ]')[0] and not judge_line_have_same_cells(lines, r'[ ]+')[0]:
		errors.append('Split by space(s), line(s) %s have different columns！'% ','.join([str(i) for i in judge_line_have_same_cells(lines, r'[ ]+')[1]]))
		#errors.append('用空格(s)对所有行进行分列后，第 %s 行的列数不一致！'% ','.join([str(i) for i in judge_line_have_same_cells(lines, r'[ ]+')[1]]))
		return [], logs, errors

def separate_char_is_space_or_tab(all_lines, logs, errors):
	""" 1.判断分割符是否为\s+，如果是，则替换为\t	"""
	if len(all_lines) < check_lines:
		lines = all_lines
	else:
		lines = all_lines[:check_lines-1]
	if judge_line_have_same_cells(lines, r'\s+')[0]:
		logs.append('All lines separeted by space(s) or tab(s), and we have replaced separate chars by single tab for you.')
		new_lines = [re.sub(r'\s+', '\t', line) for line in all_lines]
		#new_lines.sort()
		return new_lines, logs, errors
	else:
		errors.append('Split by space(s) or tab(s), line(s) %s have different columns！'% ','.join([str(i) for i in judge_line_have_same_cells(lines, r'[\s+]+')[1]]))
		#errors.append('用空格(s)或者Tab(s)对所有行进行分列后，第 %s 行的列数不一致！'% ','.join([str(i) for i in judge_line_have_same_cells(lines, r'[\s+]+')[1]]))
		return [], logs, errors

def test_return(a):
	if a==1:
		return '1'
	else:
		print '0'
	if a==2:
		return '2'
	else:
		return '3'

def judge_separate_char(tmp_lines, logs, errors):
	tmp_lines_checked_sep_char, logs, errors1 = separate_char_is_tab(tmp_lines, logs, errors)
	if not errors1:
		return tmp_lines_checked_sep_char, logs, errors1
	else:
		return [], logs, errors1

	tmp_lines_checked_sep_char, logs, errors2 = separate_char_is_space(tmp_lines, logs, errors)
	if not errors2:
		return tmp_lines_checked_sep_char, logs, errors2
	else:
		return [], logs, errors2

	tmp_lines_checked_sep_char, logs, errors3 = separate_char_is_space_or_tab(tmp_lines, logs, errors)
	if not errors3:
		return tmp_lines_checked_sep_char, logs, errors3
	else:
		return [], logs, errors3

def del_duplicate_lines(all_lines, logs):
	if len(all_lines) < check_lines:
		lines = all_lines
	else:
		lines = all_lines[:check_lines-1]
	
	lines_set_len = len(set(lines))
	if lines_set_len == len(lines):
		logs.append('Do not have duplicate lines')
		return all_lines, logs
	else:
		logs.append('Duplicated lines have been deleted.')
		new_lines = list(set(all_lines))
		new_lines.sort(key=all_lines.index) #保持原文件行的顺序
		return new_lines, logs

def del_lines_have_same_row_name(all_lines, errors, sep_char):
	if len(all_lines) < check_lines:
		lines = all_lines
	else:
		lines = all_lines[:check_lines-1]

	#new_lines = []
	row_names = []
	duplicate_row_names = []
	for line in lines:
		if line.split(sep_char)[0] not in row_names:
			row_names.append(line.split(sep_char)[0])
			#new_lines.append(line)
		elif line.split(sep_char)[0] not in duplicate_row_names:
			duplicate_row_names.append(line.split(sep_char)[0])
	if duplicate_row_names:
		errors.append('Line(s) %s have the same rowname!' % ','.join(duplicate_row_names))
		#errors.append('以下行的行名相同：%s!' % ','.join(duplicate_row_names))
	return all_lines, errors

def replace_invalid_chars(lines, logs, replace_char=''):
	valid_chars = digits + letters + '-%./ :,;_\t()[]=+{}|<>&'
	if lines[0].startswith('#'):
		logs.append('The first line is annotation line, which we will skip prechecking.')
		new_lines = [lines[0]]
		lines = lines[1:]
		ix_correction = 2
	else:
		new_lines = []
		ix_correction = 1
	#invalid_char_line_ix = []
	founded_invalid_chars = []
	for ix in range(len(lines)):
		invalid_char_found_flag = 0
		new_line = ''
		for i in lines[ix].strip():
			if i not in valid_chars:
				new_line += replace_char
				founded_invalid_chars.append(i)
			else:
				new_line += i
		new_lines.append(new_line)

	if founded_invalid_chars:
		logs.append('Some lines have invalid chars (%s), we delete them.' % ','.join(founded_invalid_chars))
	else:
		logs.append('All lines do not have invalid chars beyond %s.' % valid_chars)
	return new_lines, logs

#def warrning_negative_value_in_exp(lines, logs):

def write_errors(errors, log_file):
	log_handle = open(log_file, 'a')
	log_handle.write('Errors' + '=' * 30 + '\n')
	for error in errors:
		log_handle.write(error + '\n')
	log_handle.close()

def write_logs(logs, log_file, ix = 0):
	log_handle = open(log_file, 'a')
	if ix == 0:
		log_handle.write('\n')
		log_handle.write('Logs' + '=' * 30 + '\n')
	for log in logs:
		log_handle.write(log + '\n')
		ix += 1
	log_handle.close()

def __main__():
	description = "This script is used to pre_check input file of small tools, and correct the file if necessary!\n"
	quick_usage= 'python ' + sys.argv[0] + ' -input input_file -output output_file'

	newParser = argparse.ArgumentParser( description = description, usage = quick_usage );
	newParser.add_argument("-input", dest="input", help="Input file", default='input.txt', required=True);
	newParser.add_argument("-outdir", dest="outdir", help="Output directory", default='/share/nas1/liuw/tools_temp/');
	
	args = newParser.parse_args();
	argsDict = args.__dict__;

	input = argsDict['input']
	outdir = argsDict['outdir']
	logs = []
	errors = []
	tmp_lines = []
	input_filename = os.path.basename(input)
	corrected_input = input + '.new'
	pre_check_log = outdir + '/'+ input_filename+'.log'
	
	#print get_file_type(input)
	if get_file_type(input) == 'xls or doc' or get_file_type(input) == 'xlsx':
		convert_excel_to_txt(input, logs)
	else:
		os.system('dos2unix -q '+ input)
		os.system('mac2unix -q '+ input)
	
	logs, errors = is_empty(input, logs, errors)
	if errors:
		write_errors(errors, pre_check_log)
		print errors[0]
		sys.exit(errors[0])

	'''
	logs, errors = check_is_utf8(input, logs, errors)
	if errors:
		write_errors(errors, pre_check_log)
		print errors[0]
		sys.exit(errors[0])
	'''

	logs, errors = check_chinese_char(input, logs, errors)
	if errors:
		write_errors(errors, pre_check_log)
		print errors[0]
		sys.exit(errors[0])
	
	errors = judge_startswith_tabs_spaces(open(input).readlines(), errors)
	if errors:
		write_errors(errors, pre_check_log)
		print errors[0]
		sys.exit(errors[0])

	tmp_lines, logs = del_empty_lines(open(input).readlines(), logs)
	tmp_lines, logs = del_duplicate_lines(tmp_lines, logs)
	#tmp_lines, errors = del_lines_have_same_row_name(tmp_lines, errors, '\t')
	#if errors:
	#	write_errors(errors, pre_check_log)
	#	print errors[0]
	#	sys.exit(errors[0])

	tmp_lines_checked_sep_char, logs, errors = judge_separate_char(tmp_lines, logs, errors)
	if errors:
		write_errors(errors, pre_check_log)
		print errors[0]
		sys.exit(errors[0])
	tmp_lines, logs = replace_invalid_chars(tmp_lines_checked_sep_char, logs, '')
	#tmp_lines, logs = del_duplicate_lines(tmp_lines, logs)
	
	#tmp_lines, errors = del_lines_have_same_row_name(tmp_lines, logs)
	
	output_handle = open(corrected_input, 'w')
	for line in tmp_lines:
		output_handle.write(line.strip() + '\n')
	output_handle.close()

	ix = 0
	#print logs
	if logs:
		write_logs(logs, pre_check_log, ix)
	os.system('chmod 775 '+pre_check_log)
	
	if tmp_lines != '':
		os.system('mv '+input+' '+input+'.bak')
		os.system('mv '+corrected_input+' '+input)
	else:
		pass

if __name__ == '__main__':
	__main__()
