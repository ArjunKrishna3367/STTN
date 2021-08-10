import os
import shutil

full_dir = "/home/akrish3367/Documents/lowres_trimmed_vids/"
directory = os.fsencode("/home/akrish3367/Documents/lowres_trimmed_vids")

#copy zip file data
# for folder in os.listdir(directory):
#     print(folder)
#     foldername = os.fsdecode(folder)
#     print(full_dir + foldername, full_dir + foldername + "/frames")
#     shutil.make_archive(full_dir + foldername, 'zip', full_dir + foldername + "/frames/")
#     shutil.copyfile(full_dir + foldername)
#      # print(os.path.join(directory, filename))
#     continue

#copy videos
for folder in os.listdir(directory):
    print(folder)
    foldername = os.fsdecode(folder)
    print(full_dir + foldername)
    shutil.copyfile("{}{}/{}.mp4".format(full_dir, foldername, foldername), "/home/gsu/workspace/STTN/examples/wildlife_360_vids/" + foldername + ".mp4")
     # print(os.path.join(directory, filename))
    continue
