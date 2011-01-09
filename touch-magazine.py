import os
import re
import shutil
import sys

def main(folder):

    # Find the next unique ID.
    all_folders = os.listdir("magazine-source")
    next_id = 0
    for f in all_folders:
        if re.match("^_?[0-9]", f):
            new_id = int(re.findall("[0-9]+", f)[0])
            if new_id > next_id:
                next_id = new_id
    next_id += 1

    # Slugify the folder name
    new_folder = re.sub("[_\s]", "-", folder).lower()
    new_folder = re.sub("[^-0-9a-z]", "", new_folder)

    shutil.copytree('magazine-source/_base',
                    'magazine-source/_%s-%s' % (next_id, new_folder))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You need a name!"
    else:
        main(sys.argv[1])

