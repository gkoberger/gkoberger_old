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
        notes.append(render_notepad(note['filename'], args={'template': template, 'date': note['date'], 'slug': note['slug'], 'preview': True}))

    args['notes'] = notes

    # Articles
    to_compile_article = get_list('magazine_src')[:4]
    articles = []

    template = get_template('magazine_preview.html', render=False)

    for article in to_compile_article:
        articles.append(render_magazine(article['filename'], args={'url': article['filename'],
                'date': article['date'],
                'slug': article['slug'],
                'template': template}))

    args['articles'] = articles

    get_template('home.html', args, 'app/index.html')

def render_magazine(template, args={}, output=None, render=True):
    if not 'template' in args:
        args['template'] = get_template('magazine.html', render=False)

    if 'slug' in args:
        args['ns'] = "article-%s" % args['slug']

    return get_template(('magazine_src', template), args, output='app/magazine/%s' % output, render=render)

def render_notepad(template, args={}):
    if 'template' not in args:
        args['template'] = get_template('notepad_single.html', render=False)

    return get_template(('notepad_src', template), args=args)

def datetimeformat(value, format='%B %d, %Y'):
    return value.strftime(format)

def namespacer(value, namespace):
    return re.sub('#namespace', '#%s' % namespace, value)

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

        render_magazine(article['filename'], args, article['filename'])

def get_block(template, block=''):
    return''.join([i for i in template.blocks.get(block)({})])

def compile_notepads():
    to_compile = get_list('notepad_src')

    notes = []

    for note in to_compile:
        notes.append(render_notepad(note['filename'], args={'date': note['date'], 'slug': note['slug'] }))

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
           o.write(rendered)

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
