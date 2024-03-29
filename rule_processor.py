from itertools import combinations

from file_handler import FileHandlingTools
from itemset_processor import FrequentItemsetCalculator


class RuleGenerator(object):

    def __init__(self, levels_itemset, num_transactions):
        # frequent itemsets with their support counts dict[ level: {itemset: supportcount } ]
        self.levels_itemset: dict = levels_itemset
        self.num_transactions = num_transactions  # int

    def generate_rules(self, confidence_threshold):
        # TODO: This function generates the association rules from the frequent itemsets and returns the list of rules.
        # rules are of the form (X, Y, support, confidence) which means X => Y [support, confidence]
        rules = []
        # Traverse across the itemsets generated for each level except 1 and generating possible rules
        for k, v in self.levels_itemset.items():
            if k != 1:
                for itemset, supp in v.items():
                    for i in range(1, k):
                        # Generating possible subsets for antecedent of rule and finding consequent
                        for comb in combinations(itemset, i):
                            rule = []
                            x = frozenset(comb)  # Antecedent
                            size = len(x)
                            y = itemset.difference(x)  # Consequent
                            confidence = supp / \
                                self.levels_itemset[size][frozenset(x)]
                            if confidence >= confidence_threshold:  # Pruning if rule does not meet the given confidence threshold
                                rule.append(x)
                                rule.append(y)
                                rule.append(supp)
                                rule.append(confidence)
                                rules.append(tuple(rule))

        return rules
        # return rules

    def quality_prune(self, rules):
        # TODO: This function prunes the misleading rules by using the lift measure and returns the updated list of rules.
        # lift(X => Y) = "confidence(X => Y) / support(Y)" or "P(X and Y) / (P(X) * P(Y))"
        quality_rules = []

        for x, y, supp, conf in rules:
            x_supp = 0
            y_supp = 0

            # Finding the support counts of the antecendent and consequent
            if len(x) > 1 or len(y) > 1:
                for level, itemsets in self.levels_itemset.items():
                    for itemset, supp in itemsets.items():
                        if x == itemset:
                            x_supp = self.levels_itemset[level][itemset]
                        if y == itemset:
                            y_supp = self.levels_itemset[level][itemset]
            else:
                x_supp = self.levels_itemset[1][x]
                y_supp = self.levels_itemset[1][y]

            #lift = (supp/self.num_transactions) / \
             #   (
              #      (x_supp / self.num_transactions) *
               # (y_supp / self.num_transactions)
            #)
            lift = conf / (y_supp / self.num_transactions)


            # Using lift measure to prune misleading rules
            if lift > 1.0:
                rule = (x, y, supp, conf, lift)
                quality_rules.append(rule)
        return quality_rules


if __name__ == "__main__":
    fileHandler = FileHandlingTools("data.csv", "mapping.csv")
    transactions = fileHandler.load_transactions()
    calc = FrequentItemsetCalculator(transactions, 0.3*len(transactions))
    prev_level = calc.count_1_itemsets()
    k = 2
    while prev_level:
        C_k = calc.generate_candidate(k)
        L_k = calc.count_support(C_k)
        prev_level = L_k
        k += 1

    rule_generator = RuleGenerator(calc.levels_itemset, len(transactions))
    rules = rule_generator.generate_rules(0.6)
    rules = rule_generator.quality_prune(rules)
    print(f'RULES: {rules}')
    # print(rules)
