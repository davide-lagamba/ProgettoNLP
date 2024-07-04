#fonte:
#https://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


#fonte:
#https://github.com/chiayewken/Span-ASTE/blob/main/demo.ipynb
def main():
    import sys
    sys.path.append("SpanASTE/aste")
    sys.path.append("SpanASTE")
    from SpanASTE.aste.wrapper import SpanModel

    random_seed = 55
    random_seed_dataset = 50
    path_train = f"synthetic/dataset/seed_{random_seed_dataset}/train_final.txt"
    path_dev = f"synthetic/dataset/seed_{random_seed_dataset}/dev_final.txt"
    save_dir = f"outputs/synthetic/seed_{random_seed}"

    model = SpanModel(save_dir=save_dir, random_seed=random_seed)
    model.fit(path_train, path_dev)

    import json

    path_pred = f"outputs/synthetic/seed_{random_seed_dataset}/pred.txt"
    path_test = f"synthetic/dataset/seed_{random_seed_dataset}/test_final.txt"
    model.predict(path_in=path_test, path_out=path_pred)
    results = model.score(path_pred, path_test)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

