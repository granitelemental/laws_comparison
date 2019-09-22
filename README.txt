# laws_comparison
Сравнивает тексты названий законопроектов и выявляет пары, которые с наибольшей вероятностью представляют собой один законопроект на разных этапах (regulation, потом publication).

Запускать файлы нужно из папки laws_db:
python find_similarity_for_matched_and_shuffled_matched.py  && python find_similarity_for_UNmatched.py

Подобранные пары представлены в файле names_of_compared_laws.txt

name_ratio - мера совпадения названий законопроектов, text_ratio - мера совпадения текстов законопроектов,
id_reg - номер файла из папки "regulation", id_pub - номер файла из папки "publication"


