import datetime
import json
import os
import re
import shutil
import sys
import webbrowser

from jinja2 import FileSystemLoader, Environment

def compile_home():
    args = {'page': 'home'}

    # Notepads
    to_compile = get_list('notepad_src')[:5]
    notes = []

    template = get_template('notepad_preview.html', render=False)

    for note in to_compile:
        args_np={'template': template, 'date': note['date'],
                 'slug': note['slug'], 'preview': True}
        notes.append(render_notepad(note['filename'], args=args_np))

    args['notes'] = notes

    # Articles
    to_compile_article = get_list('magazine_src')[:4]
    articles = []

    template = get_template('magazine_preview.html', render=False)

    for article in to_compile_article:
        articles.append(render_magazine(article['filename'], args={
                'url': article['filename'],
                'date': article['date'],
                'file': article['filename'],
                'slug': article['slug'],
                'template': template}))

    args['articles'] = articles

    get_template('home.html', args, 'app/index.html')

def render_magazine(template, args={}, output=None, render=True):
    if not 'template' in args:
        args['template'] = get_template('magazine.html', render=False)

    if 'slug' in args:
        args['ns'] = "article-%s" % args['slug']

    args['file'] = template

    return get_template(('magazine_src', template), args, render=render,
                        output='app/magazine/%s' % output)

def render_notepad(template, args={}):
    if 'template' not in args:
        args['template'] = get_template('notepad_single.html', render=False)

    return get_template(('notepad_src', template), args=args)

def datetimeformat(value, format='%B %d, %Y'):
    return value.strftime(format)

def footnoter(value):
    i = 1
    match = "\(\(\(((?:.|\n)*?)\)\)\)"
    link = "<sup id='fnc-%s'>[<a href='#fn-%s'>%s</a>]</sup>"
    footnote = "<li id='fn-%s'>%s [<a href='#fnc-%s'>&#x21A9;</a>]</li>"

    fns = []

    while re.search(match, value):
        footnote_text = re.search(match, value)
        value = re.sub(match, link % (i, i, i), value, 1)
        fns.append(footnote % (i, footnote_text.group(1), i))
        i += 1

    if fns:
        value = value + ("<ol class='footnotes'>%s</ol>" % '\n'.join(fns))
    return value

def namespacer(value, namespace, f):
    value = re.sub('#namespace', '#%s' % namespace, value)
    value = re.sub('assets/', 'magazine/%s/' % f.split('.')[0], value)
    return value

def get_list(folder):
    to_compile = os.listdir(folder)
    to_compile = [f for f in to_compile
                  if re.match("\d{4}-\d{2}-\d{2}-(.*).html", f)]

    to_compile.sort(reverse=True)

    return_list = []

    for f in to_compile:
        d = re.search('(\d{4})-(\d{2})-(\d{2})-(.*).html', f)
        date = datetime.datetime(int(d.group(1)), int(d.group(2)), int(d.group(3)))
        slug = d.group(4)
        return_list.append({'date':date, 'slug':slug, 'filename':f})

    return return_list

def compile_magazines():
    to_compile = get_list('magazine_src')

    for (i, article) in enumerate(to_compile):
        nav_prev = nav_next = False

        # gosh this is crazy inefficient.
        if i > 0:
            nav_next_template = render_magazine(to_compile[i - 1]['filename'], {}, render=False)
            nav_next = (to_compile[i - 1]['filename'], get_block(nav_next_template, 'title'))
        if i < len(to_compile) - 1:
            nav_prev_template = render_magazine(to_compile[i + 1]['filename'], {}, render=False)
            nav_prev = (to_compile[i + 1]['filename'], get_block(nav_prev_template, 'title'))

        args = {'date': article['date'],
                'slug': article['slug'],
                'page': 'magazine',
                'nav_next': nav_next,
                'nav_prev': nav_prev}

        # Move assets
        template_name = article['filename'].split('.')[0]
        if os.path.exists('magazine_src/%s' % template_name):
            shutil.copytree('magazine_src/%s' % template_name, 'app/magazine/%s' % template_name)

        render_magazine(article['filename'], args, article['filename'])

def get_block(template, block=''):
    return''.join([i for i in template.blocks.get(block)({})])

def compile_notepads():
    to_compile = get_list('notepad_src')

    notes = []

    for note in to_compile:
        f = render_notepad(note['filename'], args={'date': note['date'], 'slug': note['slug'] })
        notes.append(f)

    get_template('notepad.html', args={'notes': notes, 'page': 'notebook'}, output='app/notepad.html')

def get_template(template, args={}, output=None, render=True):
    loader = False
    template_file = False

    if isinstance(template, tuple):
        loader = FileSystemLoader('%s/' % template[0])
        template_file = template[1]
    else:
        loader = FileSystemLoader('templates/')
        template_file = template

    env = Environment(loader=loader)
    env.filters['footnoter'] = footnoter
    env.filters['namespacer'] = namespacer
    env.filters['datetimeformat'] = datetimeformat

    settings = {}
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    env.globals = {'base': settings['base'],
                   'year': 2011,
                   'article_url': get_list('magazine_src')[0]['filename']}

    template_object = env.get_template(template_file)

    if not render:
        return template_object

    rendered = template_object.render(args)

    if output:
        with open(output, 'w') as o:
           rendered = unicode(rendered)
           rendered = rendered.replace(u"\xe9", " ")
           rendered = rendered.replace(u"\u2019", " ")
           rendered = rendered.replace(u"\u00A0", " ")

           o.write(unicode(rendered))

    return rendered

#def render_tempate(template, args):
    #args['base'] = 'file:///Users/gkoberger/Sites/gkoberger/'
    #args['year'] = 2011

    #return template.render(args)

def move_base():
    shutil.rmtree('app')
    shutil.copytree('app-base', 'app')

    shutil.copytree('js', 'app/js')
    shutil.copytree('css', 'app/css')
    shutil.copytree('images', 'app/images')

if __name__ == '__main__':
    move_base()

    compile_notepads()
    compile_magazines()
    compile_home()
