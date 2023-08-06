import re
from .utils import load_local_module


def load_layout_str(fpath):
    module = load_local_module(fpath)
    layout_str = module.layout.strip()
    return layout_str

def all_elements(fpath):
    layout_str = load_layout_str(fpath)
    return [i.strip() for i in layout_str.split()]

def parse_layout(fpath):
    layout_str = load_layout_str(fpath)
    pattern = re.compile(r'^([ \t]*)')
    indent_and_id = []
    for line in layout_str.split('\n'):
        match = pattern.search(line)
        indent = match.group(1)
        id_ = line.strip()
        indent_and_id.append((indent, id_))
    return indent_and_id
        
def is_indent_valid(ind_and_id):
    ind_list, ind_len_list = [], []
    for ind, _ in ind_and_id:
        if ind:
            ind_list.append(ind[0])
            ind_len_list.append(len(ind))
    if len(ind_list) == 0:
        return True
    ind_char_valid = len(set(ind_list)) == 1
    min_len = min(ind_len_list)
    ind_len_valid = not any([i % min_len for i in ind_len_list])
    if ind_char_valid and ind_len_valid:
        return True
    return False    

def get_level_and_id(ind_and_id):
    len_list, id_list = [], []
    for ind, id_ in ind_and_id:
        len_list.append(len(ind))
        id_list.append(id_)
    uniq_sorted_len = sorted(set(len_list))
    ind_unit = None
    for i in uniq_sorted_len:
        if i > 0 and ind_unit == None:
            ind_unit = i
    if ind_unit == None:
        len_list = [0 for i in len_list]
    else:
        len_list = [i / ind_unit for i in len_list]
    return zip(len_list, id_list)

def gen_id_dict(ind_and_id):
    level_and_id = get_level_and_id(ind_and_id)
    root = {}
    stack = [root]
    level_stack = [-1]
    for level, id_ in level_and_id:
        if level > level_stack[-1]:
            new_dict = {}
            stack[-1][id_] = new_dict
            stack.append(new_dict)
            level_stack.append(level)
        elif level <= level_stack[-1]:
            while 1:
                stack.pop()
                level_stack.pop()
                if level > level_stack[-1]:
                    new_dict = {}
                    stack[-1][id_] = new_dict
                    stack.append(new_dict)
                    level_stack.append(level)
                    break
    return root

def ids_to_objs(fpath, ids):
    module = load_local_module(fpath)
    objs = {}
    for id_ in ids:
        objs[id_] = getattr(module, id_)
    return objs

def gen_html(dict_, eles):
    if dict_ == {}:
        return ['']
    res = []
    for id_, children in dict_.items():
        html = eles[id_].html.format(
            id_ = id_,
            innerHtml = ''.join(gen_html(children, eles))
        )
        res.append(html)
    return res

def id_dict_to_html(fpath, root):
    ids = all_elements(fpath)
    eles = ids_to_objs(fpath, ids)
    html = gen_html(root, eles)
    return ''.join(html)

def layout_to_html(fpath):
    ind_and_id = parse_layout(fpath)
    root = gen_id_dict(ind_and_id)
    html = id_dict_to_html(fpath, root)
    return html

