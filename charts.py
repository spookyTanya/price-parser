import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def new_product_chart(results):
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


def saved_product_chart(statistics):
    df = pd.DataFrame.from_records(statistics)
    df.set_index('date', inplace=True)
    grouped = df.groupby('website')

    plt.figure(figsize=(12, 6))
    styles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p']

    for (website, data), style, marker in zip(grouped, styles, markers):
        plt.plot(data.index, data['price'], label=website, linestyle=style, marker=marker, alpha=0.7)

    plt.title('Prices for All Websites')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.ylim(ymin=0, ymax=df['price'].max() + 200)
    plt.legend(title='Website')
    plt.grid(True)
    plt.show()

