import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def information(data_frame):
    sep = "~"*30
  
    print(f"Seu dataset possui {data_frame.shape[0]} linhas e {data_frame.shape[1]} colunas.")
  
    print(sep)

    print(f"\nOs 5 primeiros elementos de seu dataset:\n\n{data_frame.head()}")
    
    print(sep)
  
    print("\nAlgumas informações a respeito de seu dataset:\n")
    data_frame.info()

    print(sep)

    print(f"\nO número de valores nulos(NaN) por coluna em seu dataset:\n\n{data_frame.isnull().sum()}")

    print(sep)

    print(f"\nUma descrição mais completa a respeito de seus dados:\n{data_frame.describe()}")