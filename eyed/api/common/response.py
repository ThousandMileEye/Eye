#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound, HTTPOk
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPRequestTimeout

#
# リクエスト成功時の処理
#
def OK(value = None):
	return HTTPOk(json_body = {
		'ok' 	: True,
		'data'	: value,
	})

#
# リクエスト失敗時の処理
#
def Error(message):
	return HTTPOk(json_body = {
		'ok'		: False,
		'error'		: {
			'message' : message
		}
	})

