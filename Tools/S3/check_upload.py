'''
Check on upload to S3. Identify files successfully and unsuccsessfully uploaded.
'''

import os
import boto3
import pandas as pd


class S3_Upload_Check:
    '''
    Identify files successfully and unsuccsessfully uploaded from local drive to S3 bucket.     
    '''

    def __init__(self, s3_bucket, s3_folder, local_directory):
        '''
        Args:
            s3_bucket (str): String of the name of the S3 bucket. 
            s3_folder (str): String of the name of the folder in the S3 bucket. 
            local_directory (str): String of local directory or directories housing files. 
        '''
        s3 = boto3.resource('s3')
        self.s3_bucket = s3.Bucket(s3_bucket)
        self.s3_folder = s3_folder
        self.local_directory = local_directory


    def return_s3_folder_files(self):
        '''
        Return a dataframe of all files in s3_folder within bucket. 

        Arg:
            s3_folder (str): String of subfolder in S3. 

        To add:
            get URL of files
        '''
        file_lst = []
        for obj in self.s3_bucket.objects.filter(Prefix=self.s3_folder):
            # split to use only file name. 
            file_lst.append(obj.key.split('/')[-1])

        # Handle empty file_lst
        if len(file_lst) == 0:
            return 'There does not seem to be anything in {}.'.format(self.s3_folder)

        # Create dataframe with file_lst
        # exclude first element as that is just folder prefix
        return pd.DataFrame({'file': file_lst[1:]}) 


    def return_local_folder_files(self):
        '''
        Returns a dataframe with the files in the local directories. 
        '''
        file_loc = []
        file_lst = []
        for walk in os.walk(self.local_directory):
            if len(walk[1]) == 0:
                for _ in range(len(walk[-1])):
                    file_loc.append(walk[0])
                file_lst.extend(walk[2])
        return pd.DataFrame({'file': file_lst, 'directory': file_loc})


    def compare_s3_and_local(self):
        '''
        Returns the following dataframes:
            df_common = DF of files in both S3 and local directory
            df_uncommon_S3 = DF of files in S3 but not in local directory 
            (expect to be empty)
            df_uncommon_LD = DF of files in local directory but not in S3 
        '''
        df_S3 = self.return_s3_folder_files()
        df_LD = self.return_local_folder_files()
        df_common = df_S3.merge(df_LD, on=['file'])
        uncommon_S3 = df_S3[~df_S3['file'].isin(df_common['file'])]
        uncommon_LD = df_LD[~df_LD['file'].isin(df_common['file'])]
        return df_common, uncommon_S3, uncommon_LD


    def upload_missing_local_to_S3(self):
        '''
        Upload files in local directory but not in S3 to S3. 
        '''
        _, _, uncommon_LD = self.compare_s3_and_local()
        # uncommon_LD['dir_file'] = uncommon_LD['directory'] + '/' + uncommon_LD['file']
        for _, row in uncommon_LD.iterrows():
            self.s3_bucket.put_object(Key=self.s3_folder + '/' + row[0].split('/')[-1] + '/' + row[1],
                                      Body=row[-1])
        return 'Upload should be complete.'