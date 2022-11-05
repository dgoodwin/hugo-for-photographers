#!/bin/env python

import os
import datetime
import shutil
import subprocess
import sys
from slugify import slugify

# store orig cwd, we need to chdir for hugo, but if using via
# a nautilus script we only get relative filenames.
orig_cwd = os.getcwd()

# if not 'HUGO_SITE_DIR' in os.environ:
    # print("ERROR: HUGO_SITE_DIR environment variable not defined")
    # sys.exit(1)

#site_dir = os.environ["HUGO_SITE_DIR"]
site_dir = "/home/dev/src/rmrf/"
os.chdir(site_dir) # for hugo binary to work

photo_files = sys.argv[1:]

print("Creating photo post with %d images: %s" % (len(photo_files), " ".join(photo_files)))
title = input("Enter post title, slug will be auto-generated: ")
slug = slugify(title)

# Get timestamp from exif data, used for what directory to place files in and post date:
first_image = photo_files[0]
if not os.path.isabs(first_image):
    first_image = os.path.join(orig_cwd, first_image)
capture_date = subprocess.run(['identify', '-format', "'%[EXIF:DateTimeOriginal]'", first_image], stdout=subprocess.PIPE).stdout.decode('utf-8')
capture_date = capture_date.replace("'", "") # comes out wrapped in '
capture_date = capture_date.split()[0].replace(":", "-") # uses : separators for some reason
photo_year = capture_date[0:4]

# Now we're getting crazy. Extract the dominant color from the image, use it as a weight, hugo
# seems to sort strings as you'd expect. This will let us group images of similar colors.

#print("Extracting dominant color from: %s (be patient)" % first_image)
#from colorthief import ColorThief
#color_thief = ColorThief(first_image)
#dominant_color = color_thief.get_color(quality=5)
#dominant_color = ('{:X}{:X}{:X}').format(dominant_color[0], dominant_color[1], dominant_color[2])
#print("Dominant color is: %s" % dominant_color)

post_dir = os.path.join(site_dir, 'content', 'photography', photo_year, slug)
print('Post created in: %s' % post_dir)
post_md_file = os.path.join(post_dir, 'index.md')
os.makedirs(post_dir)

# TODO: Serialize yaml
template = '''---
weight: 0
title: %s
date: %s
# mainImage:
tags:
- archive # always include
#- portfolio # for the best shots
#- novascotia
#- nature
#- clouds
#- martiniquebeach
#- lawrencetownbeach
#- snow
#- sunset
#- sunrise
#- ocean
#- street
#- cars
#- m3
#- bmw
---

{{< gallery match="*.JPG" >}}
'''

for pf in photo_files:
    # check if src file is a full path or not:
    if os.path.isabs(pf):
        src = pf
    else:
        src = os.path.join(orig_cwd, pf)
    shutil.copyfile(src, os.path.join(post_dir, os.path.basename(pf)))

f = open(post_md_file, "w")
f.write(template % (title, capture_date))
f.close()

os.system("nvim %s" % (post_md_file))

