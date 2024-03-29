import math
from file_handler import FileHandlingTools
from itemset_processor import FrequentItemsetCalculator
from rule_processor import RuleGenerator

SUPPORT_THRESHOLD = 0.03
CONFIDENCE_THRESHOLD = 0.07


def main():
    file_handler = FileHandlingTools('walmart1.csv', 'ID2Name.csv')
    transactions = file_handler.load_transactions()
    frequent_itemsets_calc = FrequentItemsetCalculator(
        transactions, math.ceil(SUPPORT_THRESHOLD * len(transactions)))
    prev_level = frequent_itemsets_calc.count_1_itemsets()
    k = 2
    while prev_level:
        C_k = frequent_itemsets_calc.generate_candidate(k)
        L_k = frequent_itemsets_calc.count_support(C_k)
        prev_level = L_k
        k += 1
    rule_generator = RuleGenerator(
        frequent_itemsets_calc.levels_itemset, len(transactions))
    rules = rule_generator.generate_rules(CONFIDENCE_THRESHOLD)
    rules = rule_generator.quality_prune(rules)
    print("{} Levels for frequent itemsets".format(
        len(frequent_itemsets_calc.levels_itemset)))
    for level, itemsets in frequent_itemsets_calc.levels_itemset.items():
        print("level {}: {}".format(level, len(itemsets)))
    print("------------------------------------")
    print("{} Rules have been generated".format(len(rules)))
    for rule in rules:
        print("{} -> {} [support count: {}, confidence: {}]".format(",".join(map(file_handler.id_to_name,
              rule[0])), ",".join(map(file_handler.id_to_name, rule[1])), rule[2], rule[3]))


if __name__ == "__main__":
    main()
