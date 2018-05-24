#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.object import ObjectType, registered_object_types
from bacpypes.object import get_object_class
from bacpypes.basetypes import PropertyIdentifier

#
# Object Class の 取得
#
def findObjectClassByType(object_type):
	return get_object_class(object_type)

#
# Object List の 取得
#
def getObjects():
	#
	# ObjectType を列挙
	#
	object_ids = []
	for k, v in ObjectType.enumerations.items():
		object_ids.append({
			'id'	: v,
			'name'	: k,
		})

	#
	# OpjectType の リストを返却
	#
	return object_ids

#
# ID から Object の 取得
#
def findObjectByID(id):
	result = filter(lambda object: object['id'] == id, getObjects())
	if len(result) == 0: return None
	if len(result) == 1: return result[0]
	raise Exception('It must not happen, bacnet object have some missing.')

#
# NAME から Object の 取得
#
def findObjectByName(name):
	result = filter(lambda object: object['name'] == name, getObjects())
	if len(result) == 0: return None
	if len(result) == 1: return result[0]
	raise Exception('It must not happen, bacnet object have some missing.')

#
# Property List の 取得
#
def getProperties():
	#
	# Property Identifier を列挙
	#
	property_ids = []
	for v, k in PropertyIdentifier.enumerations.items():
		property_ids.append({
			'id'	: k,
			'name'	: v
		})

	#
	# Property List の リストを返却
	#
	return property_ids

#
# NAME から Property の 取得
#
def findPropertyByName(name):
	result = filter(lambda property: property['name'] == name, getProperties())
	if len(result) == 0: return None
	if len(result) == 1: return result[0]
	raise Exception('It must not happen, bacnet object have some missing.')

#
# ID から Property の 取得
#
def findPropertyByID(id):
	result = filter(lambda property: property['id'] == id, getProperties())
	if len(result) == 0: return None
	if len(result) == 1: return result[0]
	raise Exception('It must not happen, bacnet object have some missing.')

#
# オブジェクト の プロパティ一覧の検索
#
def getPropertiesByObject(object):
	#
	# オブジェクト一覧の取得
	#
	if not 'id' in object and not 'name' in object:
		return []

	#
	# プロパティ一覧の取得
	#
	properties = PropertyIdentifier.enumerations

	#
	# オブジェクト内のプロパティ一覧の取得
	#
	propertyIdentifiers = []
	obj = { k[0]:v.properties for k, v in registered_object_types.items() }
	for property in obj[object['name']]:
		propertyIdentifiers.append({
			'id'	: properties[property.identifier],
			'name'	: property.identifier
		})

	#
	# Property List の リストを返却
	#
	return propertyIdentifiers

#
# エントリーポイント
#
if __name__ == '__main__':
	#print getObjects()
	#print findObjectByID(2)
	print findObjectByName('analogValue')
	print findPropertyByID(85)
	#print getPropertiesByObject(findObjectByName('analogValue'))
	#print getPropertiesByObject(findObjectByName('device'))
	print findObjectClassByType('analogValue')

