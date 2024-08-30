import pandas as pd
import os
import json
from datetime import datetime
import sys
import warnings
import argparse
import time
import shutil

# arg parser
# create the argumentParser object
parser = argparse.ArgumentParser()
# add argument using add_argument
parser.add_argument('-a', type=str, help='the path to the annotations.csv')
parser.add_argument('-u', type=str, help='the path to the users.csv')
parser.add_argument('-i', type=str, help='the path to the images.csv')
parser.add_argument('-s', type=str, help='the path to the label_schema.csv')
# parse the arguments using parse_args()
args = parser.parse_args()

def stratify_schema(label_schema):
    schema_dic = {}
    for i in range(len(label_schema)):
        schema_dic[label_schema.at[i,'M_label_id']] = {
            'label_id': label_schema.at[i,'M_label_id'],
            'label_name': label_schema.at[i,'M_label_name'],
            'label_type': int(label_schema.at[i,'M_label_type']),
            'label_parent': label_schema.at[i,'M_label_parent']
        }
    return schema_dic

def write_file(filename, label_data, regions):
    try:
        file = open(filename, mode="w")
        for region in regions:
            if 'prob' not in region:
                prob = 1.0
            else:
                prob = region['prob']
            file.write(f"{label_data[region['labelID']]['label_name']},{prob},{region['L']},{region['T']},{region['R']},{region['B']}\n")
    finally:
        file.close()

def export_db_to_localization(image_path, annotation_path, schema_path, user_path):
    image_data = pd.read_csv(image_path, encoding = 'utf-8')
    image_dic = image_data.set_index('M_image_id')
    annotation_data = pd.read_csv(annotation_path, encoding = 'utf-8')
    label_schema = pd.read_csv(schema_path, encoding = 'utf-8')
    label_data = stratify_schema(label_schema)

    if(os.path.isdir('./meta')):
        shutil.rmtree('./meta')
        os.mkdir('./meta')
    else:
        os.mkdir('./meta')

    user_data = pd.read_csv(user_path, encoding = 'utf-8')
    users = list(user_data['M_username'].unique())
    for user in users:
        annotation_sub_data = annotation_data.loc[annotation_data['username'] == user].reset_index(drop=True)
        if len(annotation_data) != 0:
            os.mkdir('./meta/' + user)
            root_path = './meta/' + user + '/'
            for i in range(len(annotation_sub_data)):
                image_id = annotation_sub_data.at[i,'image_id']
                image_name = image_dic.loc[image_id]['M_image_name']
                regions = annotation_sub_data.at[i,'regions']
                regions = json.loads(regions)
                dir = os.path.dirname(image_name)
                if dir != '':
                    dir = root_path + str(dir)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file_name = root_path + os.path.splitext(image_name)[0] + '.txt'
                    write_file(file_name, label_data, regions)
                else:
                    file_name = root_path + os.path.splitext(image_name)[0] + '.txt'
                    write_file(file_name, label_data, regions)

def main():
    # default path
    annotation_path = './annotations.csv'
    user_path = './users.csv'
    image_path = './images.csv'
    schema_path = './label_schema.csv'
    if(args.a != None):
        annotation_path = args.a
    if(args.u != None):
        user_path = args.u
    if(args.i != None):
        image_path = args.i
    if(args.s != None):
        schema_path = args.s

    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    print('begin to export region meta files...')
    time_start=time.time()
    export_db_to_localization(image_path, annotation_path, schema_path, user_path)
    time_end=time.time()
    print('time cost',time_end-time_start,'s')
    print('finished!')

if __name__ == "__main__":
    main()