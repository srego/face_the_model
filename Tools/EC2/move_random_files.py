'''
Move a random number of files from a one directory to another. 
'''

import os
import glob
import shutil
import numpy as np
from keras.preprocessing import image


class Move_Random_Files():
    def __init__(self, number_of_files, origin_directory, desination_directory):
        '''
        Randomly choose number_of_files to be copied from origin_directory to 
        desination_directory. Recursively searches directory for for files.  
        Args:
            number_of_files (int): number of files to be copied.
            origin_directory (str): source location of the files.
            destination_directory (str): destination location of the files. 
        '''
        self.number_of_files = number_of_files
        
        # Ensure directory path has / in end. 
        self.origin_directory = self._check_dir_name(origin_directory)
        self.desination_directory = self._check_dir_name(desination_directory)

        # Ensure origin_directory exists.
        if not self._check_dir_exists(self.origin_directory):
            print(self.origin_directory + ' does not exist.')

        # Check if destination directory exists. If not, create it. 
        if not self._check_dir_exists(self.desination_directory):
            self._create_directory(self.desination_directory)
            print(self.desination_directory, 'does not exist, but has been created.')


    def _check_dir_name(self, directory):
        '''
        Appends / to directory name if it is not the last character in string. 
        '''
        if directory[-1] != '/':
            return directory + '/'
        else:
            return directory


    def _check_dir_exists(self, directory):
        '''
        Check if directory exists.
        Args:
            directory (str): path of directory. 
        '''
        return os.path.exists(directory)


    def _create_directory(self, directory):
        '''
        Creates directory. 
        Args:
            directory (str): path of directory. 
        '''
        os.makedirs(directory)


    def move_files(self):
        '''
        Move randomly chosen number of files from origin to destination directory. 
        '''
        # Recursively create list with all contents in origin directory. 
        origin_contents = glob.glob(self.origin_directory +'**', recursive=True)

        # Keep only files in list. 
        origin_files = []
        for content in origin_contents:
            if '.' in content:
                # Conduct error check
                origin_files.append(content)
                try:
                    image.load_img(content, target_size=(256, 256))
                except:
                    os.remove(content)
                    origin_files.remove(content)

        # Choose files at random without replacement. 
        random_files = np.random.choice(origin_files, self.number_of_files, replace=False)

        # Copy files 
        for file in random_files:
            shutil.move(file, self.desination_directory + file.split('/')[-1])


'''
Sample code:
import sys
sys.path.append('/home/ubuntu/face_the_model/Tools/EC2')
from copy_random_files import Copy_Random_Files
root_dir_actor = '/home/ubuntu/images/actors'
dest_dir_actor = '/home/ubuntu/paul_model_4/training_set/not_paul'

files_to_copy = Copy_Random_Files(1585, root_dir_actor, dest_dir_actor)
files_to_copy.copy_files()

dest_dir_actor = '/home/ubuntu/paul_model_4/test_set/not_paul'
files_to_copy = Copy_Random_Files(1000, root_dir_actor, dest_dir_actor)
files_to_copy.copy_files()



origin_dir = '/Users/sergiorego/Desktop/test_walk'
dest_dir_paul = '/Users/sergiorego/Desktop/test_dest/paul'

file_copy = Copy_Random_Files(3, origin_dir, dest_dir_paul)

file_copy.copy_files()

'''