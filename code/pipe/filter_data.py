import pandas as pd
from fuzzywuzzy import fuzz

def filter_by_document_type(df, document_type):
    return df[df['Document Type'].str.lower() == document_type.lower()]

def filter_by_keyword(df, keyword, threshold=80):
    mask = df['Text Only Transcript'].apply(lambda x: fuzz.ratio(str(x).lower(), keyword.lower()) > threshold if pd.notnull(x) else False)
    return df[mask]

def filter_by_topic(df, topic):
    return df[df['Topics'].str.contains(topic, na=False, case=False)]

def filter_by_date_range(df, start_date, end_date):
    df = df.assign(Dates=df['Dates'].str.split("|")).explode('Dates')
    df['Dates'] = pd.to_datetime(df['Dates'], format='%Y-%m-%d', errors='coerce')
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()
    return df[df['Dates'].dt.date.between(start_date, end_date)]


if __name__ == '__main__':
    df = pd.read_csv('data/derived/derived_data.csv')
    print(df.info())
    filter_by_document_type(df, 'Journals')
    print(filter_by_keyword(df, 'truth'))
    filter_by_topic(df, 'Doctrine and Covenants')
    print(filter_by_date_range(df, '1836-09-10', '1844-04-22'))

    print(df)