import re
from .layout import all_elements


def ele_in_line(line, eles):
    line = [j for i in line.split('=') for j in i.split() if j]
    for e in eles:
        if e == line[0]:
            return e
    return False

def ele_write(line, eles):
    for e in eles:
        if f'{e}.write(' in line:
            return e
    return False

def select_element(ele):
    return f'{ele} = document.querySelector("#{ele}")\n'

def py2pys(fpath):
    script = ''
    elements = all_elements(fpath)
    with open(fpath) as f:
        bypass = False
        for line in f:
            # layout defined over
            if bypass:
                if ('"' in line) or ("'" in line):
                    bypass = False
            # just annotations
            elif line.strip().startswith('#'):
                script += '\n'
            # importing pyspage
            elif ('pyspage' in line) and ('import' in line):
                continue
            # defining layout
            elif ('layout' in line) and ('=' in line):
                bypass = True
                continue
            # empty line
            elif line.strip() == '':
                script += line
            # defining a element
            elif ele_in_line(line, elements):
                ele = ele_in_line(line, elements)
                new_line = select_element(ele)
                script += new_line
            # writing content into a element using `.write()`
            elif ele_write(line, elements):
                ele = ele_write(line, elements)
                pre = re.search(r'^([ \t]*)', line).group(1)
                content = re.search(r'write\((.*)\)', line).group(1)
                new_line = f"{pre}Element('{ele}').write({content})\n"
                script += new_line
            # event: oncreate
            elif ('.oncreate' in line) and ('=' in line):
                if 'lambda ' in line:
                    new_line = line.split('lambda ', maxsplit=1)[1]\
                                    .split(':', maxsplit=1)[1]\
                                    .lstrip()
                else:
                    new_line = line.split('=', maxsplit=1)[1]\
                                    .strip()\
                                    + '()\n'
                script += new_line
            else:
                script += line
    return script
    