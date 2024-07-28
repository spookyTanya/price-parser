import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def process_results(results):
    print(results)
    df = pd.DataFrame.from_records(results)
    print('min price = ', df['price'].min())

    df_melted = df.melt(id_vars=['website', 'is_available'], value_vars=['price', 'old_price'],
                        var_name='Price Type', value_name='Value')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_melted[df_melted['is_available'] == True], x='website', y='Value', hue='Price Type', alpha=1.0)
    sns.barplot(data=df_melted[df_melted['is_available'] == False], x='website', y='Value', hue='Price Type', alpha=0.5)
    plt.xlabel('Website')
    plt.ylabel('Price')
    plt.title('Price and Old Price by Website')
    plt.show()


def process_statistics():
    df = pd.read_csv("test2.csv")
    df.set_index('date', inplace=True)
    # grouped = df.groupby('website')

    # print(grouped)
    df.plot('')
    plt.show()


# process_statistics()