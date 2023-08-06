import re
import os
import sys
import importlib


def load_local_module(fpath):
    # add temporary path
    dir_name = os.path.dirname(fpath)
    sys.path.append(dir_name)
    # dynamicly import the `py` file
    module_name = os.path.basename(fpath).rstrip('.py')
    module = importlib.import_module(module_name)
    return module


colors = ['\33[41m', '\33[42m', '\33[43m', '\33[91m', '\33[44m', '\33[45m', '\33[46m']
start, end = ('\33[5m', '\33[0m')
string = ''.join([f'{c} {t} ' for t,c in zip('PYSPAGE', colors)])
name = start + string + end

def indentation(lines):
    pattern = re.compile(r'^([ \t]*)')
    indent_list = [pattern.search(l).group(1) for l in lines.split('\n')]
    single_indent_list = [i[0] for i in indent_list if i]
    if not single_indent_list:
        return ''
    s = single_indent_list
    indent = '\t' if s.count('\t') > s.count(' ') else ' '
    indent_list = [i for i in indent_list if i.startswith(indent)]
    return sorted(indent_list, key=len)[0]

def file_indent(fpath):
    with open(fpath) as f:
        lines = f.read()
    return indentation(lines)

std_libs = ['base64', '_compression', 'getopt', 'wave', 'getpass', 'argparse', 'modulefinder', 
            'os', 'bdb', 'resource', '_strptime', 'antigravity', 'time', 'zlib', '__future__', 
            'socket', 'keyword', 'wsgiref', 'binascii', 'sysconfig', 'encodings', '_py_abc', 
            '_weakrefset', 'msilib', 'grp', 'telnetlib', 'ossaudiodev', 'html', 'venv', 'xml', 
            'sqlite3', 'shutil', 'cgi', 'symtable', 'itertools', 'dataclasses', 'winsound', 'gc', 
            'socketserver', 'curses', 'ftplib', 'zipimport', 'stat', 'winreg', 'test', 'pathlib', 
            'asyncore', 'netrc', 'pickle', '_collections_abc', 'subprocess', 'tarfile', 'zipfile', 
            'importlib', 'asynchat', 'errno', 'genericpath', 'audioop', 'http', 'asyncio', 'smtpd', 
            'sched', 'xdrlib', 'bisect', '_markupbase', '_thread', '_bootlocale', 'cProfile', 'copy', 
            'fileinput', 'gzip', 'linecache', 'concurrent', 'pstats', 'secrets', 'optparse', 'calendar', 
            'stringprep', 'reprlib', 'zoneinfo', 'enum', '_sysconfigdata_x86_64_conda_cos6_linux_gnu', 
            'rlcompleter', 'aifc', 'binhex', 'configparser', 'email', 'threading', 're', 'filecmp', 
            '_aix_support', 'builtins', 'glob', 'readline', 'tabnanny', 'ipaddress', 'marshal', 'timeit', 
            'idlelib', 'zipapp', 'runpy', 'platform', 'math', '_pyio', 'mimetypes', 'typing', 'dis', 
            'cmath', 'tracemalloc', 'gettext', 'fnmatch', 'imaplib', '_pydecimal', 'contextvars', 
            'nturl2path', 'parser', '_osx_support', 'abc', 'types', 'py_compile', 'sndhdr', 'copyreg', 
            '__main__', 'selectors', '__phello__', '_bootsubprocess', 'cmd', 'site', 'turtledemo', 'hmac', 
            'inspect', 'posixpath', 'codeop', 'codecs', 'formatter', 'nntplib', 'bz2', 'symbol', 'code', 
            '_sitebuiltins', 'heapq', 'smtplib', 'sre_parse', 'pkgutil', 'token', 'numbers', 'tkinter', 
            'turtle', 'string', 'operator', 'struct', 'select', '_sysconfigdata_x86_64_conda_linux_gnu', 
            'imp', 'locale', 'pydoc_data', 'graphlib', 'pty', 'spwd', 'sunau', 'collections', 'compileall', 
            'profile', 'chunk', 'posix', 'fcntl', 'shlex', 'sre_compile', 'csv', 'xmlrpc', 'sre_constants', 
            '_compat_pickle', 'mailbox', 'syslog', 'crypt', 'pyclbr', 'io', 'ssl', 'array', 'multiprocessing', 
            'statistics', 'functools', 'cgitb', 'termios', 'weakref', 'pydoc', 'distutils', 'contextlib', 
            'dbm', 'this', 'traceback', 'urllib', 'warnings', 'poplib', 'tokenize', 'mmap', 'uu', 'logging', 
            'msvcrt', 'ctypes', 'quopri', 'queue', 'tempfile', 'json', 'fractions', 'colorsys', 'imghdr', 
            'lib2to3', 'sys', 'webbrowser', 'difflib', 'uuid', 'shelve', 'ntpath', 'decimal', 'plistlib', 
            'faulthandler', 'mailcap', 'pickletools', 'signal', 'unittest', 'datetime', 'nis', 'unicodedata', 
            'atexit', 'tty', 'lzma', 'hashlib', 'pdb', 'lib', 'pipes', 'trace', '_threading_local', 'pwd', 
            'ensurepip', 'pprint', 'random', 'textwrap', 'ast', 'opcode', 'doctest']

def is_std(m):
    if m.lower() in std_libs:
        return True
    return False
