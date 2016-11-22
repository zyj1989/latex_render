#!/usr/bin/env python
# encoding: utf-8
# By zhangyingjie
import os


des_paper_dir = u'/Users/zyj/var/data/papers'
template = u'\\documentclass{homework}\n\\begin{document}\n'

def write_paper(paper):

    def _write_item(_item):

        def __deal_opts(_opts):
            if _opts:
                opt_tex = u'\\OPTIONS'
                for opt in _opts:
                    opt_tex += u'{%s}' % opt
                return opt_tex
            else:
                return ''

        def __deal_ans(_ans):
            if isinstance(_ans, list):
                ret = u''.join(map(lambda x: chr(ord('A') + x), _ans))
            elif not _ans:
                ret = u''
            else:
                ret = _ans
            return ret

        def __deal_qs(_qs_list):
            ret = u''
            if _qs_list:
                for _qs in _qs_list:
                    desc = _qs.get('desc')
                    opts = __deal_opts(_qs.get('opts'))
                    ans = __deal_ans(_qs.get('ans'))
                    ret += u'\\SUBQS{%s}{%s}{%s}' % (desc, opts, ans)
            return ret

        _qs = _item['data']['qs'][0]
        desc = _qs.get('desc')
        opts = __deal_opts(_qs.get('opts'))
        ans = __deal_ans(_qs.get('ans'))
        qs_1 = __deal_qs(_qs.get('qs'))
        return u'\\ITEM{%s}{%s}{%s}{%s}\n' % (desc, qs_1, opts, ans)
    tex = template
    paper_name = u'{name}.tex'.format(name=paper['name'])
    file_path = os.path.join(des_paper_dir, paper_name)
    for item in paper['items']:
        tex += _write_item(item)
    tex += u'\\end{document}'
    f = open(file_path, 'w')
    f.write(tex.encode(encoding='utf-8'))
    f.close()
