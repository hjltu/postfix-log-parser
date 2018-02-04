#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
hjltu@ya.ru 02-Feb-2018
python2.7 (no pep8 style)
licence: GPL v3

about:

	Use programm for parsing postfix log files
	1) open log file and parse each string
	2) find email From,To,if,status
	3) save to csv file
	4) print tables

usage:	parser2.py [file2parse] if no arguments print this text

"""

import sys,re
import time
import os,glob
import csv


def my_regexp(reg,line,num=1):
	out = re.search(reg, line)
	if out:
#		print out.group(num)
		return out.group(num)
	else:
		return ''


def my_file(in_file=None):
	"""
	read log and create csv
	"""

	# utc
	if in_file is not None:
		csv_file=time.strftime('%d-%b-%Y_%H:%M:%S', time.gmtime(time.time()))+'.csv'
		print 'open file ',in_file
		print 'writing file ',csv_file,'...'
		csv_row={'id':'','from':'','to':'','sent':'','removed':'','reject':'','bounced':'','deferred':''}
		try:
			with open(csv_file, 'w') as out_file:
				with open(in_file) as in_file:
					for line in in_file:
						csv_row['from']=my_regexp('(from=<)([\w\.-]+@[\w\.-]+)(>)',line,2)
						csv_row['id']=my_regexp('(:[^\S\n\t]+)([A-Z0-9]+)(:)',line,2)
						csv_row['to']=my_regexp('(to=<)([\w\.-]+@[\w\.-]+)(>)',line,2)
						csv_row['sent']=my_regexp('(status=sent)',line)
						csv_row['removed']=my_regexp('(removed)',line)
						csv_row['reject']=my_regexp('(reject)',line)
						csv_row['bounced']=my_regexp('(bounced)',line)
						csv_row['deferred']=my_regexp('(deferred)',line)
						#print csv_row
						if len([len(value) for key,value in csv_row.items() if value])>0:
							row=csv_row['id']+','+csv_row['from']+','+csv_row['to']+','+csv_row['sent']+','\
							+csv_row['removed']+','+csv_row['reject']+','+csv_row['bounced']+','+csv_row['deferred']+'\n'
							out_file.write(row)
		except:
			print 'Error file read/write'
			return 1


def my_count(lst,el,comp):
	lst=lst
	comp=comp
	el=el
	count=0
	for x in xrange(len(lst)):
		if lst[x][el] != comp:
			count+=1
		else:
			break
	return count

def my_csv():
	"""
	read last csv and print stat
	"""

	# find last csv
	files=glob.glob('*.csv')
	files.sort(key=os.path.getmtime)
	print 'reading ',files[-1],' ...'

	stat_list=[]

	try:
		with open(files[-1],'r') as file:
			csv_read=csv.reader(file)
			for row in csv_read:
#				print(row)
				count=my_count(stat_list,0,row[0])
				if count==len(stat_list):
					stat_list.append(',,,,,'.split(','))
					stat_list[count][0]=row[0] 	# id
				x=[x for x in xrange(len(stat_list)) if stat_list[x][0]==row[0]][0]
				if row[1]:
					stat_list[x][1]=row[1] 	# from
				if row[2]:
					stat_list[x][2]=row[2] 	# to
				if row[3]:
					stat_list[x][3]='sent' 	# sent
				if row[4]:
					stat_list[x][4]=row[4] 	# remove
				if row[5] or row[6] or row[7]:
					stat_list[x][5]='error' 	# error

	except:
		print 'Error read csv'
		return 1

	print 'creating table ...'
	mail_stat=[]
	for x in stat_list:
		if x[1]:
			count=my_count(mail_stat,0,x[1])
			if count==len(mail_stat):
				mail_str=x[1]+',0,0,0'
				mail_stat.append(mail_str.split(','))
				for i in range(1,4):
					mail_stat[count][i]=int(mail_stat[count][i])

				id_list=[]
				sent=0
				for i in range(len(stat_list)):
					if x[1]==stat_list[i][1]:
						id_list.append(stat_list[i][0])
						if stat_list[i][3]:
							sent+=1

				mail_stat[count][1]=len(list(set(id_list)))
				mail_stat[count][2]=sent
				mail_stat[count][3]=mail_stat[count][1]-sent


#	print 'stat ',len(stat_list)
	print '\n','{0:20}{1}'.format('','*** Print list of emails ***')
	print '{0:52}{1:10}{2:10}{3:10}'.format('email','all','sent','error')
	print '{0:52}{1:10}{2:10}{3:10}'.format('-----','-----','-----','-----')
	for x in xrange(len(mail_stat)):
		print '{0:45}{1:10}{2:10}{3:10}'.format(mail_stat[x][0],mail_stat[x][1],mail_stat[x][2],mail_stat[x][3])

def main(arg):
	"""
	start
	"""

	start_time=time.time()
	my_file(arg)
	my_csv()

	print '{0:20}{1}'.format('','*** %s seconds ***' % (time.time() - start_time)),'\n'


import unittest

class Test_jino(unittest.TestCase):

	def test_one(self):
		self.assertNotEqual(my_file('maillog_small'), 1)
		self.assertEqual(my_file(), None)
		self.assertNotEqual(my_csv(), 1)

		print 'test done'


if __name__=='__main__':
	if len(sys.argv)>1:
		arg=sys.argv[1:][0]
		main(arg)
	else:
		print __doc__
		unittest.main()