from itertools import combinations

from file_handler import FileHandlingTools
from itemset_processor import FrequentItemsetCalculator


class RuleGenerator(object):

    def __init__(self, levels_itemset, num_transactions):
        self.levels_itemset: dict[tuple, int] = levels_itemset #frequent itemsets with their support counts dict[tuple, int]
        self.num_transactions = num_transactions #int
        self.rules: list[tuple] = list()

    def generate_rules(self, confidence_threshold):
        #TODO: This function generates the association rules from the frequent itemsets and returns the list of rules.
        # rules are of the form (X, Y, support, confidence) which means X => Y [support, confidence]

        for k,v in self.levels_itemset.items():
            if len(k) > 1:
                for i in range(1, len(k)):#TESTTTINGGGGGGG REMOVE !!!!!!1
                    #print(f'ITEMSET: {k}')
                    for comb in combinations(k, i):
                        #print(f'X: {set(comb)}')
                        x = comb
                        # y is the tuple that contains items except in tuple x
                        y = set(k)
                        y = y.symmetric_difference(set(x))
                        #print(f'Y: {y}')
                        support = v
                        confidence = float(v) / (float(self.levels_itemset[x]))
                        #print(f'CONFIDENCE >>>>> {confidence}')
                        if confidence >= confidence_threshold:
                            temp = list(x)
                            temp.append(tuple(y))
                            temp.append(support)
                            temp.append(confidence)
                            print(temp)
                            #self.rules.append((x, y, support, confidence)) 
                            self.rules.append(temp)

        #print(f'RULES GENERATED:')        
        #print(self.rules)
        return self.rules
        #return rules
    
    def quality_prune(self, rules):
        #TODO: This function prunes the misleading rules by using the lift measure and returns the updated list of rules.
        # lift(X => Y) = "confidence(X => Y) / support(Y)" or "P(X and Y) / (P(X) * P(Y))"
        result = []
        print(self.levels_itemset)
        print(rules)
        for x, y, support, confidence in rules:
            print(f'BLAHHH')
            temp = [x]
            print(temp)
            tempy = list(y)
            temp = temp + tempy
            temp = set(temp)
            print(y)
            print(sorted(temp))
            print(tempy)
            #lift = self.levels_itemset[tuple(temp)] / self.levels_itemset[y]
            lift = (self.levels_itemset[tuple(sorted(temp))] / self.num_transactions ) / ((self.levels_itemset[(x,)] / self.num_transactions) * (self.levels_itemset[y] / self.num_transactions))
            #lift = self.levels_itemset[tuple(temp)] / self.levels_itemset[y]
            print(lift)
            print(f'>>>>>BLAHHHHH')
            if lift >= 1.0:
                temp = list(temp)
                temp.append(support)
                temp.append(confidence)
                result.append(list(temp))
                #print(lift)
                print(result)
        print(self.levels_itemset)
        return result
    

if __name__ == "__main__":
    fileHandler = FileHandlingTools("data.csv", "mapping.csv")
    transactions = fileHandler.load_transactions()
    #print(f'TRANSACTIONS:{fileHandler.transactions}')
    calc = FrequentItemsetCalculator(transactions, 3)
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
    print(rules)
