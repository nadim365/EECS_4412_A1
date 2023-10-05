import csv


class FileHandlingTools(object):
    def __init__(self, path_to_transactions_file, path_to_name_mapping_file):
        self.path_to_transactions_file: str = path_to_transactions_file
        self.path_to_name_mapping_file: str = path_to_name_mapping_file
        self.mapping: dict[int, str] = dict()
        self.transactions: list[frozenset[int]] = list()

    def load_transactions(self):
        with open(self.path_to_name_mapping_file) as mappings:
            mappingFile = csv.reader(mappings)
            for mapping in mappingFile:
                self.mapping[frozenset({int(mapping[0])})] = mapping[1]

        mappings.close()

        with open(self.path_to_transactions_file) as transactions:
            transactionFile = csv.reader(transactions)

            for transaction in transactionFile:
                transaction = [int(x) for x in transaction]
                self.transactions.append(frozenset(transaction))
            
        transactions.close()
        
        # TODO: This fucntion reads the transactions from the csv file and returns a list of transactions
        return self.transactions

    def id_to_name(self, id):
        # TODO: This function returns the name of the item given its id which is read from the mapping file.
        return self.mapping[frozenset({id})]

if __name__ == "__main__":
    test = FileHandlingTools("data.csv", "mapping.csv")
    print(test.load_transactions())
