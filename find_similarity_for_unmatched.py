# Run from folder "laws_db"


# This script finds similarities between texts/document names of any regulation-publication pair of documents,
# if publication dates are earlier than regulation dates.

# It uses Levenshtein Distance to calculate the differences. 

# It writes comparison results into a file in case the similarity values 
# for texts/document names are higher than Q percentile of similarities obtained for shuffled matched sample. 

from multiprocessing import Pool, cpu_count
import law_functions_and_vars as lf

original_starts = 0
original_ends = 5072

# get the number of cpu cores for multiprocessing
n_processes = cpu_count()
step = int(original_ends / n_processes)

all_steps = range(original_starts, original_ends + step, step)
starts = all_steps[:-1]
ends = all_steps[1:]

Q = 0.01
dThreshold = 0.2

with Pool(n_processes) as pool:
    # suffled_matches_path = f"./results_SHUFFlEmatched_compare_by_id_0_{lf.matches.shape[0]}_TEST_3.csv"  # file writen by write_matches_comparisons for shuffled matches
    match_path = f"./results_matched_compare_by_id_0_{lf.matches.shape[0]}_TEST_3.csv"
    _args = [
        (
            Q,
            dThreshold,
            f"./results_NEW_compare_by_id_{starts[i]}_{ends[i]}_{Q}_TEST_3.csv",
            starts[i],
            ends[i],
            None,
            match_path
        )
        for i in range(len(starts))
    ]
    pool.starmap(lf.compare_laws, _args)
