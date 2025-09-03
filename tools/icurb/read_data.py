import os
import numpy as np
from PIL import Image
import json
from tqdm import tqdm
import multiprocessing
from functools import partial
import argparse
import pandas as pd

def crop_tiff(jp2_name, raw_data_dir, out_dir):
    with open('./tools/icurb/data_split.json','r') as jf:
        json_data = json.load(jf)
    tiff_list = json_data['train'] + json_data['valid'] + json_data['test'] + json_data['pretrain']
    raw_tiff = np.array(Image.open(os.path.join(raw_data_dir, jp2_name)))
    for ii in range(5):
        for jj in range(5):
            cropped_tiff_name = f'{jp2_name[:-4]}_{ii}{jj}'
            if cropped_tiff_name in tiff_list:
                Image.fromarray(raw_tiff[1000*ii:1000*(ii+1),1000*jj:1000*(jj+1)]).save(os.path.join(out_dir, f'{cropped_tiff_name}.tiff'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--jp2_dir',required=True, type=str, help ='The directory to store temp raw tiff data')
    parser.add_argument('--label_dir',required=True, type=str, help ='The directory to save cropped tiff data')
    args = parser.parse_args()

    jp2_list = os.listdir(args.jp2_dir)
    # print('jp2_list: ',jp2_list)
    jp2_list = [x[:-5] for x in jp2_list if x[-4:]=='tiff']
    jp2_list.sort()
    # print('jp2_list: ',jp2_list)
    df = pd.DataFrame(jp2_list, columns=['jp2_list'])
    df.to_csv('jp2_list.csv', index=False)
    label_list = os.listdir(args.label_dir)
    print('label_list: ',label_list)
    label_list = [x[:-5] for x in label_list if x[-4:]=='json']
    label_list.sort()
    df = pd.DataFrame(label_list, columns=['label_list'])
    df.to_csv('label_list.csv', index=False)
    not_in_list=[]
    for jp in jp2_list:
        if jp not in label_list:
            not_in_list.append(jp)
    not_in_list.sort()
    df = pd.DataFrame(not_in_list, columns=['not_in_label_list'])
    df.to_csv('not_in_list.csv', index=False)