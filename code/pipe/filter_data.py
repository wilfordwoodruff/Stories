import pandas as pd
from Levenshtein import ratio

def filter_by_document_type(df, document_type):
    return df[df['Document Type'].str.lower() == document_type.lower()]

def filter_by_keyword(df, keyword, threshold=0.8):
    # Create a mask where each element is True if the keyword is in the corresponding element of the 'Text Only Transcript' column
    mask = df['Text Only Transcript'].apply(lambda x: ratio(str(x).lower(), keyword.lower()) > threshold if pd.notnull(x) else False)
    
    # Return a new dataframe consisting only of the rows where the mask is True
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
