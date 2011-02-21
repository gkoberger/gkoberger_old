import os
import json
import webbrowser
import sys

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

if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 2 else None
    main(folder)

