

from array import array
from typing import Tuple, List, Dict
import pandas as pd
import numpy as np
import pickle
import os

def to_json(config):
    __run(config=config, format='json')

def to_csv(config):
    __run(config=config, format='csv')

def __run(config, format):
    for s in config['samples']:
        file = config['path_to_dreem_output_files']+s+'.p'
        file = file + '.gz' if config['fastq_zipped'] else file
        df = __load_pickle_to_df(file)
        if format == 'json':
            if not os.path.exists(config['path_to_json_files']):
                os.mkdir(config['path_to_json_files'])
            df.set_index('construct').to_json(config['path_to_json_files']+s+'.json', orient='index')
        if format == 'csv':            
            if not os.path.exists(config['path_to_csv_files']):
                os.mkdir(config['path_to_csv_files'])
            df.to_csv(config['path_to_csv_files']+s+'.csv')

def __load_pickle_to_df(file:str)->pd.DataFrame:
    """Load a pickle file.
    
    Args:
        path (str): the path to the pickle file.
    
    Returns:
        The pickle file content under the dataframe format.    
    """
    assert os.path.exists(file), '{} does not exist.'.format(file)

    with open(file, 'rb') as f:
        mut_hist = pickle.load(f)

    dict_df = {}
    for construct, mh in mut_hist.items():
        dict_df[construct] = mhs2dict(mh, '_MutationHistogram__bases')

    df = pd.DataFrame.from_dict(dict_df, orient='index').reset_index().drop(columns='index').rename(columns={'name':'construct'})

    return df

def mhs2dict(mhs, drop_attribute:List[str]=[])->dict:
    """Turns the output of DREEM into a 1-level construct-wise index dictionary.

    Args:
        mhs (MutationHistogram): one sample's content under DREEM's MutationHistogram class format. 
        drop_attribute (List[str]): a list of attributes from MutationHistogram class that you don't want into your dictionary
    
    Returns:
        A 1-level dictionary form of the MutationHistogram class.
    """
    mhs_copy = mhs.__dict__.copy()
    for k,v in mhs_copy.items():
        if k in drop_attribute:
            delattr(mhs, k)
        if type(v) == dict:
            for k2,v2 in v.items():
                setattr(mhs, k+'_'+k2, v2)
            delattr(mhs, k)
        if type(v) == np.array:
            setattr(mhs, k, tuple(v))
    return mhs.__dict__


