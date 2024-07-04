import os
import re
import random

#fonte:
#https://stackoverflow.com/questions/35688126/replace-strings-in-a-file-using-regular-expressions
def change_characters(input: str, output: str):
    with open(input, 'r') as f:
        content = f.read()
        content_new = re.sub('####', '#### #### ####', content, flags=re.M)
        content_new = re.sub('\'Positive\'', '\'POS\'', content_new, flags=re.M)
        content_new = re.sub('\'Negative\'', '\'NEG\'', content_new, flags=re.M)
        content_new = re.sub('\'Neutral\'', '\'NEU\'', content_new, flags=re.M)
        output = open(output, "w")
        output.write(content_new)


#fonti:
#https://stackoverflow.com/questions/4618298/randomly-mix-lines-of-3-million-line-file
#https://stackoverflow.com/questions/34133976/splitting-lines-from-a-text-file-in-python-3

def shuffle_and_split(input_file: str, train_file: str, dev_file: str, test_file: str, train_perc: int, dev_perc: int, test_perc: int, random_seed: int):
    random.seed(random_seed)
    lines = open(input_file).readlines()
    random.shuffle(lines)
    size = lines.__len__()
    if(train_perc+dev_perc+test_perc != 100):
        print("Le percentuali dei dataset non sono valide")
        exit(-1)
    size_train = int((size/100)*train_perc)
    size_dev = int((size/100)*dev_perc)
    size_test = int((size/100)*test_perc)
    list_train = list()
    list_dev = list()
    list_test = list()
    for i in range(0, size_train):
        list_train.append(lines.__getitem__(i))

    for i in range(size_train+1, size_train+size_dev):
        list_dev.append(lines.__getitem__(i))

    for i in range(size_train+size_dev+1, size_train+size_dev+size_test):
        list_test.append(lines.__getitem__(i))

    os.mkdir(f'synthetic/dataset/seed_{random_seed}/')
    open(train_file, "w").writelines(list_train)
    open(dev_file, "w").writelines(list_dev)
    open(test_file, "w").writelines(list_test)


def remove_errors(input_file: str, output_file: str):
    from SpanASTE.aste.data_utils import Data
    index_errors = 0

    reviews = Data.load_from_full_path(input_file)

    for i in range(len(reviews.sentences)):
        for r in reviews.sentences[i].triples:

            if ((r.dict().get("o_end")) > reviews.sentences[i].tokens.__len__() - 1):
                index_errors += 1
                new_value = reviews.sentences[i].tokens.__len__() - 1
                r.__setattr__("o_end", new_value)

            if ((r.dict().get("t_end")) > reviews.sentences[i].tokens.__len__() - 1):
                index_errors += 1
                new_value = reviews.sentences[i].tokens.__len__() - 1
                r.__setattr__("t_end", new_value)

    print(index_errors.__str__()+" Index Errors rilevati")

    reviews.save_to_path(output_file)


def split_single_multi(path_file: str, path_single: str, path_multi: str):
    from SpanASTE.aste.data_utils import Data
    reviews = Data.load_from_full_path(path_file)
    single_file = open(path_single, "w", encoding='utf-8')
    multi_file = open(path_multi, "w", encoding='utf-8')
    for i in range(len(reviews.sentences)):
        single = 1
        for t in reviews.sentences[i].triples:
            if (t.dict().get("o_start") != t.dict().get("o_end") or t.dict().get("t_start") != t.dict().get("t_end")):
                single = 0
        if single == 1:
            single_file.write(reviews.sentences[i].to_line_format())
        else:
            multi_file.write(reviews.sentences[i].to_line_format())

def main():
    import sys
    sys.path.append("SpanASTE/aste")
    random_seed = 50
    train_perc = 60
    dev_perc = 15
    test_perc = 25
    change_characters(f'synthetic/dataset/train.txt', 'synthetic/dataset/train_tmp.txt')
    remove_errors(f'synthetic/dataset/train_tmp.txt', 'synthetic/dataset/train_modified.txt')
    shuffle_and_split('synthetic/dataset/train_modified.txt', f'synthetic/dataset/seed_{random_seed}/train_final.txt',
                      f'synthetic/dataset/seed_{random_seed}/dev_final.txt',
                      f'synthetic/dataset/seed_{random_seed}/test_final.txt',
                      train_perc, dev_perc, test_perc, random_seed)
    split_single_multi(f'synthetic/dataset/seed_{random_seed}/test_final.txt',
                       f'synthetic/dataset/seed_{random_seed}/test_final_single.txt',
                       f'synthetic/dataset/seed_{random_seed}/test_final_multi.txt')

if __name__ == "__main__":
    main()

