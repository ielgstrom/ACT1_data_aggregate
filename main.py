import pandas as pd

df_migration = pd.read_csv('dataset/world_pop_mig_186_countries.csv')
df_happiness_2015 = pd.read_csv('dataset/WHR_2015.csv')
df_happiness_2016 = pd.read_csv('dataset/WHR_2016.csv')
df_happiness_2017 = pd.read_csv('dataset/WHR_2017.csv')
df_happiness_2018 = pd.read_csv('dataset/WHR_2018.csv')
df_happiness_2019 = pd.read_csv('dataset/WHR_2019.csv')
df_happiness_2020 = pd.read_csv('dataset/WHR_2020.csv')
df_happiness_2021 = pd.read_csv('dataset/WHR_2021.csv')
df_happiness_2022 = pd.read_csv('dataset/WHR_2022.csv')
df_happiness_2023 = pd.read_csv('dataset/WHR_2023.csv')
df_political_regime = pd.read_csv('dataset/political-regime.csv')

# Suppose this is your mapping:
idx_to_regime = {0: 'closed autocracies', 1: 'electoral autocracies',
                 2: 'electoral democracies', 3: 'liberal democracies'}

# Canviem el tipus de columna
df_political_regime['Political regime'] = df_political_regime['Political regime'].map(idx_to_regime)
df_political_regime['Political regime'] = df_political_regime['Political regime'].astype('category')
df_political_regime = df_political_regime.rename(columns={'Entity': 'country', 'Year': 'year'})

final_df = pd.DataFrame()
for year in range(2015, 2024):
    df_name = f"df_happiness_{year}"
    df_year = globals()[df_name]
    df_subset = df_migration[df_migration['year'] == year]
    df = pd.merge(df_subset, df_year, on='country', how='left')
    final_df = pd.concat([final_df, df], ignore_index=True)

final_df = (pd.merge(final_df, df_political_regime, on=['country', 'year'], how='left'))

not_data_countries = final_df[(final_df['happiness_score'].isna())]['country'].unique()

final_df = final_df[final_df['happiness_score'].notna()]
final_df.to_csv('final_data.csv')

print(final_df)
