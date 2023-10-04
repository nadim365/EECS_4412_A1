from itertools import combinations
from file_handler import FileHandlingTools


class FrequentItemsetCalculator(object):
    def __init__(self, transactions, support_threshold):
        self.transactions: set[set[int]] = transactions
        self.support_threshold = support_threshold
        self.level1Itemset = dict()
        self.levels_itemset: dict = {}
        self.candidate_itemset = dict()

    def count_1_itemsets(self):
        # TODO: This function counts the support count for 1-itemsets and returns the freque nt 1-itemsets
        # return L1
        #generating level 1 itemsets and pruning that are less than support threshold


        for transaction in self.transactions:
            for item in transaction:
                if item in self.level1Itemset:
                    self.level1Itemset[item] += 1
                else:
                    self.level1Itemset[item] = 1

        self.level1Itemset = {
            frozenset({k}):v
            for k, v in self.level1Itemset.items()
            if v >= self.support_threshold
        }
        #print(f'Level 1 Itemset: {self.level1Itemset}')
        #temp = {(k,):v for k,v in self.level1Itemset.items()}
        #self.levels_itemset.update(temp)
        self.levels_itemset.update(self.level1Itemset)
        return self.level1Itemset

    def generate_candidate(self, k):
        # TODO generate k-itemset candidates from (k-1)-itemset and prunes candidates based on apriori property and returns the list of candidates.
        if k == 2:
            #print("LEVEL 2 ITEMSET")
            c_k = list(combinations(self.level1Itemset, k))
        else:
            #print(f'LEVEL {k} ITEMSET')
            c_k = list(combinations(self.candidate_itemset, 2))
            #c_k = [tuple(set(cand[0] + cand[1])) for cand in c_k if cand[0][:-1] == cand[1][:-1] ]
            c_k = [tuple(set(cand[0] + cand[1])) for cand in c_k if cand[0][:-1] == cand[1][:-1]]
            #print(c_k)

        freq_items = {}
        for candidate in c_k:
            for transaction in self.transactions:
                if frozenset(candidate).issubset(transaction):
                    if frozenset(candidate) in freq_items:
                        #self.candidate_itemset[candidate] += 1
                        freq_items[frozenset(candidate)] += 1
                    else:
                        #self.candidate_itemset[candidate] = 1
                        freq_items[frozenset(candidate)] = 1
        
        self.candidate_itemset = freq_items.copy()
        #print(self.candidate_itemset)
        return self.candidate_itemset
        # return C_k

    def count_support(self, C_k):
        # TODO: This fucntion counts the support for each candidates in C_k and after checking the support threshold, returns the frequent itemsets of level k.
        #Pruning itemsets that have support count less than the support threshold
        #C_k = {
        #    k:v
        #    for k,v in C_k.items()
        #    if v >= self.support_threshold
        #}
        #self.levels_itemset.update(C_k)
        #print(f'Pruned Candidates: {self.levels_itemset}')
        C_k = {
            k:v
            for k,v in C_k.items()
            if v >= self.support_threshold
        }
        if C_k != {}:
            self.levels_itemset.update(C_k)
        
        #print(f'FINAL LEVELS ITEMSET:')
        #temp = {(k,):v for k,v in self.level1Itemset.items()}
        #self.levels_itemset.update(temp)
        #print(self.levels_itemset)
        return C_k
        # return L_k


if __name__ == "__main__":
    fileHandler = FileHandlingTools("data.csv", "mapping.csv")
    test = fileHandler.load_transactions()
    print(test)
    calc = FrequentItemsetCalculator(test, 3)
    prev_level = calc.count_1_itemsets()
    print(f'Level 1 Itemset: {prev_level}')

    #supp = calc.generate_candidate(2)
    #calc.count_support(supp)
    k = 2
    while prev_level:
        C_k = calc.generate_candidate(k)
        L_k = calc.count_support(C_k)
        prev_level = L_k
        k += 1
    print(f'Candidates with support counts:')
    print(C_k)
    print(f'Frequent Itemsets with support counts:')
    print(calc.levels_itemset)
    #print(L_k)
    #cand = calc.generate_candidate(2)
    #result = calc.count_support(cand)