import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def fill(data_frame, method):
    data_frame.fillna(method=method, inplace=True)

def remove_spikes(data_frame):
    return data_frame.drop(pd.to_datetime(['2017-12-28','2018-03-04']))
