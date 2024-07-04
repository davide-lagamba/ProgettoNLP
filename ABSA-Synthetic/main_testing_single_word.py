from testing import *


def main():
    random_seed_1 = 50
    random_seed_2 = 51
    random_seed_3 = 52
    random_seed_4 = 53
    random_seed_5 = 54
    random_seed_dataset = 50

    import sys
    import json

    sys.path.append("SpanASTE/aste")
    sys.path.append("SpanASTE")
    from SpanASTE.aste.wrapper import SpanModel

    pred_path_list = [f"outputs/synthetic/seed_{random_seed_1}/pred_single.txt",
                      f"outputs/synthetic/seed_{random_seed_2}/pred_single.txt",
                      f"outputs/synthetic/seed_{random_seed_3}/pred_single.txt",
                      f"outputs/synthetic/seed_{random_seed_4}/pred_single.txt",
                      f"outputs/synthetic/seed_{random_seed_5}/pred_single.txt"]

    errors_path_list = [f"outputs/synthetic/seed_{random_seed_1}/errors_single.txt",
                      f"outputs/synthetic/seed_{random_seed_2}/errors_single.txt",
                      f"outputs/synthetic/seed_{random_seed_3}/errors_single.txt",
                      f"outputs/synthetic/seed_{random_seed_4}/errors_single.txt",
                      f"outputs/synthetic/seed_{random_seed_5}/errors_single.txt"]

    errors_triples_path_list = [f"outputs/synthetic/seed_{random_seed_1}/errors_triples_single.txt",
                        f"outputs/synthetic/seed_{random_seed_2}/errors_triples_single.txt",
                        f"outputs/synthetic/seed_{random_seed_3}/errors_triples_single.txt",
                        f"outputs/synthetic/seed_{random_seed_4}/errors_triples_single.txt",
                        f"outputs/synthetic/seed_{random_seed_5}/errors_triples_single.txt"]

    info_path_list = [f"outputs/synthetic/seed_{random_seed_1}/info_single.txt",
                                f"outputs/synthetic/seed_{random_seed_2}/info_single.txt",
                                f"outputs/synthetic/seed_{random_seed_3}/info_single.txt",
                                f"outputs/synthetic/seed_{random_seed_4}/info_single.txt",
                                f"outputs/synthetic/seed_{random_seed_5}/info_single.txt"]

    gold_path = f"synthetic/dataset/seed_{random_seed_dataset}/test_final_single.txt"

    model_list = [SpanModel(save_dir=f"outputs/synthetic/seed_{random_seed_1}", random_seed=random_seed_1),
             SpanModel(save_dir=f"outputs/synthetic/seed_{random_seed_2}", random_seed=random_seed_2),
             SpanModel(save_dir=f"outputs/synthetic/seed_{random_seed_3}", random_seed=random_seed_3),
             SpanModel(save_dir=f"outputs/synthetic/seed_{random_seed_4}", random_seed=random_seed_4),
             SpanModel(save_dir=f"outputs/synthetic/seed_{random_seed_5}", random_seed=random_seed_5)]

    for i in range(len(model_list)):
        print("Test Single Words\nModello addestrato con random seed: "+(50+i).__str__()+"\n")
        model_list[i].predict(path_in=gold_path, path_out=pred_path_list[i])
        results = model_list[i].score(pred_path_list[i], gold_path)
        print(json.dumps(results, indent=2))

    eval_gold_many(pred_path_list, gold_path,errors_path_list,
             errors_triples_path_list, info_path_list)

    check_unique_errors(errors_triples_path_list[0], errors_triples_path_list[1],
                        errors_triples_path_list[2], errors_triples_path_list[3],
                        errors_triples_path_list[4], f"outputs/synthetic/unique_errors_triples_single.txt")

    check_common_errors(errors_triples_path_list[0], errors_triples_path_list[1],
                        errors_triples_path_list[2], errors_triples_path_list[3],
                        errors_triples_path_list[4], f"outputs/synthetic/common_errors_triples_single.txt")

if __name__ == "__main__":
    main()

