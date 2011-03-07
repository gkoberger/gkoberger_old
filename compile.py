import datetime
import json
import os
import re
import sys
import webbrowser

from jinja2 import FileSystemLoader, Environment

def compile(folder):
    old_folder = 'magazine/%s/source' % folder
    new_folder = 'magazine/%s' % folder

    # Get the settings.
    settings_file = open('settings.json')
    settings = json.load(settings_file)

    # Get the variables.
    data_file = open('%s/data.json' % old_folder)
    data = dict(settings.items() + json.load(data_file).items())

    # Set up the header.
    input = 'magazine-header.html'
    header = output_file(input, False, data, return_file=True)
    data.setdefault('header', header)

    # Copy over the article-specific stuff.
    for file in os.listdir(old_folder):
        input = '%s/%s' % (old_folder, file)
        output = '%s/%s' % (new_folder, file)
        output_file(input, output, data)

    # Integrate it into the main content.
    data.setdefault('content', open('%s/content.html' % new_folder).read())
    input = 'magazine-frame.html'
    output = '%s/index.html' % new_folder
    output_file(input, output, data)

    # Remove unnecessary files.  I'm looking at you, content.html and data.json.
    remove_files = ["content.html", "data.json"]
    for file in remove_files:
        os.remove('%s/%s' % (new_folder, file))

def output_file(input_file, output_file, data, return_file=False):
    # Inefficient, but we only do it once so it doesn't matter.
    input = open(input_file)
    output_buffer = []

    for line in input:
        if input_file.endswith("html"):
            for (k, v) in data.items():
                line = line.replace("<!-- [%s] -->" % k, v)
        output_buffer.append(line)

    if output_file:
        output = open(output_file, 'a')
        for line in output_buffer:
            output.write(line)
        output.close()

    if return_file:
        return '\n'.join(output_buffer)

def main(f):
    to_compile = os.listdir("magazine")

    # Rerender each folder.
    for folder in to_compile:
        compile(folder)

    # Open if folder passed in
    if f:
        webbrowser.open(f)

def compile_home():
    args = {'page': 'home'}

    # Notepads
    to_compile = list_notepads()[:5]
    notes = []

    for note in to_compile:
        d = re.search('(\d{4})-(\d{2})-(\d{2})-(.*).html', note)
        date = datetime.datetime(int(d.group(1)), int(d.group(2)), int(d.group(3)))
        slug = d.group(4)
        notes.append(render_notepad(note, {'date': date, 'preview': True, 'slug': slug}))

    args['notes'] = notes

    render('home.html', args, 'index.html')

def render_notepad(template, args={}):
    loader = FileSystemLoader('notepad/')
    env = Environment(loader=loader)

    env.filters['datetimeformat'] = datetimeformat

    rendered = env.get_template(template).render(args)

    return rendered

def datetimeformat(value, format='%B %d, %Y'):
    return value.strftime(format)

def list_notepads():
    to_compile = os.listdir("notepad")
    to_compile = [f for f in to_compile
                  if re.match("\d{4}-\d{2}-\d{2}-(.*).html", f)]

    to_compile.sort(reverse=True)

    return to_compile

def compile_notepads():
    to_compile = list_notepads()

    notes = []

    for note in to_compile:
        d = re.search('(\d{4})-(\d{2})-(\d{2})-(.*).html', note)
        date = datetime.datetime(int(d.group(1)), int(d.group(2)), int(d.group(3)))
        slug = d.group(4)
        notes.append(render_notepad(note, {'date': date, 'slug': slug}))

    render('notepad.html', {'notes': notes, 'page': 'notebook'}, 'notepad.html')

def render(template, args={}, output=None):
    loader = FileSystemLoader('templates/')
    env = Environment(loader=loader)

    args['base'] = 'file:///Users/gkoberger/Sites/gkoberger/'
    args['year'] = 2011

    rendered = env.get_template(template).render(args)

    if output:
        with open(output, 'w') as o:
           o.write(rendered)
    else:
        return rendered

if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 2 else None
    #main(folder)

    compile_notepads()
    compile_home()
