import csv

def get_unique_items(transactions):
    return list(set(item for transaction in transactions for item in transaction))

def generate_groupings(items, index, current_group, all_groupings):
    if index == len(items):
        all_groupings.append(current_group[:])
        return
    generate_groupings(items, index + 1, current_group, all_groupings)
    current_group.append(items[index])
    generate_groupings(items, index + 1, current_group, all_groupings)
    current_group.pop()

def write_groupings_to_csv(output_file, groupings):
    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Grouping'])
        for grouping in groupings:
            csv_writer.writerow([' '.join(grouping)])

def read_transactions_from_csv(input_file):
    with open(input_file, 'r') as file:
        return [row[1:] for row in csv.reader(file)][1:]

def main(input_file, output_file):
    transactions = read_transactions_from_csv(input_file)
    unique_items = get_unique_items(transactions)
    all_groupings = []
    generate_groupings(unique_items, 0, [], all_groupings)
    write_groupings_to_csv(output_file, all_groupings)

main('ip.csv', 'generated_groupings.csv')
