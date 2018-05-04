'''
Copy a random number of files from a one directory to another. 
'''

import os
import glob
import shutil
import numpy as np


class Copy_Random_Files():
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


    def copy_files(self):
        '''
        Copy randomly chosen number of files from origin to destination directory. 
        '''
        # Recursively create list with all contents in origin directory. 
        origin_contents = glob.glob(self.origin_directory +'**', recursive=True)

        # Keep only files in list
        origin_files = []
        for content in origin_contents:
            if '.' in content:
                origin_files.append(content)

        # Choose files at random without replacement. 
        random_files = np.random.choice(origin_files, self.number_of_files, replace=False)

        # Copy files 
        for file in random_files:
            shutil.copyfile(file, self.desination_directory + file.split('/')[-1])


'''
Sample code:
origin_dir = '/Users/sergiorego/Desktop/test_walk'
dest_dir_paul = '/Users/sergiorego/Desktop/test_dest/paul'

file_copy = Copy_Random_Files(3, origin_dir, dest_dir_paul)

file_copy.copy_files()

'''