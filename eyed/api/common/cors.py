#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.request import Request
from pyramid.response import Response

def request_factory(environ):
	request = Request(environ)
	request.response = Response()
	request.response.headerlist = []
	request.response.headerlist.extend((
		('Access-Control-Allow-Origin', '*'),
	))
	return request

