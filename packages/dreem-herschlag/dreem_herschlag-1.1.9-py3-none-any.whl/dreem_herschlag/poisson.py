import scipy.stats
import numpy as np

def compute_conf_interval(info_bases, mut_bases, alpha = 0.05):
    assert len(info_bases)==len(mut_bases), "info_bases and mut_bases must be of same length"
    ci = {}
    i, ci['min'], ci['max'], ci['low'], ci['high'] = 0, np.zeros(len(info_bases)), np.zeros(len(info_bases)), np.zeros(len(info_bases)), np.zeros(len(info_bases))
    for cov, mut in zip(info_bases, mut_bases):
        ci['min'][i], ci['max'][i] = 0.5*scipy.stats.chi2.ppf(alpha/2, df=2*mut)/cov, 0.5*scipy.stats.chi2.ppf(1-alpha/2, df=2*(mut+1))/cov
        if mut == 0:
            ci['min'][i] = 0
        ci['low'][i], ci['high'][i] = mut/cov-ci['min'][i], ci['max'][i]-mut/cov
        i = i+1
    return ci
