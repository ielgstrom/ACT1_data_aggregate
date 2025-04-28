import pandas as pd

# Llegim les dades
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
df_women = pd.read_csv("dataset/share-of-women-in-parliament.csv")

# Fem el mapping segons la documentació:
idx_to_regime = {0: 'closed autocracies', 1: 'electoral autocracies',
                 2: 'electoral democracies', 3: 'liberal democracies'}

# Canviem el tipus de columna i els noms
df_political_regime['Political regime'] = df_political_regime['Political regime'].map(idx_to_regime)
df_political_regime['Political regime'] = df_political_regime['Political regime'].astype('category')
df_political_regime = df_political_regime.rename(columns={'Entity': 'country', 'Year': 'year'})
df_women = df_women.rename(columns={'Entity': 'country', 'Year': 'year',
                                    'Lower chamber female legislators (aggregate: average)': 'women_in_parlament'})

# Afegim les dades de l'índex de felicitat a un df conjunt
final_df = pd.DataFrame()
for year in range(2015, 2024):  # agafem els limits de les dades del World Happiness Report
    df_name = f"df_happiness_{year}"
    df_year = globals()[df_name]
    df_subset = df_migration[df_migration['year'] == year]
    df = pd.merge(df_subset, df_year, on='country', how='left')
    final_df = pd.concat([final_df, df], ignore_index=True)

# Adjuntem totes les dades
final_df = (pd.merge(final_df, df_political_regime, on=['country', 'year'], how='left'))
final_df = (pd.merge(final_df, df_women, on=['country', 'year', 'Code'], how='left'))

# Eliminem els registres que no tenen prou dades
not_data_countries = final_df[(final_df['happiness_score'].isna())]['country'].unique()
final_df = final_df[final_df['happiness_score'].notna()]

# Construïm el df resultant
final_df.to_csv('final_data.csv')


