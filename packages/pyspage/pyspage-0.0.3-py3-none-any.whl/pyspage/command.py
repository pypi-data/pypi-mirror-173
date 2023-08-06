import argparse
import os
import pyspage


def parse_args():
    parser = argparse.ArgumentParser(description = pyspage.name + 
                        ' Quickly build open source web pages for academic purposes in a pythonic and elegant way.')
    parser.add_argument('file', type=str,
                        help='path to input file')
    parser.add_argument('-o', '--output', type=str, 
                        help='path to output file (default: the same as input, but .py -> .html)')
    parser.add_argument('-l', '--localize', action=argparse.BooleanOptionalAction,
                        help='save all used network resources to local')
    parser.add_argument('-s', '--server', action=argparse.BooleanOptionalAction,
                        help='start a server on localhost:8000')
    parser.add_argument('-b', '--browser', action=argparse.BooleanOptionalAction, 
                        help='open the page with your default browser')
    args = parser.parse_args()
    return args

def run_server(dirname, port=8000):
    if dirname == '':
        dirname = '.'
    try:
        os.system(f'python -m http.server --directory {dirname} --bind 127.0.0.1 {port}')
    except KeyboardInterrupt:
        pass

def open_browser(outfile, base_url='http://127.0.0.1:8000/'):
    os.system(f'python -m webbrowser -t {base_url}{outfile}')

def main(args):
    fpath = args.file
    print(f'[Pyspage] input  file: {fpath}')
    html = pyspage.main(fpath)
    if args.output:
        outpath = args.output
    else:
        dirname, filename = os.path.split(fpath)
        outpath = os.path.join(dirname, filename.replace('.py', '.html'))
    with open(outpath, 'w') as f:
        f.write(html)
    print(f'[Pyspage] output file: {outpath}')
    outdir, outfile = os.path.split(outpath)
    if args.browser:
        open_browser(outfile)
    if args.server:
        run_server(outdir)

def run():
    args = parse_args()
    print(pyspage.name)
    main(args)
    print(pyspage.name)
