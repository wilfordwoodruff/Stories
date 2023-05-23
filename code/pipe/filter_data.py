import pandas as pd
from fuzzywuzzy import fuzz

def filter_by_document_type(df, document_type):
    return df[df['Document Type'].str.lower() == document_type.lower()]

def filter_by_keyword(df, keyword, threshold=70):
    def contains_fuzzy(word_list, keyword):
        if isinstance(word_list, str):
            words = word_list.split()
            scores = [fuzz.ratio(word, keyword) for word in words]
            return any(score > threshold for score in scores)
        else:
            return False

    mask = df['Text Only Transcript'].apply(contains_fuzzy, keyword=keyword)
    return df[mask]

def filter_by_topic(df, topic):
    return df[df['Topics'].str.contains(topic, na=False, case=False)]

def filter_by_topic(df, topic):
    # Convert the topic to lower case
    topic = topic.lower()
    
    # Create a mask that is True for each row where the 'Topics' column contains the topic
    mask = df['Topics'].str.lower().str.split('|').apply(lambda topics: topic in topics if isinstance(topics, list) else False)
    
    # Return only the rows of the DataFrame where the mask is True
    return df[mask]

if __name__ == '__main__':
    df = pd.read_csv('data/derived/derived_data.csv')

    df = filter_by_document_type(df, 'Journals')
    df = filter_by_keyword(df, 'truth')
    df = filter_by_topic(df, 'Doctrine and Covenants')
    df = filter_by_date_range(df, '1836-09-10', '1836-09-12')

    print(df)
