#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound, HTTPOk
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPRequestTimeout

#
# リクエスト成功時の処理
#
def OK(value):
	return HTTPOk(json_body = {
		'ok' 	: True,
		'data'	: value,
	})

