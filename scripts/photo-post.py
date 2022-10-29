#!/bin/env python

import os
import shutil
import sys

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
slug = input("Enter post slug/title (i.e. my-photoshoot-title): ")

# TODO: Guess the timestamp for post from the creation timestamp of the first
# image in the list. This is less complex than dealing with exif.
# TODO: should this be the time the post was made though? Old posts might
# get missed by rss feeds.

post_dir = os.path.join(site_dir, 'content', 'photography', '2022', slug)
post_md_file = os.path.join(post_dir, 'index.md')
os.system("hugo new %s" % post_md_file)
#if len(photo_files) > 1:
os.mkdir(os.path.join(post_dir, 'gallery'))

for pf in photo_files:
    # check if src file is a full path or not:
    if os.path.isabs(pf):
        src = pf
    else:
        src = os.path.join(orig_cwd, pf)
    shutil.copyfile(src, os.path.join(post_dir, 'gallery', os.path.basename(pf)))
    # Also copy to my best of 2022 gallery
    shutil.copyfile(src, os.path.join(post_dir, '../../bestof/2022/images', os.path.basename(pf)))

# massage the file for our input:
os.system("sed -i 's/COVERIMAGE/gallery\/%s/g' %s" % (os.path.basename(photo_files[0]),
    post_md_file))

os.system("nvim %s" % (post_md_file))

