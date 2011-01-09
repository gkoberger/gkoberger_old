import os, shutil, json

def compile(folder):
    old_folder = 'magazine-source/%s' % folder
    new_folder = 'magazine-rendered/%s' % folder
    os.mkdir(new_folder)

    # Get the settings.
    settings_file = open('settings.json')
    settings = json.load(settings_file)
    
    # Get the variables.
    data_file = open('%s/data.json' % old_folder)
    data = dict(settings.items() + json.load(data_file).items())

    # Copy over the article-specific stuff.
    for file in os.listdir(old_folder):
        input ='%s/%s' % (old_folder, file)
        output = '%s/%s' % (new_folder, file)
        output_file(input, output, data)

    # Integrate it into the main content.
    data.setdefault('content', open('%s/content.html' % new_folder).read())
    input ='magazine-frame.html'
    output = '%s/index.html' % new_folder
    output_file(input, output, data)

def output_file(input_file, output_file, data):
    # Inefficient, but we only do it once so it doesn't matter.
    input = open(input_file)
    output = open(output_file, 'a')

    for line in input:
        if input_file.endswith("html"):
            for (k, v) in data.items():
                line = line.replace("<!-- [%s] -->" % k, v)
        output.write(line + "\n")
    output.close()
        
def main():
    to_compile = os.listdir("magazine-source")

    # Remove all old rendered folders.
    os.system('rm -r -f magazine-rendered/*')

    # Rerender each folder.
    for folder in to_compile:
        compile(folder)
        
if __name__ == '__main__':
    main()

