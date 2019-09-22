# Cоединяет полученные с помощью скриптов find*.py файлы в 1, если name_ratio > N, делает файл с названиями и айдишниками пар
import os, fnmatch

N = 70

path = './'
files = fnmatch.filter(os.listdir(path), '*NEW*00*TEST_3*.csv')
dfs = [pd.read_csv(path+file, sep = "\t") for file in files]
DF = pd.concat(dfs)
right = DF[(DF["name_ratio"] > N)]
right.index = range(0,right.shape[0])
right.to_csv(path+"results.csv", sep = "\t")

cols = list(right.columns)


with open(path + "/names_of_compared_laws.txt", "a") as file:
    for i in range(0, right.shape[0]):
        
        line = "; ".join([f"{col}: {right[col][1]}" for col in cols])
        file.write(line)
        
        val = reg_names["name"][right["id_reg"][i]]
        line = f"\nREGULATION: {val} \n"
        file.write(line)
           
        val = pub_names["name"][right["id_pub"][i]]    
        line = f"\nPUBLICATION: {val} \n\n\n"
        file.write(line)
