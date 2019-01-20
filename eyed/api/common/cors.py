#!/usr/bin/env python
# -*- coding: utf-8 -*-
<<<<<<< HEAD
from pyramid.request import Request
from pyramid.response import Response
=======
<<<<<<< HEAD
from pyramid.request import Request
from pyramid.response import Response
=======
>>>>>>> fc0f4f6487538e5a7fc9a46c91bac71d642e3f0c
>>>>>>> 5b1abcfd708bf008c6a968d8e4872d16800c2d38

def request_factory(environ):
	request = Request(environ)
	request.response = Response()
	request.response.headerlist = []
	request.response.headerlist.extend((
		('Access-Control-Allow-Origin', '*'),
	))
	return request

