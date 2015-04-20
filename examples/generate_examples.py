# This script must be run from the examples directory. 

import os
import sys

sys.path.append("..")
import avatar_gen

usernames = ["testuser", "chrsintyre", "username", "underscore_________"]



for username in usernames:
    filename = username + ".png"
    im = avatme.make_image(username)
    im.save(filename, "PNG")

