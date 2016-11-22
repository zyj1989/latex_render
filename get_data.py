#!/usr/bin/env python
# encoding: utf-8
# By zhangyingjie

from pymongo import MongoClient
from bson.objectid import ObjectId
from operator import itemgetter
from pprint import pprint
from write_tex import write_paper

db = MongoClient('192.168.168.90', 27017)['zmath']
section = ObjectId("5833d445ce4efd102e28d651")


def get_data_test():
    paper = db.section.find_one({'_id': section})
    item_ids = paper.get('item_ids')[-1]
    indexes = {item_id: index for index, item_id in enumerate(item_ids)}
    items = list(db.item.find({'_id': {'$in': item_ids}}))
    for item in items:
        assert isinstance(item, dict)
        item['index'] = indexes[item['_id']]
    items.sort(key=itemgetter('index'))
    items = items_data_transfer(items)
    paper['items'] = items
    write_paper(paper)
    return items


def items_data_transfer(items):

    def _deal_item(_item):
        if 'stem' in _item['data']:
            _item['data']['qs'] = [{'qs': _item['data']['qs'], 'desc': _item['data']['stem']}]
            del _item['data']['stem']
        return _item
    items = [_deal_item(item) for item in items]
    return items


def test():
    get_data_test()
