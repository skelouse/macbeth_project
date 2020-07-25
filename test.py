import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_data():
    url = "http://www.gutenberg.org/cache/epub/2264/pg2264.txt"
    try:
        with open('./mac.txt', 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        macbeth = requests.get(url).text
        with open('./macbeth.txt', 'w', encoding='utf-8') as f:
            f.write('need to remove to the macbeth')
            f.write(str(macbeth))
        data = macbeth
    return data

def read_data(data):
    print(type(macbeth))
    print(len(macbeth))
    print(macbeth[:500])

def get_dict_of_names(macbeth):
    dict_of_names = {}
    #macbeth = macbeth.replace('\n', ' ')
    # Splitting the whole text by two spaces, because in the text
    # there is 2-4 spaces before someone speaks
    for i in macbeth.split('  '):
        try:
            # After a name there is a period, so this finds the name
            name = i[0:i.index('.')]
            
            # Replacing the leading spaces with nothing to clean the name
            # case being 3/4 spaces before rather than 2
            name = name.replace(' ', '')

            # The spoken words by _name_ i.e the text after the period
            spoken = i[i.index('.')+2::]

            # There were a couple outliers that had long names of text
            # This removes that
            if len(name) < 20:
                try:
                    dict_of_names[name]  # checking if the name is in the dictionary yet
                    for word in spoken.split(' '):
                        
                        
                        word = word.replace('\n', ' ')
                        puncs = [',', ':', ';', '!', '.', '?', '(', ')']
                        for i in puncs:
                            word = word.replace(i, '')
                        for i in range(5):
                            word = word.replace('  ', ' ')
                        words = word.split(' ')
                        for word in words:
                            try:
                                dict_of_names[name][word] += 1
                            except KeyError:
                                dict_of_names[name][word] = 1
                except KeyError:
                    # Creates the empty dictionary to the name if line 49 has a key error
                    dict_of_names[name] = {}
        except ValueError:
            pass
    dict_of_names['1'].update(dict_of_names.pop('1ISir,allthisisso'))
    dict_of_names['1Appar'].update(dict_of_names.pop('1'))
    dict_of_names['2Appar'].update(dict_of_names.pop('2'))
    dict_of_names['3Appar'].update(dict_of_names.pop('3'))
    return dict_of_names

def get_df(macbeth):
    macbeth = macbeth.replace('\n', ' ')
    for i in range(5):
        macbeth = macbeth.replace('  ', ' ')
    macbeth_l = macbeth.split(' ')
    macbeth_d = {}
    for word in macbeth_l:
        word = word.lower()
        if word in macbeth_d:
            macbeth_d[word] += 1
        else:
            macbeth_d[word] = 1
    return pd.DataFrame.from_dict(macbeth_d.items())

def plot_top_words(macbeth):
    df = get_df(macbeth)
    df.columns = ['word', 'count']
    df = df.set_index('word')
    df = df.sort_values(by='count')
    df.tail(25).plot(kind='barh')
    plt.show()

def plot_mentions(df):
    mentions = {}
    for name in df.columns:
        try:
            mentions[name] = df.loc[name].sum()
        except KeyError:
            pass
    mentions = sorted(mentions.items(), key=lambda x: x[1])
    mention_df = pd.DataFrame.from_records(mentions)
    mention_df.columns = ['name', 'count']
    mention_df.set_index('name', inplace=True)
    mention_df.plot(kind='barh')
    plt.show()

def clean(df):
    to_drop = (['Seyt', 'Seyw', 'Sold', 'Syw', 'Banquo', 'Porter', 
                'Don', 'OldM', 'Banquowithin', 'Appar', 'Ro'])
    df.drop
    df.drop(to_drop, inplace=True, axis=1)
    df.fillna(0, inplace=True)
    df = df.astype('int32')
    return df

def build_df(macbeth):
    dict_of_names = get_dict_of_names(macbeth)
    df = clean(pd.DataFrame.from_dict(dict_of_names))
    return df

#read_data(macbeth)
#plot_mentions(df)
if __name__ == "__main__":
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df = build_df(get_data())
    
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.8, wspace=0.8)
    for n, col in enumerate(df.columns):
        ax = fig.add_subplot(6, 7, (n+1))
        df[col].sort_values(ascending=False)[:5].plot(kind='barh', ax=ax)
        ax.set_title(col)
    plt.show()
    
    
    
    
    
    
    
    
    

    


