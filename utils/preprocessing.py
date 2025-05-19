import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import spacy.cli
from spacy.lang.en.stop_words import STOP_WORDS


try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def fill_missing_numeric_values(df, columns):
    """
    Fill missing numeric values in the DataFrame with the mean of each column.
    """
    for column in columns:
        df[column].fillna(0, inplace=True)
    return df



def fill_missing_categorical_values(df, columns):
    """
    Fill missing categorical values in the DataFrame with the mode of each column.
    """
    for column in columns:
        df[column].fillna('', inplace=True)
    return df


def plot_pivot_table(df, column1, column2):
    
    heatmap_data = df.pivot_table(column1, column2)

    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='coolwarm', cbar=True)
    plt.title('Heatmap of User Ratings')
    plt.xlabel(column2)
    plt.ylabel(column1)
    plt.show()


def clean_and_extract_tags(text):
    doc = nlp(text.lower())
    tags = [token.text for token in doc if token.text.isalnum() and token.text not in STOP_WORDS]
    return ', '.join(tags)


def tags_creation(df, columns):
    for column in columns:
        df[column] = df[column].apply(clean_and_extract_tags)
    return df