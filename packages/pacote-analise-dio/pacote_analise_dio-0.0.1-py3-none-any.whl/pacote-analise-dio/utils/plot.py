import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

def plot(data_frame):
    data_frame.plot(xlabel="Timestamp",ylabel="Value",figsize=(10, 6));

def plot_spikes(data_frame):
    f, (ax1, ax2) = plt.subplots(2, 1, figsize=(8,6)) 
    N=5

    ax1.plot(data_frame['2017-12-25':'2018-01-01'])
    ax1.set_title('First spike')
    ax1.set_ylabel("Value")

    ax1_ticks = ticker.MaxNLocator(N)
    ax1.xaxis.set_major_locator(ax1_ticks)


    ax2.plot(data_frame['2018-03-01': '2018-03-09'])
    ax2.set_title('Second spike')
    ax2.set_ylabel("Value")


    ax2_ticks = ticker.MaxNLocator(N)
    ax2.xaxis.set_major_locator(ax2_ticks)

    plt.xlabel("Timestamp")

    plt.tight_layout()
    plt.show()

def plot_missing_values(data_frame):
    data_frame.loc['2017-12': '2017-12-15'].plot.line(y='Ether', ylabel='Value', color='orange', figsize=(10, 6));