import copy
from typing import List

def check_index(p_start, p_end, g_start, g_end):
    if (p_start != g_start or p_end != g_end):
        return False
    else:
        return True


def eval_gold(path_pred: str, path_gold: str, errors_path: str, errors_triples_path: str, info_path: str):
    from SpanASTE.aste.data_utils import Data

    print("Evaluation\nPath Pred: " + path_pred + "\nPath Gold: " + path_gold + "\nErrors Path: " + errors_path +
          "\nErrors Triples Path: " + errors_triples_path + "\nInfo Path: " + info_path + "\n")
    pred = Data.load_from_full_path(path_pred)
    gold = Data.load_from_full_path(path_gold)
    assert len(pred.sentences) == len(gold.sentences)
    num_pred = 0
    num_gold = 0
    num_error = 0
    num_correct = 0
    index_errors_gold = 0
    index_errors_gold_list = []
    index_errors_pred = 0
    errors_file = open(errors_path, "w", encoding='utf-8')
    info_file = open(info_path, "w", encoding='utf-8')
    errors_triples_file = open(errors_triples_path, "w", encoding='utf-8')
    polarity_errors = 0
    target_errors = 0
    target_errors_by_1 = 0
    opinion_errors = 0
    opinion_errors_by_1 = 0
    missed_triples = 0
    errors_triples_list = []

    for i in range(len(gold.sentences)):
        num_pred += len(pred.sentences[i].triples)
        num_gold += len(gold.sentences[i].triples)
        set_correct = set()
        missed_triples += len(gold.sentences[i].triples) - len(pred.sentences[i].triples)
        for p in pred.sentences[i].triples:
            error = 0
            match = 0
            errors_list = []
            for g in gold.sentences[i].triples:
                p_t_end = (p.dict().get("t_end"))
                p_o_end = (p.dict().get("o_end"))
                g_t_end = (g.dict().get("t_end"))
                g_o_end = (g.dict().get("o_end"))

                if ((p.dict().get("o_end")) > pred.sentences[i].tokens.__len__() - 1):
                    index_errors_pred += 1
                    p_o_end -= pred.sentences[i].tokens.__len__() - 1
                    error = 1

                if ((p.dict().get("t_end")) > pred.sentences[i].tokens.__len__() - 1):
                    index_errors_pred += 1
                    p_t_end -= pred.sentences[i].tokens.__len__() - 1
                    error = 1

                if ((g.dict().get("o_end")) > gold.sentences[i].tokens.__len__() - 1):
                    index_errors_gold += 1
                    g_o_end -= gold.sentences[i].tokens.__len__() - 1
                    index_errors_gold_list.append(gold.sentences[i])
                    error = 1

                if ((g.dict().get("t_end")) > gold.sentences[i].tokens.__len__() - 1):
                    index_errors_gold += 1
                    g_t_end -= gold.sentences[i].tokens.__len__() - 1
                    index_errors_gold_list.append(gold.sentences[i])
                    error = 1

                if (error):
                    print("INDEX ERROR\n\n")

                if (set_correct.__contains__(p.__str__())):
                    continue
                if (set_correct.__contains__(g.__str__())):
                    continue

                if p.dict() != g.dict():

                    if (((p.dict().get("label")) != (g.dict().get("label"))) and
                            check_index(p.dict().get("o_start"), p_o_end,
                                        g.dict().get("o_start"), g_o_end) and
                            check_index(p.dict().get("t_start"), p_t_end,
                                        g.dict().get("t_start"), g_t_end)):
                        polarity_errors += 1

                    if (p.dict().get("label") == g.dict().get("label") and
                            not check_index(p.dict().get("o_start"), p_o_end,
                                            g.dict().get("o_start"), g_o_end) and
                            check_index(p.dict().get("t_start"), p_t_end,
                                        g.dict().get("t_start"), g_t_end)):
                        opinion_errors += 1
                        if ((p.dict().get("o_start") == g.dict().get("o_start")) and
                            (p_o_end == g_o_end + 1) or (p_o_end == g_o_end - 1)) or ((p_o_end == g_o_end) and
                                                                                      ((p.dict().get(
                                                                                          "o_start") == g.dict().get(
                                                                                          "o_start") + 1)
                                                                                       or ((p.dict().get(
                                                                                                  "o_start") == g.dict().get(
                                                                                                  "o_start") - 1)))):
                            opinion_errors_by_1 += 1

                    if (p.dict().get("label") == g.dict().get("label") and
                            check_index(p.dict().get("o_start"), p_o_end,
                                        g.dict().get("o_start"), g_o_end) and
                            not check_index(p.dict().get("t_start"), p_t_end,
                                            g.dict().get("t_start"), g_t_end)):
                        target_errors += 1
                        if ((p.dict().get("t_start") == g.dict().get("t_start")) and
                            (p_t_end == g_t_end + 1) or (p_t_end == g_t_end - 1)) or ((p_t_end == g_t_end) and
                                                                                      ((p.dict().get(
                                                                                          "t_start") == g.dict().get(
                                                                                          "t_start") + 1)
                                                                                       or ((p.dict().get(
                                                                                                  "t_start") == g.dict().get(
                                                                                                  "t_start") - 1)))):
                            target_errors_by_1 += 1

                    error_message = "\nMANCATO MATCH: \n" + "Frase: \n"
                    for w in gold.sentences[i].tokens:
                        error_message += (w + " ")

                    error_message += ("\nOpinione predetta da: \"" + pred.sentences[i].tokens[
                        (p.dict().get("o_start"))] + "\" a \"" +
                                      pred.sentences[i].tokens[p_o_end] + "\"")
                    error_message += ("\nAspetto predetto da: \"" + pred.sentences[i].tokens[
                        (p.dict().get("t_start"))] + "\" a \"" +
                                      pred.sentences[i].tokens[p_t_end] + "\"")
                    error_message += ("\nPolarità predetta: " + p.dict().get("label") + "\n")

                    error_message += ("\nOpinione reale da: \"" + gold.sentences[i].tokens[
                        (g.dict().get("o_start"))] + "\" a \"" +
                                      gold.sentences[i].tokens[g_o_end] + "\"")
                    error_message += ("\nAspetto reale da: \"" + gold.sentences[i].tokens[
                        (g.dict().get("t_start"))] + "\" a \"" +
                                      gold.sentences[i].tokens[g_t_end] + "\"")
                    error_message += ("\nPolarità reale: " + g.dict().get("label") + "\n")

                    # print(error_message)
                    errors_list.append(error_message)

                else:
                    num_correct += 1
                    match = 1
                    set_correct.add(g.__str__())
                    set_correct.add(p.__str__())
                    correct_message = "CORRETTA #" + num_correct.__str__() + ": \n" + "Frase: \n"
                    for w in gold.sentences[i].tokens:
                        correct_message += (w + " ")
                    correct_message += (
                            "\nOpinione predetta da: \"" + pred.sentences[i].tokens[
                        (p.dict().get("o_start"))] + "\" a \"" +
                            pred.sentences[i].tokens[(p.dict().get("o_end"))] + "\"")
                    correct_message += (
                            "\nAspetto predetto da: \"" + pred.sentences[i].tokens[
                        (p.dict().get("t_start"))] + "\" a \"" +
                            pred.sentences[i].tokens[(p.dict().get("t_end"))] + "\"")
                    correct_message += ("\nPolarità predetta: " + p.dict().get("label") + "\n")

                    correct_message += ("\nOpinione reale da: \"" + gold.sentences[i].tokens[
                        (g.dict().get("o_start"))] + "\" a \"" +
                                        gold.sentences[i].tokens[(g.dict().get("o_end"))] + "\"")
                    correct_message += ("\nAspetto reale da: \"" + gold.sentences[i].tokens[
                        (g.dict().get("t_start"))] + "\" a \"" +
                                        gold.sentences[i].tokens[(g.dict().get("t_end"))] + "\"")
                    correct_message += ("\nPolarità reale: " + g.dict().get("label") + "\n")
                    # print(correct_message)

            if match == 0:
                num_error += 1
                error_message = "\n\nERRORE #" + num_error.__str__() + "\n\n\n"
                errors_list.insert(0, error_message)
                # print(error_message)
                errors_file.writelines(errors_list)

        for g in gold.sentences[i].triples:
            if (not set_correct.__contains__(g.__str__())):
                tmp_triple = copy.deepcopy(gold.sentences[i])
                tmp_triple.triples.clear()
                tmp_triple.triples.append(g)
                if (not errors_triples_list.__contains__(tmp_triple.to_line_format())):
                    errors_triples_list.append(tmp_triple.to_line_format())

    for i in errors_triples_list:
        errors_triples_file.write(i)

    info = dict(
        num_correct=num_correct,
        num_error=num_error,
        missed_triples=missed_triples,
        opinion_errors=opinion_errors,
        opinion_errors_by_1=opinion_errors_by_1,
        target_errors=target_errors,
        target_errors_by_1=target_errors_by_1,
        polarity_errors=polarity_errors,
        index_errors_pred=index_errors_pred,
        index_errors_gold=index_errors_gold,
    )
    print("\n\n" + info.__str__())
    info_file.write("\n\n" + info.__str__())
    for i in index_errors_gold_list:
        print(i)
    return info

def eval_gold_many(path_pred_list: List[str], path_gold: str, errors_path_list: List[str],
                   errors_triples_path_list: List[str], info_path_list: List[str]):
    assert len(path_pred_list) == len(errors_path_list) == len(errors_triples_path_list) == len(info_path_list)

    info_results = []
    for i in range(len(path_pred_list)):
        info_results.append(eval_gold(path_pred_list[i], path_gold, errors_path_list[i],
                                      errors_triples_path_list[i], info_path_list[i]))

    summary_info = dict(
        num_correct=sum(r["num_correct"] for r in info_results) / len(path_pred_list),
        num_error=sum(r["num_error"] for r in info_results) / len(path_pred_list),
        missed_triples=sum(r["missed_triples"] for r in info_results) / len(path_pred_list),
        opinion_errors=sum(r["opinion_errors"] for r in info_results) / len(path_pred_list),
        opinion_errors_by_1=sum(r["opinion_errors_by_1"] for r in info_results) / len(path_pred_list),
        target_errors=sum(r["target_errors"] for r in info_results) / len(path_pred_list),
        target_errors_by_1=sum(r["target_errors_by_1"] for r in info_results) / len(path_pred_list),
        polarity_errors=sum(r["polarity_errors"] for r in info_results) / len(path_pred_list),
        index_errors_pred=sum(r["index_errors_pred"] for r in info_results) / len(path_pred_list),
        index_errors_gold=sum(r["index_errors_gold"] for r in info_results) / len(path_pred_list),
    )
    print("\n\nSummary Info\n")
    print(summary_info)
    print("\n\n")
def check_unique_errors(path_1: str, path_2: str, path_3: str, path_4: str, path_5: str, path_final: str):
    from SpanASTE.aste.data_utils import Data
    from SpanASTE.aste.data_utils import merge_data
    print("Checking unique errors\nResults in: "+path_final+"\n")
    file_1 = Data.load_from_full_path(path_1)
    file_2 = Data.load_from_full_path(path_2)
    file_3 = Data.load_from_full_path(path_3)
    file_4 = Data.load_from_full_path(path_4)
    file_5 = Data.load_from_full_path(path_5)
    file_final = open(path_final, "w", encoding='utf-8')

    merge_file = merge_data([file_1, file_2, file_3, file_4, file_5])
    unique_triples = []
    for i in range(len(merge_file.sentences)):
        for t in merge_file.sentences[i]:
            if (not unique_triples.__contains__(merge_file.sentences[i].to_line_format())):
                unique_triples.append(merge_file.sentences[i].to_line_format())

    for i in unique_triples:
        file_final.write(i)


def check_common_errors(path_1: str, path_2: str, path_3: str, path_4: str, path_5: str, path_final: str):
    from SpanASTE.aste.data_utils import Data
    from SpanASTE.aste.data_utils import merge_data
    print("Checking common errors\nResults in: "+path_final+"\n")

    file_1 = Data.load_from_full_path(path_1)
    file_2 = Data.load_from_full_path(path_2)
    file_3 = Data.load_from_full_path(path_3)
    file_4 = Data.load_from_full_path(path_4)
    file_5 = Data.load_from_full_path(path_5)
    file_final = open(path_final, "w", encoding='utf-8')

    merge_file = merge_data([file_1, file_2, file_3, file_4, file_5])
    common_triples = []
    common_unique_triples = []
    for i in range(len(merge_file.sentences)):
        for t in merge_file.sentences[i].triples:
            common_triples.append(merge_file.sentences[i].to_line_format())

    for i in common_triples:
        if (common_triples.count(i) == 5):
            if not common_unique_triples.__contains__(i):
                common_unique_triples.append(i)

    for i in common_unique_triples:
        file_final.write(i)
