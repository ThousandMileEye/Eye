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
	}, headers = [{
		'Access-Control-Allow-Origin', '*'
	}])

#
# リクエスト失敗時の処理
#
def Error(message):
	return HTTPBadRequest(json_body = {
		'ok'		: False,
		'error'		: {
			'message' : message
		}
	}, headers = [{
		'Access-Control-Allow-Origin', '*'
	}])

