# Run from folder "laws_db"

# This script finds and writes similarities between texts/document names of regulation-publication pair of documents 
# from matched sample and suffled matched sample.

# It uses Levenshtein Distance to calculate the differences.


import numpy as np
import law_functions_and_vars as lf

shuffled_matches = lf.matches.copy()
shuffled_matches["publication"] = np.random.permutation(shuffled_matches["publication"].values)

starts = 0
ends = lf.matches.shape[0]
Q = 0.01 #0.95
dThreshold = 0.2

match_path = f"./results_matched_compare_by_id_{starts}_{ends}_TEST_3.csv"
lf.write_matches_comparisons(lf.matches, match_path, starts, ends)
print("File written: ", match_path)

shuffled_path = f"./results_SHUFFlEmatched_compare_by_id_{starts}_{ends}_TEST_3.csv"
lf.write_matches_comparisons(shuffled_matches, shuffled_path, starts, ends)
print("File written: ", shuffled_path)


check_path = f"./check_results_on_matched_sample_TEST_3.csv"
lf.write_check_treshold_on_matched_sample(lf.matches, dThreshold, Q, check_path, matches_path=match_path)
print("File written: ", check_path)
