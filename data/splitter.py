import csv
import random

def split_train_valid_test_csv(
    input_file, train_file, valid_file, test_file,
    train_frac=0.34, valid_frac=0.33, test_frac=0.33, random_seed=None
):
    # Read the CSV file with UTF-8 encoding
    with open(input_file, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        rows = list(reader)
    
    data = rows
        
    # Shuffle data
    if random_seed is not None:
        random.seed(random_seed)
    random.shuffle(data)
    
    total = len(data)
    train_end = int(total * train_frac)
    valid_end = train_end + int(total * valid_frac)
    
    train_rows = data[:train_end]
    valid_rows = data[train_end:valid_end]
    test_rows = data[valid_end:]
    
    # Write splits to CSV files with UTF-8 encoding
    for filename, split_rows in [
        (train_file, train_rows),
        (valid_file, valid_rows),
        (test_file, test_rows)
    ]:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for s in split_rows:
                writer.writerow(s)

split_train_valid_test_csv('reference.csv', 'data/train.csv', 'data/valid.csv', 'data/test.csv', random_seed=42)
