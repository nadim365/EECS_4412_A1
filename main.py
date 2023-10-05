import math
from file_handler import FileHandlingTools
from itemset_processor1 import FrequentItemsetCalculator1
from rule_processor import RuleGenerator
from itemset_processor import FrequentItemsetCalculator
from rule_processor1 import RuleGenerator1

SUPPORT_THRESHOLD = 0.02
CONFIDENCE_THRESHOLD = 0.6

def main():
    file_handler = FileHandlingTools('walmart1.csv', 'ID2Name.csv')
    print(f'LOADING TRANSACTIONS....')
    transactions = file_handler.load_transactions()
    frequent_itemsets_calc = FrequentItemsetCalculator1(transactions, math.ceil(SUPPORT_THRESHOLD * len(transactions)))
    prev_level = frequent_itemsets_calc.count_1_itemsets()
    print(f'GENERATING ITEMSETS.....')
    k=2
    while prev_level:
        C_k = frequent_itemsets_calc.generate_candidate(k)
        L_k = frequent_itemsets_calc.count_support(C_k)
        prev_level = L_k
        k += 1
    print(frequent_itemsets_calc.levels_itemset)
    print(f'GENERATING RULES.....')
    rule_generator = RuleGenerator1(frequent_itemsets_calc.levels_itemset, len(transactions))
    rules = rule_generator.generate_rules(CONFIDENCE_THRESHOLD)
    rules = rule_generator.quality_prune(rules)
    print(f'FORMATTING AND PRINTING THE ITEMSETS AT EACH LEVEL......')
    print("{} Levels for frequent itemsets".format(len(frequent_itemsets_calc.levels_itemset)))
    for level, itemsets in frequent_itemsets_calc.levels_itemset.items():
        print("level {}: {}".format(level, len(itemsets)))
    print(f'FORMATTING AND PRINTING THE RULES GENERATED.......')
    print("------------------------------------")
    print("{} Rules have been generated".format(len(rules)))
    for rule in rules:
        print("{} -> {} [support count: {}, confidence: {}]".format(",".join(map(file_handler.id_to_name, rule[0])), ",".join(map(file_handler.id_to_name, rule[1])), rule[2], rule[3]))
        
    

if __name__ == "__main__":
    main()