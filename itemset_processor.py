from itertools import combinations
from file_handler import FileHandlingTools


class FrequentItemsetCalculator(object):
    def __init__(self, transactions, support_threshold):
        self.transactions: list[frozenset[int]] = transactions
        self.support_threshold = support_threshold
        self.levels_itemset: dict[int: {frozenset: int}] = {}

    def count_1_itemsets(self):
        # TODO: This function counts the support count for 1-itemsets and returns the frequent 1-itemsets
        # return L1
        # generating level 1 itemsets and pruning that are less than support threshold
        result = {}
        # Traverse list of transactions and assign values for 1-itemsets accordingly
        for transaction in self.transactions:
            for item in transaction:
                if frozenset({item}) not in result:
                    result[frozenset({item})] = 1
                else:
                    result[frozenset({item})] += 1

        # pruning the itemsets with support less than support threshold
        result = {k: v for k, v in result.items() if v >=
                  self.support_threshold}
        self.levels_itemset[1] = result
        return result

    def generate_candidate(self, k):
        # TODO generate k-itemset candidates from (k-1)-itemset and prunes candidates based on apriori property and returns the list of candidates.
        self.level = k
        # Itemsets from previous level to generate new candidates
        prev_level = set(self.levels_itemset[self.level-1].keys())
        C_k = set()
        for item1 in prev_level:
            for item2 in prev_level:
                if item1 == item2:
                    continue
                # Creating the possible candidate
                candidate = item1.union(item2)
                cand_subsets = set(  # Generating possible subsets to verify apriori property
                    frozenset(item) for item in combinations(candidate, k-1)
                )
                print(f'PREV LEVEL: {prev_level}')
                print(f'CANDIDATE: {candidate}')
                print(f'CANDIDATE SUBSETS:{cand_subsets}')
                if cand_subsets.issubset(prev_level):
                    C_k.add(candidate)

        return C_k

    def count_support(self, C_k):
        # TODO: This fucntion counts the support for each candidates in C_k and after checking the support threshold, returns the frequent itemsets of level k.
        # Pruning itemsets that have support count less than the support threshold
        L_k = dict()

        # Counting support counts of generated candidates
        for candidate in C_k:
            for transaction in self.transactions:
                if candidate.issubset(transaction):
                    if candidate not in L_k:
                        L_k[candidate] = 1
                    else:
                        L_k[candidate] += 1

        # Pruning candidates if candidate does not meet given support threshold
        L_k = {
            k: v
            for k, v in L_k.items() if v >= self.support_threshold
        }

        # Store the valid itemsets generated from current level if any
        if L_k != {}:
            self.levels_itemset[self.level] = L_k
        return L_k


if __name__ == "__main__":
    fileHandler = FileHandlingTools("data.csv", "mapping.csv")
    test = fileHandler.load_transactions()
    print(f'TRANSACTIONS: {test}')
    calc = FrequentItemsetCalculator(test, 3)
    prev_level = calc.count_1_itemsets()
    k = 2
    while prev_level:
        C_k = calc.generate_candidate(k)
        L_k = calc.count_support(C_k)
        prev_level = L_k
        k += 1
    print(f'LEVELS ITEMSET: {calc.levels_itemset}')
