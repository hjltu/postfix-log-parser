#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
hjltu@ya.ru for jino.ru 02-Feb-2018
python2.7 (no pep8 style)

licence: GPL v3

unittest for parser

usage:	python test_jino.py
"""


import unittest
from jino import Mail

class Test_jino(unittest.TestCase):

	def test_one(self):
		mail=Mail()
		self.assertNotEqual(mail.my_file('maillog_small'), 1)
		self.assertNotEqual(mail.my_csv(), 1)

		print 'test done'

if __name__=='__main__':
	unittest.main()