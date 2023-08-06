#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Yalin Li <mailto.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/main/LICENSE.txt
for license details.
'''

from os import path as ospath
path = ospath.dirname(ospath.realpath(__file__))
qs_path = ospath.realpath(ospath.join(ospath.dirname(__file__), '../'))
data_path = ospath.join(qs_path, 'data')

import pandas as pd
import numpy as np
from warnings import warn
from .. import _pk

__all__ = (
    'ospath', 'load_data', 'data_path',
    'save_pickle', 'load_pickle', 'load_pickled_cmps',
    )


# %%

# =============================================================================
# Datasheet
# =============================================================================

def load_data(path=None, sheet=None, index_col=0, **kwargs):
    '''For data importing.'''
    if path.endswith(('.tsv', '.txt')):
        data = pd.read_csv(path, sep='\t', index_col=index_col, **kwargs)
    elif path.endswith('.csv'):
        data = pd.read_csv(path, index_col=index_col, **kwargs)
    elif path.endswith(('.xlsx', '.xls')):
        if sheet:
            data = pd.read_excel(path, sheet_name=sheet, engine='openpyxl',
                                 index_col=index_col, **kwargs)
        else:
            data = pd.read_excel(path, engine='openpyxl',
                                 index_col=index_col, **kwargs)
    elif path.endswith('.npy'):
        arr = np.load(path)
        index = arr[:, index_col]
        data = arr[:, np.arange(arr.shape[1]) != index_col]
        data = pd.DataFrame(data, index=index, **kwargs)
    else:
        raise ValueError('Only tab deliminted (tsv/txt), comma delimited (csv), '
                         'Excel (xlsx, xls) , or binary (.npy) files can be loaded.')
    return data



# %%

# =============================================================================
# Pickle files
# =============================================================================

def save_pickle(obj, path):
    '''Save object as a pickle file using Pickle Protocol 5.'''
    if _pk is None:
        raise RuntimeError('Current environment does not support Pickle Protocol 5, '
                           'cannot save pickle files.')
    f = open(path, 'wb')
    _pk.dump(obj, f, protocol=5)
    f.close()


def load_pickle(path):
    '''Load object saved as a pickle file using Pickle Protocol 5.'''
    if _pk is None:
        raise RuntimeError('Current environment does not support Pickle Protocol 5, '
                           'cannot load pickle files.')
    f = open(path, 'rb')
    obj = _pk.load(f)
    f.close()
    return obj


def load_pickled_cmps(components_creation_f, pickle_path, pickle=None):
    '''
    Load components from pickle, update the pickled files if needed.

    Parameters
    ----------
    pickle: bool or None.
        Whether to pickle the generated components.
        If set to None, will pickle when there is no valid pickle file
        (either the file is non-existing or it's outdated).
    '''
    if pickle == True: # repickle if asked to
        return components_creation_f(pickle=True)
    if ospath.isfile(pickle_path): # try to load pickled file
        try: return load_pickle(pickle_path)
        except: # want to repickle if there's no pickled file
            pickle = True if pickle==None else False
    if pickle is not False:
        if _pk: # repickle if can
            return components_creation_f(pickle=True)
        else:
            warn('Pickle Protocol 5 is required to pickle the components.')
            return components_creation_f(pickle=False)
    else:
        return components_creation_f(pickle=False)
