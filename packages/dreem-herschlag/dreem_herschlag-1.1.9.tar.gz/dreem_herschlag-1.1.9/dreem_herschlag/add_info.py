import pickle
from dreem_herschlag import rnastructure, poisson, export
import pandas as pd
from tqdm.auto import tqdm
import numpy as np

class AddInfo(object):
    def __init__(self, config) -> None:
        self.samples = config['samples']
        self.config = config
        self.rna = rnastructure.RNAstructure(config)
    
    def run(self):
        if self.config['use_samples']:
            df_samp = pd.read_csv(self.config['temp_folder']+'/samples.csv')
        if self.config['use_library']:
            df_lib = pd.read_csv(self.config['temp_folder']+'/library.csv').astype({'name':str}).set_index('name')
        for s in self.samples:
            path = self.config['path_to_dreem_output_files']
            pf = pickle.load(open(path + s +'.p', 'rb'))
            for name, mh in tqdm(pf.items(), total= len(pf), unit='construct', colour='green', postfix= 'sample:'+str(s)):
                if self.config['use_samples']:
                    df_samp['sample'] = df_samp['sample'].astype(str)
                    for col in df_samp.drop(columns=['sample']).columns:
                        assert not (data:=df_samp[col].loc[df_samp['sample']==s]).empty, f"{s} doesn't have {col} in samples.csv"
                        setattr(mh,col,data.iloc[0])
                if self.config['use_library']:
                    for col in df_lib.columns:
                        try:
                            data =df_lib[col].loc[name]
                        except:
                            print( f"{name} not found in library.csv for col {col}")
                        setattr(mh,col,data)
                if self.config['use_rnastructure']:
                    rna_pred = self.rna.run(s, mh)
                    for name, val in rna_pred.items():
                        setattr(mh, name, val)

                if self.config['use_poisson']:
                    ci = poisson.compute_conf_interval(info_bases=mh.info_bases[1:], mut_bases=mh.mut_bases[1:])
                    for k,v in ci.items():
                        setattr(mh,'poisson_'+k,v)
            pickle.dump(pf, open(path + s +'.p', 'wb'))
        