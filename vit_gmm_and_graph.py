# -*- coding: utf-8 -*-
"""ViT_GMM_and_graph.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QRmbtQoOdGiC8rQOqDYhcDiDFy-Crj97
"""

! pip install scikit-posthocs

#connect to drive

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from pathlib import Path
from scipy.ndimage import gaussian_filter
from PIL import Image
import scipy
import scikit_posthocs as sp
import seaborn as sns

def create_heatmap(csv_path,cover_img):
    csv = pd.read_csv(csv_path, header = None)

    # Save the array to a CSV file
    plt.figure(figsize=(8,8))
    plt.imshow(cover_img)
    plt.imshow(csv, cmap='jet', alpha=0.5)
    plt.axis('off')
    plt.savefig(f"/content/drive/MyDrive/resultados_ViT/cesteria_01/{csv_file[:-4]}_heatmap.png");
    plt.close()

"""#gmm"""

def create_heatmap(surface_df,csv_file, cover_img, i,dir_obj):
  csv = pd.read_csv(csv_file, header = None)

  grid = cover_img.shape[0:2] # height, width of the loaded image
  heatmap_detail = 0.01 # this will determine the gaussian blur kerner of the image (higher number = more blur)

  filter_h = int(heatmap_detail * grid[0]) // 2 * 2 + 1
  filter_w = int(heatmap_detail * grid[1]) // 2 * 2 + 1
  heatmap = gaussian_filter(csv, sigma=(filter_w, filter_h), order=0)

  # Step 1: Get height and width
  height, width = heatmap.shape
  # Step 2: Calculate remainder
  height_remainder = height % 16
  width_remainder = width % 16
  # Step 3: Eliminate last rows and columns
  new_height = height - height_remainder
  new_width = width - width_remainder
  # Update the array by keeping only the relevant portion
  your_array = heatmap[:new_height, :new_width]
  # Save the array to a CSV file
  np.savetxt(f"/content/drive/MyDrive/resultados_ViT/{dir_obj}/gmm/{i}.csv", your_array, delimiter=',')
  plt.figure(figsize=(8,8))
  plt.imshow(cover_img)
  plt.imshow(your_array, cmap='jet', alpha=0.5)
  plt.axis('off')
  plt.savefig(f"/content/drive/MyDrive/resultados_ViT/{dir_obj}/gmm/{i}.png");



def gmm(dir_obj):
  csv_folder = f"/content/drive/MyDrive/resultados_ViT/{dir_obj}/csv"
  csv_files = sorted([file for file in os.listdir(csv_folder) if file.endswith(".csv")])

  img = f'/content/drive/MyDrive/imagenes_vit/{dir_obj}.jpg'
  jpg_file = img
  cover_img = plt.imread(jpg_file)

  for csv_file in csv_files:
      csv_path = os.path.join(csv_folder, csv_file)
      create_heatmap(csv_path,csv_path, cover_img, csv_file[:-4],dir_obj)

lista = [
  "cesteria_01", "cesteria_02", "cesteria_03", "cesteria_04", "cesteria_05",
  "cesteria_06", "cesteria_07", "cesteria_08", "cesteria_09", "cesteria_10",
  "jarra_01", "jarra_02", "jarra_03", "jarra_04", "jarra_05",
  "jarra_06", "jarra_07", "jarra_08", "jarra_09", "jarra_10",
]


#list = [
#  "cesteria_01"]
#list = ['cesteria_01']

for i in lista:
  gmm(i)

"""# kullback

"""

def replace_zero(arr, small_number=1e-10):
    # Convert the array to a numpy array (optional, but it provides convenient functions)
    np_arr = np.array(arr)

    # Find the indices where the values are 0
    zero_indices = np_arr == 0

    # Replace 0 values with a small number greater than 0
    np_arr[zero_indices] = small_number

    # Return the updated array
    return np_arr.tolist()

def kullback(dir_obj):
  array = [dir_obj]


  hum = pd.read_csv(f"/content/drive/MyDrive/resultados_ViT/{dir_obj}/hum/cum_reminder.csv", header=None)
  p = hum
  p_f = replace_zero(p)


  csv_folder = f"/content/drive/MyDrive/resultados_ViT/{dir_obj}/csv"
  csv_files = sorted([file for file in os.listdir(csv_folder) if file.endswith(".csv")])

  for csv_file in csv_files:

    vit_gmm = pd.read_csv(f"/content/drive/MyDrive/resultados_ViT/{dir_obj}/csv/{csv_file}", header=None)
    q = vit_gmm
    q_f = replace_zero(q)

    kullb_hum_to_vit_et = scipy.stats.entropy(p_f, q_f)
    kl = np.sum(kullb_hum_to_vit_et)

    array.append(kl)


  return(array)

lista = [
  "cesteria_01", "cesteria_02", "cesteria_03", "cesteria_04", "cesteria_05",
  "cesteria_06", "cesteria_07", "cesteria_08", "cesteria_09", "cesteria_10",
  "jarra_01", "jarra_02", "jarra_03", "jarra_04", "jarra_05",
  "jarra_06", "jarra_07", "jarra_08", "jarra_09", "jarra_10",
]

col = [
    "img", "avg" ,"0", "1", "10", "11", "2" , "3" ,"4", "5", "6" , "7", "8", "9"
]

n = 0
for i in lista:
  col = np.vstack([col,kullback(i)])

df = pd.DataFrame(col)
new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header
df

df = df.apply(pd.to_numeric, errors='ignore')

df.dtypes

df

df.to_csv("/content/drive/MyDrive/resultados_ViT/kl_divergence.csv")

"""# KL per clases"""

def replace_zero(arr, small_number=1e-10):
    # Convert the array to a numpy array (optional, but it provides convenient functions)
    np_arr = np.array(arr)

    # Find the indices where the values are 0
    zero_indices = np_arr == 0

    # Replace 0 values with a small number greater than 0
    np_arr[zero_indices] = small_number

    # Return the updated array
    return np_arr.tolist()

def kullback_cls(dir_obj):
  array = [dir_obj]


  vit = pd.read_csv(f"/content/drive/MyDrive/resultados_ViT/{dir_obj}/gmm/{dir_obj}_attention_avg.csv", header=None)
  q = vit
  q_f = replace_zero(q)



  hum_folder = f"/content/drive/MyDrive/resultados_ViT/{dir_obj}"
  hum_files = sorted([file for file in os.listdir(hum_folder) if file.endswith(".csv")])

  for hum_file in hum_files:
    print(hum_file)
    hum = pd.read_csv(f"/content/drive/MyDrive/resultados_ViT/{dir_obj}/{hum_file}", header=None)
    p = hum
    p_f = replace_zero(p)

    kullb_hum_to_vit_et = scipy.stats.entropy(p_f, q_f)
    kl = np.sum(kullb_hum_to_vit_et)

    array.append(kl)


  return(array)

lista = [
  "cesteria_01", "cesteria_02", "cesteria_03", "cesteria_04", "cesteria_05",
  "cesteria_06", "cesteria_07", "cesteria_08", "cesteria_09", "cesteria_10",
  "jarra_01", "jarra_02", "jarra_03", "jarra_04", "jarra_05",
  "jarra_06", "jarra_07", "jarra_08", "jarra_09", "jarra_10",
]


col = [
    "img", "calculo" ,"femenino","humanista", "masculino"
]

for i in lista:
  col = np.vstack([col,kullback_cls(i)])

df = pd.DataFrame(col)
new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header
df

df.to_csv("/content/drive/MyDrive/resultados_ViT/kl_divergence_per_cls.csv")

df = pd.read_csv("/content/drive/MyDrive/resultados_ViT/kl_divergence_per_cls.csv", header = 0, index_col = 0)
df

#df = pd.read_csv("/content/drive/MyDrive/resultados_ViT/kl_divergence.csv", header = 0, index_col = 0)
sns.heatmap(data = df.iloc[:,1:], yticklabels=df.iloc[:,0] )

"""#test de medias, medianas y post hoc

Dataframe de distancias de kullback
"""

df = pd.read_csv("/content/drive/MyDrive/resultados_ViT/kl_divergence.csv", header = 0, index_col = 0)
df

"""Resumen dataframe"""

df.describe()

"""Heatmap de distancias"""

sns.heatmap(data = df.iloc[:,1:], yticklabels=df.iloc[:,0] )

"""boxplot de medias de distancias"""

sprays = df.to_numpy()

plt.figure(figsize=(8, 4))

box = sns.boxplot([df["0"], df["1"],df["2"], df["3"],df["4"], df["5"],df["6"], df["7"],df["8"], df["9"],df["10"], df["11"]] , palette="Set3")

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()

"""Combinaciones de cabezas de atención posibles"""

from itertools import combinations

df2 = df.iloc[:,2:]
df2.columns

combinations(df2.columns,2)

combs = list(combinations(df2.columns,2))

#combs

"""Test de medianas"""

qwerty = scipy.stats.median_test(df["0"], df["1"],df["2"], df["3"],df["4"], df["5"],df["6"], df["7"],df["8"], df["9"],df["10"], df["11"])
qwerty

qwerty = scipy.stats.median_test(df.iloc[:,2],df.iloc[:,3],df.iloc[:,4],df.iloc[:,5],df.iloc[:,6],df.iloc[:,7],df.iloc[:,8],df.iloc[:,9],df.iloc[:,10],df.iloc[:,11],df.iloc[:,12],df.iloc[:,13])
qwerty

"""test de medianas entre *cabezas*"""

array = []

for comb in combs:

  v = scipy.stats.median_test(df[f"{comb[0]}"], df[f"{comb[1]}"])

  array.append([comb, v.pvalue, v.median])

print(array)

"""resultados test de medianas"""

final = pd.DataFrame(array, columns = ["comb", "p-value", "median"])
final

"""Top 14 valores que tienen rechazan hipotesis nula"""

final.sort_values("p-value").head(14)

median = []
Box_median = []
columnas = []
for i in df2.columns:
  median = []
  columnas.append(i)
  for j in df2.columns:
    median.append(scipy.stats.median_test(df[f"{i}"], df[f"{j}"]).pvalue)
  Box_median.append(median)

tabla = pd.DataFrame(Box_median,index = columnas , columns=columnas )
tabla

sns.heatmap(tabla)

"""**Test de krustal wallis**"""

data = [df2["0"], df2["1"],df2["2"], df2["3"],df2["4"], df2["5"],df2["6"], df2["7"],df2["8"], df2["9"],df2["10"], df2["11"]]

# kuratkal_wallis

scipy.stats.kruskal(df2["0"], df2["1"],df2["2"], df2["3"],df2["4"], df2["5"],df2["6"], df2["7"],df2["8"], df2["9"],df2["10"], df2["11"])

"""Dunn Beforroni post hoc kruskall

Bonferroni-Dunn post hoc
"""

p_values = sp.posthoc_dunn(data, p_adjust='holm')

p_values.columns=df2.columns
p_values.index=df2.columns
p_values

sns.heatmap(data = p_values )

p_values = sp.posthoc_dunn([df2["0"], df2["1"],df2["10"], df2["11"],df2["2"], df2["3"],df2["4"], df2["5"],df2["6"], df2["7"],df2["8"], df2["9"]], p_adjust='holm')

p_values.columns=df2.columns
p_values.index=df2.columns
p_values

p_values = sp.posthoc_dunn([df2["0"], df2["1"],df2["10"], df2["11"],df2["2"], df2["3"],df2["4"], df2["5"], df2["7"],df2["8"], df2["9"]], p_adjust='holm')
p_values.columns=[0,1,10,11,2,3,4,5,7,8,9]
p_values.index=[0,1,10,11,2,3,4,5,7,8,9]

print(p_values)

sns.heatmap(data = p_values )

"""Anova"""

# anova

scipy.stats.f_oneway(df2["0"], df2["1"],df2["2"], df2["3"],df2["4"], df2["5"],df2["6"], df2["7"],df2["8"], df2["9"],df2["10"], df2["11"])

"""post hoc tukes hsd"""

hsd = scipy.stats.tukey_hsd(df2["0"], df2["1"],df2["2"], df2["3"],df2["4"], df2["5"],df2["6"], df2["7"],df2["8"], df2["9"],df2["10"], df2["11"])

print(type(hsd))

print(hsd)

"""# graficos extra"""

