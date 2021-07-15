import os
import shutil

full_dir = "/home/gsu/Documents/lowres_trimmed_vids/"
directory = os.fsencode("/home/gsu/Documents/lowres_trimmed_vids")

for folder in os.listdir(directory):
    print(folder)
    foldername = os.fsdecode(folder)
    print(full_dir + foldername, full_dir + foldername + "/frames")
    shutil.make_archive(full_dir + foldername, 'zip', full_dir + foldername + "/frames/")
     # print(os.path.join(directory, filename))
    continue
