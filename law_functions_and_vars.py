# Run from folder "laws_db"


import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import numpy as np
import os, fnmatch


def write_file_with_new_delim(old_file_path, new_file_path):
    with open(old_file_path, "r+") as pf, open(new_file_path, "w+") as new_pf:
        for line in pf:
            if line[0:4].isdigit():
                line = line.replace(";", "_DELIMITER_", 2)

            new_pf.write(line)
            new_pf.write('\n')
    return


def concatenate_names(data):
    """creates table with law names, ids and dates"""

    for i in data.iloc[:-1].index:
        if (data["name"][i] is not None) & (data["name"][i + 1] is None):
            count = i + 1

            while data["name"][count] is None:
                data["name"][i] = (data["name"][i] + " " + data["id"][count])
                count += 1

    data_new = data.dropna()
    data_new.index = [i for i in range(0, data_new.shape[0])]

    return data_new


def id2list(_id, folder):
    try:
        filename = fnmatch.filter(os.listdir(f'./{folder}/files/'), f'*{_id}*.txt')[0]
        path = (f"./{folder}/files/" + filename)

        with open(path, "r+") as file:

            text = re.sub(subs, "", file.read())
            text = re.sub("\s+", " ", text).lower()
            text_list = re.split(splits, text)
            text_list = list(filter(lambda line: len(line) > 2,
                                    map(lambda x: x.strip(), filter(None, text_list))
                                    ))
    except:
        print("no such file")
        return []

    return text_list


def compare_text_by_ids(id_reg, id_pub):
    try:
        T1 = id2list(id_reg, "regulation")
        T2 = id2list(id_pub, "publication")

        if len(T1) >= len(T2):
            long_str = T1
            short_str = T2
        else:
            long_str = T2
            short_str = T1

        res = {"strs": [],
               "ratio": []}

        for string in short_str:
            res["strs"].append(process.extract(string, long_str, limit=1)[0][0])
            res["ratio"].append(process.extract(string, long_str, limit=1)[0][1])

        measure = np.mean(res["ratio"])
        return measure
    except:
        return


def compare_names_by_ids(id_reg, id_pub):
    S1 = reg_names["name"][id_reg]
    S1 = S1.replace("\ufeff|\t", "").lower()
    while S1.find("  ") > 0:
        S1 = S1.replace("  ", " ")

    S2 = pub_names["name"][id_pub]
    S2 = S2.replace("\ufeff|\t", "").lower()
    while S2.find("  ") > 0:
        S2 = S2.replace("  ", " ")

    measure = fuzz.partial_ratio(S1, S2)
    return measure


def compare_by_id(id_reg, id_pub, min_name_ratio=None):
    res = {"name_ratio": [], "text_ratio": [], "id_reg": [], "id_pub": []}

    res["name_ratio"] = compare_names_by_ids(id_reg, id_pub)
    res["id_reg"] = id_reg
    res["id_pub"] = id_pub

    name_ratio = res["name_ratio"]

    if min_name_ratio is not None:

        if res["name_ratio"] >= min_name_ratio:
            print(f"name_ratio: {name_ratio} >= min_name_ratio: {min_name_ratio}")
            res["text_ratio"] = compare_text_by_ids(id_reg, id_pub)
        else:
            print(f"name_ratio: {name_ratio} < min_name_ratio: {min_name_ratio}")
            res["text_ratio"] = -1
        return res

    else:
        res["text_ratio"] = compare_text_by_ids(id_reg, id_pub)

    return res


def write_matches_comparisons(matches, path, starts, ends):
    with open(path, "a") as file:

        with open(path, "r") as f:
            if f.readline().find("name") < 0:
                results = "name_ratio\ttext_ratio\tid_reg\tid_pub"
                print(results, file=file)

        for i in range(starts, ends):

            id_reg = matches["regulation"][i]
            id_pub = matches["publication"][i]

            res = compare_by_id(id_reg, id_pub)
            print(res)

            name_ratio, text_ratio = res["name_ratio"], res["text_ratio"]

            results = f"{name_ratio}\t{text_ratio}\t{id_reg}\t{id_pub}"

            if (not np.isnan(text_ratio)) & (text_ratio is not None):
                print(results, file=file)
    return


def write_check_treshold_on_matched_sample(matches, dThreshold, Q, path, shuffled_matches_path=None, matches_path=None):
    """If matches_path is given Q ~ 0.15, if suffled_matches_path is given Q ~ 0.95-0.99
    dThreshold - part (~ 0.1) which will be substracted from Q quantile of name_ratio in order to obtain min_name_ratio.
    dThreshold used only if matches_path is not None and suffled_matches_path=None"""

    if (shuffled_matches_path is not None) & (matches_path is None):
        shuffled_matched_ratio = pd.read_csv(shuffled_matches_path, sep="\t")
        min_name_ratio = shuffled_matched_ratio[["name_ratio", "text_ratio", ]].quantile(q=Q)[0]
        min_text_ratio = shuffled_matched_ratio[["name_ratio", "text_ratio", ]].quantile(q=Q)[1]
        print("SHUFFLED matches were used ", "Q:", Q, "min_name_ratio: ", min_name_ratio, "min_text_ratio: ",
              min_text_ratio)

    elif (shuffled_matches_path is None) & (matches_path is not None):
        matched_ratio = pd.read_csv(matches_path, sep="\t")
        min_name_ratio = matched_ratio[["name_ratio", "text_ratio", ]].quantile(q=Q)[0]
        min_name_ratio = min_name_ratio - min_name_ratio * dThreshold
        min_text_ratio = matched_ratio[["name_ratio", "text_ratio", ]].quantile(q=Q)[1]
        print("UNSHUFFLED matches were used ", "dThreshold: ", dThreshold, "Q:", Q, "min_name_ratio: ", min_name_ratio,
              "min_text_ratio: ", min_text_ratio)

    else:
        print("No matched of shuffled matched file.")

    matched_df = pd.read_csv(matches_path, sep="\t")
    # print(matched_df)

    with open(path, "a") as file:

        with open(path, "r") as f:
            if f.readline().find("name") < 0:
                results = "name_ratio\ttext_ratio\tid_reg\tid_pub\tis_same_document"
                print(results, file=file)

        # starts, ends = 0, matches.shape[0]

        for i in range(0, matched_df.shape[0]):

            id_reg = matched_df["id_reg"][i]
            id_pub = matched_df["id_pub"][i]

            # res = compare_by_id(id_reg, id_pub)
            # print(res)

            name_ratio, text_ratio = matched_df["name_ratio"][i], matched_df["text_ratio"][i]

            is_same_document = (name_ratio >= min_name_ratio)  # & (text_ratio >= min_text_ratio)

            results = f"{name_ratio}\t{text_ratio}\t{id_reg}\t{id_pub}\t{is_same_document}"
            print("\nComparison: ", results)

            if (not np.isnan(text_ratio)) & (text_ratio is not None):
                print(results, file=file)

    return


def compare_laws(Q, dThreshold, path, starts, ends, suffled_matches_path=None, matches_path=None):
    """If matches_path is given Q ~ 0.15, if suffled_matches_path is given Q ~ 0.95-0.99
    dThreshold - part (~ 0.1) which will be substracted from Q quantile of name_ratio in order to obtain min_name_ratio.
    dThreshold used only if matches_path is not None and suffled_matches_path=None"""

    if (suffled_matches_path is not None) & (matches_path is None):
        shuffled_matched_ratio = pd.read_csv(suffled_matches_path, sep="\t")
        min_name_ratio = shuffled_matched_ratio[["name_ratio", "text_ratio", ]].quantile(q=Q)[0]
        min_text_ratio = shuffled_matched_ratio[["name_ratio", "text_ratio", ]].quantile(q=Q)[1]
        print("SHUFFLED matches were used ", "Q:", Q, "min_name_ratio: ", min_name_ratio, "min_text_ratio: ",
              min_text_ratio)

    elif (suffled_matches_path is None) & (matches_path is not None):
        matched_ratio = pd.read_csv(matches_path, sep="\t")
        min_name_ratio = matched_ratio[["name_ratio", "text_ratio", ]].quantile(q=Q)[0]
        min_name_ratio = min_name_ratio - min_name_ratio * dThreshold
        min_text_ratio = matched_ratio[["name_ratio", "text_ratio", ]].quantile(q=Q)[1]
        print("UNSHUFFLED matches were used ", "dThreshold: ", dThreshold, "Q:", Q, "min_name_ratio: ", min_name_ratio,
              "min_text_ratio: ", min_text_ratio)

    else:
        print("No matched of shuffled matched file.")

    with open(path, "a") as file:
        with open(path, "r") as f:
            if f.readline().find("name") < 0:
                results = "name_ratio\ttext_ratio\tid_reg\tid_pub"
                print(results, file=file)

        for count, id_reg in enumerate(reg_names.index[starts:ends]):

            print("IRERATION: ", count)

            for id_pub in pub_names.index:
                print("id_pub: ", id_pub, "id_reg: ", id_reg)
                if pub_names["date"][id_pub] > reg_names["date"][id_reg]:

                    res = compare_by_id(id_reg, id_pub, min_name_ratio=min_name_ratio)
                    print(res)

                    name_ratio, text_ratio = res["name_ratio"], res["text_ratio"]

                    if (not np.isnan(text_ratio)) & (text_ratio is not None):
                        if (
                                name_ratio >= min_name_ratio):  # (text_ratio >= min_text_ratio) & (name_ratio >= min_name_ratio):
                            results = f"{name_ratio}\t{text_ratio}\t{id_reg}\t{id_pub}"
                            print(results, file=file)

                else:
                    print("pub_names date <= reg_names date")


subs = "|".join(
    ["«", "»", "\!", "\?", "/", "\s([а-я]|[a-z]){1,2}\.", "#", "-", "%", "\+", "=", ">|<", "'", '"', "\^", "\*",
     "и\s{1,}\(или\)", "№"])
splits = "|".join([":", ";", ",", "\.", "\r", "\*", "\n", "\n\r", "\ufeff"])

old_pub_path = "./publication/publication.csv"
new_pub_path = "./publication/new_publication.csv"

old_reg_path = "./regulation/regulation.csv"
new_reg_path = "./regulation/new_regulation.csv"

write_file_with_new_delim(old_pub_path, new_pub_path)
write_file_with_new_delim(old_reg_path, new_reg_path)

pub_names = pd.read_csv("./publication/new_publication.csv", sep="_DELIMITER_", names=["id", "date", "name"])
reg_names = pd.read_csv("./regulation/new_regulation.csv", sep="_DELIMITER_", names=["id", "date", "name"])

matches = pd.read_csv("./matches.csv", sep=";")

pub_names = concatenate_names(pub_names)
reg_names = concatenate_names(reg_names)

pub_names.id = pub_names.id.astype(int)
reg_names.id = reg_names.id.astype(int)

pub_names = pub_names.set_index("id")
reg_names = reg_names.set_index("id")

pub_names.date = pd.to_datetime(pub_names.date)
reg_names.date = pd.to_datetime(reg_names.date)
