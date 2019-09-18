import numpy as np
import pandas as pd


def subdataframe(dataset: pd.DataFrame, attribute: str, value = None):
    if value is None:
        return [subdataframe(dataset,attribute=attribute,value=value) for value in dataset[attribute].unique()]
    return dataset[dataset[attribute] == value].drop(attribute,axis=1)


def subdataframe_with_repeated(dataset: pd.DataFrame, size: int):
    return pd.DataFrame([dataset.iloc[i] for i in np.random.randint(len(dataset), size=size)]).reset_index(drop=True)


def divide_in_training_test_datasets(dataset: pd.DataFrame, train_pctg: float = 0.5):
    indexes = np.arange(len(dataset))
    indexes = list(np.random.shuffle(indexes))
    split_index = np.floor(len(dataset) * train_pctg)
    train = pd.DataFrame([dataset.iloc[i] for i in indexes[split_index:]])
    test = pd.DataFrame([dataset.iloc[i] for i in indexes[split_index:]])
    return train, test

if __name__ == '__main__':
    # Create a DataFrame
    df1 = {
        'State': ['Arizona AZ', 'Georgia GG', 'Newyork NY', 'Indiana IN', 'Florida FL']*55,
        'Score': [62, 47, 55, 74, 31]*55}

    df1 = pd.DataFrame(df1, columns=['State', 'Score'])
    divide_in_training_test_datasets(df1)