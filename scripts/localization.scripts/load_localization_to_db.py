'''
Input: path to image.csv, path to user.csv, path to label_schema.csv and path to the meta files
Output: annotations.csv that can be used to update the database
'''

import pandas as pd
import os
import json
from datetime import datetime
import sys
import warnings
import argparse
import time
import pytz

# arg parser
# create the argumentParser object
parser = argparse.ArgumentParser()
# add argument using add_argument
parser.add_argument('-m', type=str, help='the path to the meta files')
parser.add_argument('-u', type=str, help='the path to the users.csv')
parser.add_argument('-i', type=str, help='the path to the images.csv')
parser.add_argument('-s', type=str, help='the path to the label_schema.csv')
# parse the arguments using parse_args()
args = parser.parse_args()

def generate_annotate_json(meta_path, label_name_data):
    files = os.listdir(meta_path)
    filename_list = []
    for f in files:
        # filename = f.replace(':','/')
        filename = f.replace('.txt','')
        filename_list.append(filename)
    localization_dic = {}
    current_time = datetime.now(pytz.utc).strftime("%m/%d/%Y, %H:%M:%S.%f")[:-3]
    for filename in filename_list:
        try:
            f = open(meta_path + filename + '.txt', 'r') 
            content=f.readlines() 
            table_list = [] # store the image meta info
            text_index = 0
            localization_dic[filename] = []
            for index, item in enumerate(content):
                row = item.lstrip()
                row = row.split(',')
                if row[0] not in label_name_data:
                    print(f"unknown label name {row[0]}, please check your label_schema.csv!")
                    exit()
                localization_dic[filename].append({
                    'labelType': 'AI',
                    'labelID': label_name_data[row[0]]['label_id'],
                    'prob': row[1],
                    'timestamp': current_time,
                    'L': row[2],
                    'T': row[3],
                    'R': row[4],
                    'B': row[5].replace('\n','')
                })
        finally:
            if f:
                f.close()
    # print(localization_dic)
    # with open('result.json', 'w') as fp:
    #     json.dump(localization_dic, fp)
    return localization_dic

def parse_meta_file(meta_path, label_name_data, current_time):
    localizations = []
    try:
        f = open(meta_path, 'r') 
        content=f.readlines() 
        for index, item in enumerate(content):
            row = item.lstrip()
            row = row.split(',')
            if row[0] not in label_name_data:
                print(f"unknown label name {row[0]}, please check your label_schema.csv!")
                exit()
            localizations.append({
                'labelType': 'AI',
                'labelID': label_name_data[row[0]]['label_id'],
                'prob': row[1],
                'timestamp': current_time,
                'L': row[2],
                'T': row[3],
                'R': row[4],
                'B': row[5].replace('\n','')
            })
    finally:
        if f:
            f.close()
    return localizations

def stratify_schema(label_schema):
    schema_dic = {}
    for i in range(len(label_schema)):
        schema_dic[label_schema.at[i,'M_label_id']] = {
            'label_id': label_schema.at[i,'M_label_id'],
            'label_type': int(label_schema.at[i,'M_label_type']),
            'label_parent': label_schema.at[i,'M_label_parent']
        }
    return schema_dic

def stratify_schema_name(label_schema):
    schema_dic = {}
    for i in range(len(label_schema)):
        schema_dic[label_schema.at[i,'M_label_name']] = {
            'label_id': label_schema.at[i,'M_label_id'],
            'label_type': int(label_schema.at[i,'M_label_type']),
            'label_parent': label_schema.at[i,'M_label_parent']
        }
    return schema_dic

def stratify_image(image_data):
    image_dic = {}
    for i in range(len(image_data)):
        image_dic[image_data.at[i,'M_image_id']] = {
            'image_id': image_data.at[i,'M_image_id'],
            'image_name': image_data.at[i,'M_image_name'].split('.')[0]}
    return image_dic

def load_localization_to_db(meta_path, user_path, image_path, schema_path, replaceDB = True):
    '''
    @replaceDB: if the original database will be overwritten
    '''
    label_schema = pd.read_csv(schema_path, encoding = 'utf-8')
    label_name_data = stratify_schema_name(label_schema)
    label_data = stratify_schema(label_schema)
    image_data = pd.read_csv(image_path, encoding = 'utf-8')
    image_data = image_data.set_index('M_image_id')
    current_time = datetime.now(pytz.utc).strftime("%m/%d/%Y, %H:%M:%S.%f")[:-3]
    if replaceDB:
        user_data = pd.read_csv(user_path, encoding = 'utf-8')
        anno_table_list = []
        id = 0
        for i in range(len(user_data)):
            username = user_data.at[i,'M_username']
            if pd.isna(user_data.at[i,'M_assignment_by_image_id']):
                assignment = []
            else:
                assignment = user_data.at[i,'M_assignment_by_image_id'].split(';')
            if(len(assignment) == 1 and assignment[0] == ''):
                assignment = []
            for image_id in assignment:
                anno_table_dic = {}
                anno_table_dic['id'] = id
                id += 1
                anno_table_dic['image_id'] = image_id
                anno_table_dic['username'] = username
                anno_table_dic['annotation_log'] = ""
                anno_table_dic['log_dates'] = ""
                anno_table_dic['is_error_image'] = 0
                anno_table_dic['need_discuss'] = 0
                anno_table_dic['marked_fun'] = 0
                anno_table_dic['marked_OK'] = 0
                anno_table_dic['checked_caption'] = 0
                anno_table_dic['checked_paper'] = 0
                anno_table_dic['marked_excluded'] = 0
                anno_table_dic['placeholder_integer1'] = 0
                anno_table_dic['placeholder_integer2'] = 0
                anno_table_dic['placeholder_integer3'] = 0
                anno_table_dic['placeholder_text1'] = ''
                anno_table_dic['placeholder_text2'] = ''
                anno_table_dic['placeholder_text3'] = ''
                for label in label_data:
                    if(int(label_data[label]['label_type']) == 0):
                        pass
                    elif(int(label_data[label]['label_type']) == 1):
                        anno_table_dic[label] = int(0)
                    elif(int(label_data[label]['label_type']) == 2):
                        anno_table_dic[label['label_parent']] = ""
                    elif(int(label_data[label]['label_type']) == 3):
                        anno_table_dic[label] = ""
                    elif(int(label_data[label]['label_type']) == -1):
                        anno_table_dic[label] = ""
                image_name = image_data.loc[image_id]['M_image_name']
                meta_file_path = meta_path + image_name
                meta_file_path = os.path.splitext(meta_file_path)[0]
                meta_file_path = meta_file_path + '.txt'
                if os.path.exists(meta_file_path):
                    localization_res = parse_meta_file(meta_file_path, label_name_data, current_time)
                    for bbox in localization_res:
                        if label_data[bbox['labelID']]['label_type'] == 1:
                            anno_table_dic[bbox['labelID']] = int(1)
                        elif label_data[bbox['labelID']]['label_type'] == 2:
                            anno_table_dic[label_data[bbox['labelID']]['label_parent']] = bbox['labelID']
                    anno_table_dic['regions'] = json.dumps(localization_res)
                else:
                    print(f"Cannot find the meta data {meta_file_path}")
                    anno_table_dic['regions'] = ""
                anno_table_list.append(anno_table_dic)
        df = pd.DataFrame(anno_table_list)
    df.to_csv('./annotations.csv',index=False)

def main():
    # default path
    meta_path = './meta/'
    user_path = './users.csv'
    image_path = './images.csv'
    schema_path = './label_schema.csv'
    if(args.m != None):
        meta_path = args.m
    if(args.u != None):
        user_path = args.u
    if(args.i != None):
        image_path = args.i
    if(args.s != None):
        schema_path = args.s

    if meta_path[-1] != '/':
        meta_path += '/'

    print('begin to convert data into the database format...')
    time_start=time.time()
    load_localization_to_db(meta_path, user_path, image_path, schema_path)
    time_end=time.time()
    print('time cost',time_end-time_start,'s')
    print('finished!')

if __name__ == "__main__":
    main()