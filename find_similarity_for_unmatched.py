# Run from folder "laws_db"


# This script finds similarities between texts/document names of any regulation-publication pair of documents,
# if publication dates are earlier than regulation dates.

# It uses Levenshtein Distance to calculate the differences. 

# It writes comparison results into a file in case the similarity values 
# for texts/document names are higher than Q percentile of similarities obtained for shuffled matched sample. 


import law_functions_and_vars as lf

starts = 0
ends = 1000
Q = 0.01 #0.95
dThreshold = 0.2

path = f"./results_NEW_compare_by_id_{starts}_{ends}_{Q}_TEST_3.csv"

#suffled_matches_path = f"./results_SHUFFlEmatched_compare_by_id_0_{lf.matches.shape[0]}_TEST_3.csv"  # file writen by write_matches_comparisons for shuffled matches
match_path = f"./results_matched_compare_by_id_0_{lf.matches.shape[0]}_TEST_3.csv"



lf.compare_laws(Q, dThreshold ,path, starts, ends, matches_path = match_path)
