'''
Remove image files that OS is not able to open.

Of 51,961 FaceScrub files, 7,189 are not working in Ubuntu.
'''


import os
from PIL import Image
from collections import defaultdict


class Remove_Faulty_Images():
    def __init__(self, root_directories):
        '''
        Remove files in root_directories that OS is not able to open.
        Prints the count of bad files, and returns a dictinonary with the faulty
        files per directory and a dictinonary with the count of faulty files per
        directory and subdirectories.
        Args:
            root_directories (list): directories with files inside.
        '''
        # Ensure directory path has / in end.
        self.root_directories = self._check_dir_name(root_directories)


    def _check_dir_name(self, directory_list):
        '''
        Ensure directory has correct syntax.
        Args:
            directory_list (list): paths of directories.
        '''
        dir_list = []
        for directory in directory_list:
            if directory[-1] != '/':
                dir_list.append(directory + '/')
            else:
                dir_list.append(directory)
        return dir_list


    def remove_files(self):
        '''
        Remove image files that OS is unable to open.
        '''
        bad_files = {dir:[] for dir in self.root_directories}
        bad_counts = defaultdict(int)
        total_bad_count = 0
        for root in self.root_directories:
            for (dirpath, _, filenames) in os.walk(root):
                for filename in filenames:
                    try:
                        if dirpath[-1] != '/':
                            dirpath += '/'
                        Image.open(dirpath + filename)
                    except OSError:
                        bad_files[root].append(filename)
                        bad_counts[dirpath] += 1
                        total_bad_count += 1
                        os.remove(dirpath + filename)
        print('{} faulty files were removed'.format(total_bad_count))
        return bad_files, bad_counts


'''
Sample code of how to run this. TRY ON A COPIED DIR FIRST.

import sys
sys.path.append('/Users/sergiorego/face_the_model_WIP/Tools/EC2')
from remove_faulty_img_files import Remove_Faulty_Images

roots = ['./images/actors/', './images/actresses/', './images/paul/']

faulty_images = Remove_Faulty_Images(roots)
faulty_files, faulty_counts = faulty_images.remove_files()

'''


'''
def error_count():
  bad_files = {k:[] for k in roots}
  bad_counts = defaultdict(int)
  i = -1
  total_bad_count = 0
  for root in roots:
    for (dirpath, dirnames, filenames) in os.walk(root):
      if i % 1000 == 0:
        print("completed file number: ", i)
      for filename in filenames:
        i += 1
        try:
          img = Image.open(dirpath + "/" + filename)
        except OSError:
          bad_files[root].append(filename)
          bad_counts[dirpath] += 1
          total_bad_count += 1
  print(bad_files)
  print(bad_counts)
  print('{} bad files were removed'.format(total_bad_count))
 '''
