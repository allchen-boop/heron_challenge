# ---------------------------------- HERON DATA DEPLOYMENT ENG CHALLENGE ---------------------------------- #

import json
import pandas as pd
import numpy as np
import datetime as dt
import re
from difflib import SequenceMatcher

def read_transactions(filename):
    with open(filename) as f:
        raw_data = json.load(f)

    return raw_data['transactions'] # list of transactions

def to_df(transactions):
    df = pd.DataFrame(transactions)

    return df


def amt_occurences(df):
    df['occurrences'] = df.duplicated('amount', keep=False)
    df = df.drop(columns=['occurrences'])
    return df


def normalize_desc(df):
    # date in YYYY-MM-DD format
    df['description'] = df['description'].str.replace(r'\d{4}-\d{2}-\d{2}', '', regex=True)
    
    # date in MonthYYYY format
    df['description'] = df['description'].str.replace(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{4}\b', '', regex=True)
    
    # no special characters
    df['description'] = df['description'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
    
    # make all lowercase
    df['description'] = df['description'].str.lower()
    
    return df

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def similarity_matrix(df):
    # list of just the descriptions
    desc_list = df['description'].tolist()

    similarity_matrix = []
    for a in desc_list:
        row = []
        for b in desc_list:
            similarity_score = similarity(a, b)
            row.append(similarity_score)
        similarity_matrix.append(row)
    return similarity_matrix


def similarity_clusters(similarity_matrix):
    clusters = []
    for i, row in enumerate(similarity_matrix):
        cluster_found = False
        for cluster in clusters:
            if any(similarity_matrix[i][j] > 0.6 for j in cluster):
                cluster.append(i)
                cluster_found = True
                break
        if not cluster_found:
            clusters.append([i])

    return [len(sublist) for sublist in clusters]

def date_diff(cluster_sizes, df):
    curr = 0
    diffs = []

    for i in cluster_sizes:
        cluster_dates = df['date'][curr : curr + i]

        for i in range(1, len(cluster_dates)):
            df['delta_date'] = df['date'].diff().abs()
        
        curr += 1
    curr = 0

    for i in cluster_sizes:
        df.iat[curr, df.columns.get_loc('delta_date')] = pd.Timedelta(0)
        curr += i
    return df

def check_dates_within_range(df, start_index, end_index):
    cluster = df.loc[start_index:end_index, 'delta_date']
    min_diff = cluster.min()
    df.loc[start_index:end_index, 'delta'] = cluster.apply(lambda x: x if (x - min_diff) <  pd.Timedelta(5) else pd.Timedelta(0))
    
    return df
    
def recurring_status(df, cluster_sizes):
    curr = 0
    for size in cluster_ranges:
        start_index = curr
        end_index = curr + size - 1
        check_dates_within_range(df, start_index, end_index)
        curr += size
    return df

def identify_recurring_transactions(transactions_list):
    # 1. turn transfactions in df
    transactions_df = to_df (transactions_list)
    
    # 2. calculate occurences of transaction amounts
    possible_recurring = amt_occurences(transactions_df)

    # 3. normalize descriptions
    normalized_desc = normalize_desc(possible_recurring)

    # 4. matrix of all desc similarity scores
    similarity_matrix = similarity_matrix(normalized_desc)

    # 5. get clusters ranges of transactions based on desc similarity
    cluster_ranges = similarity_clusters(similarity_matrix)

    # 6. get the date deltas for each cluster in days
    date_delta_df = date_diff(cluster_ranges, normalized_desc)

    # 7. make sure the deltas are within threshold
    final_df = recurring_status(date_delta_df, cluster_ranges)

    


def main():
    identify_recurring_transactions(read_transactions('tests/example.json'))


if __name__ == "__main__":
    main()
