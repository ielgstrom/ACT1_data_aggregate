import pandas as pd

df = pd.read_csv('final_data.csv')

#Preparem dades per la visualització 1
df_pivot = df.pivot_table(index='country', columns='year', values='netMigration', aggfunc='mean')

df_pivot.to_csv('vis_1.csv')

#Preparem dades per la visualització 2
df_pivot_2 = df.pivot_table(
    index='year',
    columns='Political regime',
    values='netMigration',
    aggfunc='sum'
)

df_pivot_2 = df_pivot_2.groupby(['year', 'Political regime'])['netMigration'].sum().unstack()

df_pivot_2.to_csv('vis_2.csv')