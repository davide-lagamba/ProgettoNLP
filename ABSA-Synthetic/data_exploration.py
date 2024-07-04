
def explore_dataset(train_path: str, dev_path: str, test_path: str):
    from SpanASTE.aste.data_utils import LabelEnum
    from SpanASTE.aste.data_utils import Data
    train = Data.load_from_full_path(train_path)
    dev = Data.load_from_full_path(dev_path)
    test = Data.load_from_full_path(test_path)
    train_lines = len(train.sentences)
    dev_lines = len(dev.sentences)
    test_lines = len(test.sentences)
    positive_train = 0
    negative_train = 0
    neutral_train = 0
    single_train = 0
    multi_train = 0
    positive_dev = 0
    negative_dev = 0
    neutral_dev = 0
    single_dev = 0
    multi_dev = 0
    positive_test = 0
    negative_test = 0
    neutral_test = 0
    single_test = 0
    multi_test = 0
    for i in range(len(train.sentences)):
        for t in train.sentences[i].triples:
            if (t.dict().get("label") == LabelEnum.positive):
                positive_train += 1
            if (t.dict().get("label") == LabelEnum.negative):
                negative_train += 1
            if (t.dict().get("label") == LabelEnum.neutral):
                neutral_train += 1
            if(t.dict().get("o_start")!=t.dict().get("o_end") or t.dict().get("t_start")!=t.dict().get("t_end")):
                multi_train += 1
            else:
                single_train += 1

    for i in range(len(dev.sentences)):
        for t in dev.sentences[i].triples:
            if (t.dict().get("label") == LabelEnum.positive):
                positive_dev += 1
            if (t.dict().get("label") == LabelEnum.negative):
                negative_dev += 1
            if (t.dict().get("label") == LabelEnum.neutral):
                neutral_dev += 1
            if(t.dict().get("o_start")!=t.dict().get("o_end") or t.dict().get("t_start")!=t.dict().get("t_end")):
                multi_dev += 1
            else:
                single_dev += 1

    for i in range(len(test.sentences)):
        for t in test.sentences[i].triples:
            print(t)
            if (t.dict().get("label") == LabelEnum.positive):
                positive_test += 1
            if (t.dict().get("label") == LabelEnum.negative):
                negative_test += 1
            if (t.dict().get("label") == LabelEnum.neutral):
                neutral_test += 1
            if(t.dict().get("o_start")!=t.dict().get("o_end") or t.dict().get("t_start")!=t.dict().get("t_end")):
                multi_test += 1
            else:
                single_test += 1

    print("Dataset train")
    print("Num Reviews: "+str(train_lines))
    print("Positive Triples: "+str(positive_train))
    print("Neutral Triples: "+str(neutral_train))
    print("Negative Triples: "+str(negative_train))
    print("Single Triples: "+str(single_train))
    print("Multi Triples: "+str(multi_train)+"\n")

    print("Dataset dev")
    print("Num Reviews: " + str(dev_lines))
    print("Positive Triples: " + str(positive_dev))
    print("Neutral Triples: " + str(neutral_dev))
    print("Negative Triples: " + str(negative_dev))
    print("Single Triples: " + str(single_dev))
    print("Multi Triples: " + str(multi_dev)+"\n")

    print("Dataset test")
    print("Num Reviews: " + str(test_lines))
    print("Positive Triples: " + str(positive_test))
    print("Neutral Triples: " + str(neutral_test))
    print("Negative Triples: " + str(negative_test))
    print("Single Triples: " + str(single_test))
    print("Multi Triples: " + str(multi_test)+"\n")


def main():
    import sys
    sys.path.append("aste")
    explore_dataset('synthetic/dataset/seed_50/train_final.txt', 'synthetic/dataset/seed_50/dev_final.txt',
                    'synthetic/dataset/seed_50/test_final.txt')


if __name__ == "__main__":
    main()

