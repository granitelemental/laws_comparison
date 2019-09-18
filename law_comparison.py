import law_functions as lf

pub_names = pd.read_csv("/home/alena/Desktop/Laws/laws_db/publication/new_publication.csv",sep="_DELIMITER_",names=["id","date","name"])
reg_names = pd.read_csv("/home/alena/Desktop/Laws/laws_db/regulation/new_regulation.csv",sep="_DELIMITER_",names=["id","date","name"])

matches = pd.read_csv("/home/alena/Desktop/Laws/laws_db/matches.csv", sep = ";")

pub_names = lf.concatenate_names(pub_names)
reg_names = lf.concatenate_names(reg_names)

pub_names.id = pub_names.id.astype(int)
reg_names.id = reg_names.id.astype(int)

pub_names = pub_names.set_index("id")
reg_names = reg_names.set_index("id")

pub_names.date = pd.to_datetime(pub_names.date)
reg_names.date = pd.to_datetime(reg_names.date)


results = lf.get_sample_matches(matches.iloc[:-1],min_similarity=50)
results_df = pd.DataFrame(results).dropna()


shuffled_matches = matches.copy()
shuffled_matches["publication"] = np.random.permutation(shuffled_matches["publication"].values)

shuffled_results = lf.get_sample_matches(shuffled_matches.iloc[:-1],min_similarity=50)
shuffled_results_df = pd.DataFrame(shuffled_results).dropna()

