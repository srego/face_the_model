'''
Remove EXIF data from files.
'''

import os
import glob
from PIL import Image


class Remove_Exif():
    def __init__(self, root_directory):
        '''
        Open file, remove exif data, and resave file.
        Args:
            root_directory (str): path of the root directory
        '''
        # Ensure origin_directory exists.
        if not self._check_dir_exists(root_directory):
            print(root_directory + ' does not exist.')

        # Ensure directory path has / in end.
        self.root_directory = self._check_dir_name(root_directory)


    def _check_dir_exists(self, directory):
        '''
        Check if directory exists.
        Args:
            directory (str): path of directory.
        '''
        return os.path.exists(directory)


    def _check_dir_name(self, directory):
        '''
        Appends / to directory name if it is not the last character in string.
        Args:
            directory (str): path of directory.
        '''
        if directory[-1] != '/':
            return directory + '/'
        else:
            return directory

    def remove_exif(self):
        '''
        Save file without exif data.
        Args:
            self.root_directory (str): path of root directory.
        '''
        # Recursively create list with all contents in origin directory.
        files = glob.glob(self.root_directory +'**', recursive=True)

        # Resave files without exif data.
        file_count = 0
        for file in files:
            if '.' in file:
                img = Image.open(file)
                img_no_exif = Image.new(img.mode, img.size)
                img_no_exif.save(file)
                file_count += 1

        print('{} files have been resaved without exif data.'.format(file_count))



'''
Sample code:
import sys
sys.path.append('/Users/sergiorego/face_the_model_WIP/Tools/EC2')
from remove_exif_data import Remove_Exif

root_dir = '/Users/sergiorego/Desktop/test_exif'

exif_files = Remove_Exif(root_dir)
exif_files.remove_exif()
'''
