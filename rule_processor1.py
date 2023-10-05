from itertools import combinations

from file_handler import FileHandlingTools
from itemset_processor import FrequentItemsetCalculator
from itemset_processor1 import FrequentItemsetCalculator1


class RuleGenerator1(object):

    def __init__(self, levels_itemset, num_transactions):
        self.levels_itemset: dict = levels_itemset #frequent itemsets with their support counts dict[tuple, int]
        self.num_transactions = num_transactions #int

    def generate_rules(self, confidence_threshold):
        #TODO: This function generates the association rules from the frequent itemsets and returns the list of rules.
        # rules are of the form (X, Y, support, confidence) which means X => Y [support, confidence]
        rules = []
        print(self.levels_itemset)
        for k,v in self.levels_itemset.items():
            for itemset, supp in v.items():
                if len(itemset) > 1:
                    for comb in combinations(itemset, k-1):
                        rule = []
                        x = frozenset(comb)
                        size = len(x)
                        y = itemset.difference(x)
                        confidence = supp / self.levels_itemset[size][frozenset(x)]
                        print(f'X: {x} Y: {y} CONFIDENCE: {confidence}')
                        if confidence >= confidence_threshold:
                            rule.append(x)
                            rule.append(y)
                            rule.append(supp)
                            rule.append(confidence)
                            rule = tuple(rule)
                            rules.append(rule)
                            print(f'RULE: {rule}')
                        
        return rules
        #return rules
    
    def quality_prune(self, rules):
        #TODO: This function prunes the misleading rules by using the lift measure and returns the updated list of rules.
        # lift(X => Y) = "confidence(X => Y) / support(Y)" or "P(X and Y) / (P(X) * P(Y))"
        quality_rules = []

        for x, y, supp, conf in rules:
            #for level, item in self.levels_itemset:
            x_supp = 0
            y_supp = 0
            if len(x) > 1 or len(y) > 1:
                #TODO: VERIFY IF THIS INNER FOR LOOP IS NEEDED OR NOT AND FINISH IT !!!!
                for level, itemsets in self.levels_itemset.items():
                    for itemset, supp in itemsets.items():
                        if x == itemset:
                            x_supp = self.levels_itemset[level][itemset]
                        if y == itemset:
                            y_supp = self.levels_itemset[level][itemset]
            else:
                x_supp = self.levels_itemset[1][x]
                y_supp = self.levels_itemset[1][y]
            #lift = (supp / self.num_transactions) / ((self.levels_itemset[1][x]/ self.num_transactions) * (self.levels_itemset[1][y] / self.num_transactions))
            lift = (supp/self.num_transactions) / ((x_supp / self.num_transactions) * (y_supp / self.num_transactions))
            if lift > 1:
                rule = (x, y, supp, conf,)
                quality_rules.append(rule)
                print(f'X: {x} Y: {y} CONFIDENCE: {conf}')
                print(f'LIFT: {lift}')
        return quality_rules
    

if __name__ == "__main__":
    fileHandler = FileHandlingTools("data.csv", "mapping.csv")
    transactions = fileHandler.load_transactions()
    calc = FrequentItemsetCalculator1(transactions, 0.3*len(transactions))
    prev_level = calc.count_1_itemsets()
    k = 2
    while prev_level:
        C_k = calc.generate_candidate(k)
        L_k = calc.count_support(C_k)
        prev_level = L_k
        k += 1
    
    rule_generator = RuleGenerator1(calc.levels_itemset, len(transactions))
    rules = rule_generator.generate_rules(0.6)
    rules = rule_generator.quality_prune(rules)
    print(f'RULES: {rules}')
    #print(rules)
