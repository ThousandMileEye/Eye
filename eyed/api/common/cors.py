#!/usr/bin/env python
# -*- coding: utf-8 -*-
<<<<<<< HEAD
from pyramid.request import Request
from pyramid.response import Response
=======
>>>>>>> fc0f4f6487538e5a7fc9a46c91bac71d642e3f0c

def request_factory(environ):
	request = Request(environ)
	request.response = Response()
	request.response.headerlist = []
	request.response.headerlist.extend((
		('Access-Control-Allow-Origin', '*'),
	))
	return request

