#!/usr/bin/env python
#encoding: utf8

import argparse
import sys

import jinja2
import markdown
#from libs.markdown2 import Markdown

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <script type="text/javascript" src="static/js/jquery.1.11.1.js"></script>
    <script type="text/javascript" src="static/js/jquery.jsonview.js"></script>
    <link rel="stylesheet" href="static/css/bootstrap-3.3.5.min.css">
    <link rel="stylesheet" href="static/css/jquery.jsonview.css">
    <script type="text/javascript">
    $( document ).ready(function() {
        $('table').addClass('table table-bordered');
        $( ".json" ).each(function( index ) {
            original_json_data = $( this ).text();
            var json_decode_data=jQuery.parseJSON(original_json_data);
            if(typeof json_decode_data =='object'){
                pretty_json = $(this).JSONView(original_json_data);
            }
        });
    });
    </script>
    <style>
        body {
            /*font-family: sans-serif;*/
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        code, pre ,pre code{
              /*color: #080;*/
              border: none;
              border-radius: 0;
              font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
              background-color: #F9F9F9;
              padding: 2px 4px;
              border-radius: 4px;
              font-size: 12px !important;
              line-height: 16px !important;
              margin: 0;
        }
        h1 code,
        h2 code,
        h3 code,
        h4 code,
        h5 code,
        h6 code {
            font-size: inherit;
        }

    </style>
</head>
<body>
<div class="container">
{{content}}
</div>
</body>
</html>
"""


def parse_args(args=None):
    d = 'Make a complete, styled HTML document from a Markdown file.'
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('mdfile',
                        type=argparse.FileType('r'),
                        nargs='?',
                        default=sys.stdin,
                        help='File to convert. Defaults to stdin.')
    parser.add_argument('-o', '--out',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Output file name. Defaults to stdout.')
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    md = args.mdfile.read()
    #extensions = ['extra', 'smartypants']
    extensions = ['extra']
    md = md.decode('utf8')
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    doc = jinja2.Template(TEMPLATE).render(content=html)
    args.out.write(doc.encode('utf8'))


if __name__ == '__main__':
    sys.exit(main())
