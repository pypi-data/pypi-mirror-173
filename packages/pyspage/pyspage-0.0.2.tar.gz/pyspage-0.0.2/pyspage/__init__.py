from .elements import *
from .layout import layout_to_html
from .pyscript import py2pys, get_pkgs
from .utils import name


__author__ = 'jianjiang.bio@gmail.com'
__version__ = '0.0.2'

def main(fpath):
    script = py2pys(fpath)
    html = layout_to_html(fpath)
    packages = get_pkgs(fpath)
    page = Page(layout=html, script=script, packages=packages)
    return page.html

# fake methods
class Fake:
    def __init__(self, name, help_):
        self.name = name
        self.__doc__ = help_
    def __str__(self):
        return self.name
document = Fake('document', "`document` is used to manipulate HTML tags and events.")
body = Fake('body', '`body` represents to the body element in browser.')
