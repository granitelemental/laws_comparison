# laws_comparison

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import numpy as np
import os, fnmatch
import string

def concatenate_names(data):
    """creates table with law names, ids and dates"""
    for i in data.iloc[:-1].index:
        
        if (data["name"][i] is not np.nan) & (data["name"][i+1] is np.nan):
            
            count = i+1
            
            while data["name"][count] is np.nan:
                
                data["name"][i] = (data["name"][i] + " " + data["id"][count])
                count += 1
                
    data_new = data.dropna()
    data_new.index = [i for i in range(0,data_new.shape[0])]
    
    return data_new



     

def file2str(id, folder):
    try:
        filename = fnmatch.filter(os.listdir(f'/home/alena/Desktop/Laws/laws_db/{folder}/files/'), f'*{id}*.txt')[0]
        path = (f"/home/alena/Desktop/Laws/laws_db/{folder}/files/"+filename)
        with open(path,"r+") as file:
            text = ""
            for line in file.readlines():

                text = text + line

                text = text.replace("\t"," ").replace("\ufeff"," ").strip().lower()

                trans = str.maketrans('', '', string.punctuation)
                text = text.translate(trans)

                while text.find("  ")>0:
                    text = text.replace("  "," ")

        #print(text)
        return text    
    except:
        print(f"cannot find file: *{id}.txt in /home/alena/Desktop/Laws/laws_db/{folder}/files/")
        return None

    
    
def compare_strings(S1,S2):
   
    try:
        strs = [S1,S2]
        strs_sorted = sorted(strs, key=len) # in lst2 short string - first string

        #print("Example string: ", strs_sorted[0],"\n")

        str_list_short  = strs_sorted[0].split(" ")
        str_list_long = strs_sorted[1].split(" ")

        rates = []
        compared_strs = []

        len_diff = len(str_list_long) - len(str_list_short)

        for begining in range(0,len_diff+1):

            compared_str = " ".join(str_list_long[begining:begining + len(str_list_short)])
            res = fuzz.ratio(compared_str,strs_sorted[0])
            #print("similarity: ", res, " pair: ",[compared_str,strs_sorted[0]])
            rates.append(res)

        return max(rates)
    except:
        print("one or both input strings are None")
        return None
    
    
    
def is_texts_match(S1, S2, min_similarity=90):
    """ S1, S2 - textstrings returned by text2str"""
    try:
        similarity = compare_strings(S1, S2)


        if similarity >= min_similarity:
            print(similarity)
            return True, similarity
        else:
            return False, similarity
    except:
        print("S1, S2 or min_similarity are None")
        return None, None
            

    
def get_is_texts_match_by_id(id_pub, id_reg, min_similarity=50):
    
    try:

        S1 = file2str(id_reg,"regulation")
        S2 = file2str(id_pub,"publication")

        res = is_texts_match(S1,S2,min_similarity = min_similarity)

        return res
    except:
        return None, None
        
