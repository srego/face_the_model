'''
This file creates a Pandas DataFrame to handle Paul image tags. 
'''


import pandas as pd


class Create_Paul_Tag_DF():
    def __init__(self, tag_dir, paul_image_dir):
        '''
        Create a Pandas DataFrame to handle Paul image tags. 
        Args:
            tag_dir (str): string representation of the working directory of the tag file. 
            paul_image_dir (str): string representation of workding directory of paul images. 
        '''
        self.tag_dir = tag_dir

        # Handle paul_image_dir structure
        if paul_image_dir[-1] != '/':
            paul_image_dir += '/'
        self.paul_image_dir = paul_image_dir

    
    # Helper function for facial hair label
    def facial_hair_helper(self, row):
        if len(row) == 3:
            return row['Facial Hair']


    def create_data_frame(self):
        '''
        Return a DataFrame with tag information. 
        '''
        df = pd.read_csv(self.tag_dir)

        # Create Directory column. 
        df['Directory'] = self.paul_image_dir + df['External ID']
        
        # Convert Label column from string to dict.
        df['Label'] = df['Label'].apply(lambda row: eval(row))

        # Create Age_label column. 
        df['Age_label'] = df['Label'].apply(lambda row: row['Age'])
       
        # Create Angle_label column. 
        df['Angle_label'] = df['Label'].apply(lambda row: row['Angle'])

        # Create Facial_hair_label column. 
        df['Facial_hair_label'] = df['Label'].apply(self.facial_hair_helper)

        return df

    # Create method to handle filter

    # Create method to output image location list. 

'''
from create_paul_tag_df import Create_Paul_Tag_DF

tag_dir = '/Users/sergiorego/face_the_model_WIP/Tools/Tagging/labelbox_output_tags.csv'
paul_image_dir = '/Users/sergiorego/face_the_model_WIP/Images/paul'

tag = Create_Tag_DF(tag_dir, paul_image_dir)
df = tag.create_data_frame()
'''