import pandas as pd
import wbgapi as wb
import re
import openpyxl
import xlrd

iso3_reference_df = pd.read_csv('iso3_country_reference.csv')
africa_iso3 = list(wb.region.members('AFR')

africa_m49 = iso3_reference_df[iso3_reference_df['iso3'].isin(africa_iso3)]['m49'].tolist()

# indicator_to_csv
def process_indicator_to_csv(indicator_code, file_name):
    # Step 1: Extract the data for the indicator and reset the index
    df = wb.data.DataFrame(indicator_code, wb.region.members('AFR'), db=67).reset_index()

    # Step 2: Melt the DataFrame from wide to long format
    df = pd.melt(df, id_vars=['classification', 'economy'], var_name='YearMonth', value_name='Value')

    # Step 3: Rename and clean columns
    df = df.rename(columns={'economy': 'Country'})
    df['Year'] = df['YearMonth'].str[2:6]
    df['Month'] = df['YearMonth'].str[6:]
    df = df.drop(columns=['YearMonth'])  # Drop 'YearMonth' column

    # Step 4: Reorder columns and save to CSV
    df = df[['classification', 'Country', 'Year', 'Month', 'Value']]
    df.to_csv(file_name, index=False)
    print(f"Cleaned data saved to '{file_name}'")

# CSV Indicator 4.1.1.1: DONE!
process_indicator_to_csv('PI-01', 'indicator_4_1_1_1.csv')
# CSV indicator 4.1.1.2: DONE!
process_indicator_to_csv('PI-02', 'indicator_4_1_1_2.csv')
# CSV indicator 4.1.1.3: DONE!
process_indicator_to_csv('PI-03', 'indicator_4_1_1_3.csv')

######################################################################################
# indicator 4.2.1.1: DONE!
def get_4_2_1_1():
    indicator4_2_1_1 = wb.data.DataFrame('GC.TAX.TOTL.GD.ZS', wb.region.members('AFR'))
    return indicator4_2_1_1
indicator_4_2_1_1_df = get_4_2_1_1()
indicator_4_2_1_1_df = indicator_4_2_1_1_df.reset_index()

long_df = pd.melt(indicator_4_2_1_1_df, id_vars=['economy'], var_name='Year', value_name='Value')
long_df['Year'] = long_df['Year'].str.replace('YR', '')
long_df['Indicator'] = 'Tax Revenue as Percentage of GDP'
long_df.to_csv('indicator_4_2_1_1.csv', index=False)

########################################################################################
# indicator 4.2.1.2: DONE!

# Load the Excel file
file_path = 'ATO_RAW_ATAF 2.xlsx' #this is relative path from my 
xls = pd.ExcelFile(file_path, engine='openpyxl')

# Load the first sheet into a DataFrame
df = pd.read_excel(xls, 'Sheet1')

# Initialize lists to store cleaned data
cleaned_data = []

# Temporary storage for theme and topic
current_theme = None
current_topic = None

# Loop through the DataFrame to organize the data based on themes, topics, and indicators
for index, row in df.iterrows():
    first_col_value = row[0]
    
    # Check if the row indicates a new Theme
    if isinstance(first_col_value, str) and first_col_value.startswith('Theme'):
        current_theme = first_col_value.strip()
        current_topic = None  # Reset topic when a new theme starts
    
    # Check if the row indicates a new Topic
    elif pd.notna(first_col_value) and first_col_value != 'Year':
        current_topic = first_col_value.strip()
    
    # If the row indicates 'Year', extract country and year, then collect indicators
    elif first_col_value == 'Year':
        for col_idx in range(1, len(row)):
            if pd.notna(row[col_idx]):
                country_year = row[col_idx]
                if isinstance(country_year, str) and len(country_year.split()) == 2:
                    country, year = country_year.split()
                    
                    # Collect indicators until the next 'Theme' row
                    indicator_idx = index + 1
                    while indicator_idx < len(df) and not (
                        isinstance(df.iloc[indicator_idx, 0], str) and df.iloc[indicator_idx, 0].startswith('Theme')
                    ):
                        indicator_name = df.iloc[indicator_idx, 0]
                        indicator_value = df.iloc[indicator_idx, col_idx]
                        
                        # Add cleaned data to the list if the indicator name is not NaN
                        if pd.notna(indicator_name):
                            cleaned_data.append({
                                'Theme': current_theme,
                                'Topic': current_topic,
                                'Country': country,
                                'Year': year,
                                'Indicator': indicator_name.strip(),
                                'Value': indicator_value
                            })
                        indicator_idx += 1

# Create a cleaned DataFrame from the collected data
cleaned_df = pd.DataFrame(cleaned_data)

# Filter for 'Domestic revenue from large taxpayers' and indicators containing 'Taxpayers'
filtered_df = cleaned_df[(cleaned_df['Indicator'].str.contains('Domestic revenue from large taxpayers', case=False)) |
                         (cleaned_df['Indicator'].str.contains('Taxpayers', case=False))]

# Display the first few rows of the cleaned DataFrame
print(filtered_df .head())
filtered_df .to_csv('indicator_4_2_1_2.csv', index=False)
############################################################################################
# indicator 4.2.2.1 DONE!
# Define the function to get the indicator
def get_4_2_2_1():

    usaid_df = pd.read_excel('USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
    indicator4_2_2_1 = usaid_df[usaid_df['m49'].notna()][['ISO2','country_name', 'year', 'Tax effort (ratio) [tax_eff]']]
    indicator4_2_2_1 = indicator4_2_2_1.rename(columns={'Tax effort (ratio) [tax_eff]': 'Value'})
    indicator4_2_2_1['Indicator'] = 'Tax effort (ratio)'
    return indicator4_2_2_1[['country_name', 'year', 'Indicator', 'Value']]
indicator4_2_2_1 = get_4_2_2_1()
indicator4_2_2_1.to_csv('indicator_4_2_2_1.csv', index=False)
##########################################################################################
# indicator 4.2.2.2 two parts Tax buoyancy [by_tax] + tax cpacity and gap from
#4_2_2_1a
def get_4_2_2_2a():

    usaid_df = pd.read_excel('USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
    indicator4_2_2_2a = usaid_df[usaid_df['m49'].notna()][['ISO2','country_name', 'year', 'Tax buoyancy [by_tax]']]
    indicator4_2_2_2a = indicator4_2_2_1.rename(columns={' Tax buoyancy [by_tax]': 'Value'})
    indicator4_2_2_2a['Indicator'] = 'Tax effort (ratio)'
    return indicator4_2_2_2a[['country_name', 'year', 'Indicator', 'Value']]
indicator4_2_2_2a = get_4_2_2_2a()

indicator4_2_2_1a.to_csv('indicator_4_2_2_1a.csv', index=False)

#4_2_2_1b it has gap cpacity and buoyancy
file_path = 'C:/Users/MYASSIEN/WB_TAX CPACITY AND GAP.csv'
df = pd.read_csv(file_path)
# Define the function to reshape the dataset
def reshape_tax_data(df):
    # Filter for relevant indicators: Buoyancy, Capacity, and Gap
    indicators = ['Buoyancy', 'Capacity', 'Gap']
    reshaped_data = []

    for indicator in indicators:
        # Extract columns that contain the indicator name
        indicator_columns = [col for col in df.columns if indicator in col]
        for col in indicator_columns:
            # Extract the main indicator name and unit if available
            main_indicator = df['indicator name'].iloc[0] if 'indicator name' in df.columns else 'Unknown'
            unit = df['indicator unit'].iloc[0] if 'indicator unit' in df.columns else 'Unknown'
            reshaped_data.append(
                df[['iso3_code', 'Year']]  # Keep common columns
                .assign(Indicator=f"{main_indicator} - {unit} - {indicator}",  # Indicator name with unit and type
                        Value=df[col])  # Indicator value
            )

    reshaped_df = pd.concat(reshaped_data)
    return reshaped_df[['iso3_code', 'Year', 'Indicator', 'Value']]

# Reshape the data
indicator4_2_2_1b = reshape_tax_data(df)

# Save the reshaped DataFrame to a CSV file
indicator4_2_2_1b.to_csv('indicator4_2_2_1b.csv', index=False)

####################################################################################

# indicator 4.3.1.1
def get_4_2_1_1():

    # get market cap and GDP
    market_cap = wb.data.DataFrame('CM.MKT.LCAP.CD', wb.region.members('AFR'))
    gdp = wb.data.DataFrame('NY.GDP.MKTP.CD', wb.region.members('AFR'))

    # calculate indicator
    indicator4_3_1_1 = (market_cap / gdp) * 100

    return indicator4_3_1_1


# indicator 4.3.1.2
def get_4_3_1_2():
    indicator4_3_1_2 = wb.data.DataFrame('DT.NFL.BOND.CD', wb.region.members('AFR'))
    return indicator4_3_1_2


# indicator 4.3.1.3
def get_4_3_1_3():

    # get reserves and debt
    reserves = wb.data.DataFrame('BN.RES.INCL.CD', wb.region.members('AFR'))
    debt = wb.data.DataFrame('DT.DOD.DSTC.CD', wb.region.members('AFR'))

    # calculate indicator
    indicator4_3_1_3 = reserves / debt

    return indicator4_3_1_3


# indicator 4.3.2.1
def get_4_3_2_1():

    # get banking sector indicators
    capital_to_assets = wb.data.DataFrame('FB.BNK.CAPA.ZS', wb.region.members('AFR'))
    liquid_reserves_to_assets = wb.data.DataFrame('FD.RES.LIQU.AS.ZS', wb.region.members('AFR'))
    domestic_credit = wb.data.DataFrame('FS.AST.DOMS.GD.ZS', wb.region.members('AFR')) / 100

    # normalize indicators
    def min_max_normalize(df):
        return (df - df.min()) / (df.max() - df.min())

    # calculate banking sector strength score from indicators
    capital_to_assets = min_max_normalize(capital_to_assets) * 0.4
    liquid_reserves_to_assets = min_max_normalize(liquid_reserves_to_assets) * 0.3
    domestic_credit  = min_max_normalize(domestic_credit) * 0.3
    indicator4_3_2_1 = (capital_to_assets + liquid_reserves_to_assets + domestic_credit)
    
    return indicator4_3_2_1


# indicator 4.3.2.2
def get_4_3_2_2():
    indicator4_3_2_2 = wb.data.DataFrame('FS.AST.DOMS.GD.ZS', wb.region.members('AFR'))
    return indicator4_3_2_2



# TODO: indicator 4.3.3.1
""" FIND SOURCE FOR PENSION / SOVREIGN WEALTH FUNDS - DONT WORRY ABOUT THIS FOR NOW """


# TODO: indicator 4.4.1.1
""" SUM BELOW INDICATORS AS PERCENTAGE OF GDP """



# indicator 4.4.2.1
def get4_4_2_1():
    indicator4_4_2_1 = pd.read_excel('data/gfi trade mispricing.xlsx', skiprows=4, engine='openpyxl', sheet_name='Table A')
    indicator4_4_2_1.columns = ['Index', 'Country', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', 'Average']
    indicator4_4_2_1 = indicator4_4_2_1.drop(columns=['Index'])
    indicator4_4_2_1 = indicator4_4_2_1.dropna(subset=['Country']).replace('N/A', pd.NA)
    indicator4_4_2_1['Country'] = indicator4_4_2_1['Country'].astype(str)
    indicator4_4_2_1['iso3'] = indicator4_4_2_1['Country'].apply(lambda x: wb.economy.coder(x) if pd.notnull(x) else None)

    # TODO: get trade mis-invoicing and calculate indicator 4.4.2.1 - DONT WORRY ABOUT THIS FOR NOW
    
    return indicator4_4_2_1


# indicator 4.4.2.2
def get_4_4_2_2():
    imf_tax_evasion_df = pd.read_excel('data/imf tax evasion.xlsx', engine='openpyxl', sheet_name=None)
    return imf_tax_evasion_df


# indicator 4.4.2.3
def get_4_4_2_3():

    # get druge prices and seizures data
    drug_prices_df = pd.read_excel('data/unodc drug prices.xlsx', skiprows=1, engine='openpyxl', sheet_name='Prices in USD')
    drug_seizures_df = pd.read_excel('data/unodc drug seizures.xlsx', skiprows=1, engine='openpyxl', sheet_name='Export')

    # filter drug prices data and convert units
    filtered_prices_df = drug_prices_df[drug_prices_df['Unit'].isin(['Grams', 'Kilograms'])].copy()
    filtered_prices_df.loc[filtered_prices_df['Unit'] == 'Grams', 'Typical_USD'] *= 1000

    # merge drug prices and seizures
    drug_total_df = pd.merge(
        drug_seizures_df, 
        filtered_prices_df, 
        left_on=['Country', 'DrugName', 'Reference year'], 
        right_on=['Country/Territory', 'Drug', 'Year'], 
        how='inner'
    )

    # calculate total drug sales
    drug_total_df['Total_Sale'] = drug_total_df['Kilograms'] * drug_total_df['Typical_USD']

    indicator4_4_2_3 = drug_total_df.groupby(['Country', 'Reference year'])['Total_Sale'].sum().reset_index()
    indicator4_4_2_3.columns = ['Country', 'Year', 'Total_Sale']
    indicator4_4_2_3['iso3'] = indicator4_4_2_3['Country'].apply(lambda x: wb.economy.coder(x) if pd.notnull(x) else None)

    return indicator4_4_2_3


# indicator 4.4.2.4 
def get_4_4_2_4():
    wb_corruption_score = wb.data.DataFrame('CC.EST', wb.region.members('AFR'), db=3).reset_index().melt(id_vars=['economy'], var_name='Year', value_name='Score')
    wb_corruption_score['Year'] = wb_corruption_score['Year'].str.replace('YR', '')
    wb_corruption_score['normalized_score'] = wb_corruption_score.groupby('Year')['Score'].transform(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )

    wb_corruption_score['weight'] = wb_corruption_score['normalized_score']
    total_weights = wb_corruption_score.groupby('Year')['weight'].sum().reset_index()
    total_weights = total_weights.rename(columns={'weight': 'total_weight'})
    wb_corruption_score = wb_corruption_score.merge(total_weights, on='Year')

    wb_corruption_score['country_share'] = (wb_corruption_score['weight'] / wb_corruption_score['total_weight']) * 148

    wjp_absence_of_corruption = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'Factor 2: Absence of Corruption']]

    """ 
        TODO: add afrobarometer data and calculate indicator 4.4.2.4
        Afrobarometer data is stored as .sav files right now, and I cant figure out how to convert them to csv.
        Theres a command line tool and an online tool but neither have worked for me.
    """

    return


######################################################################################
# indicator 4.4.3.1 has several indicators
def get_4_4_3_1b():
    wjp_rule_of_law = pd.read_excel('C:/Users/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'WJP Rule of Law Index: Overall Score']]
get_4_4_3_1b()
# Function to get and save Rule of Law & Justice indicator - Mo Ibrahim
def get_4_4_3_1c():
   def get_4_4_3_1c():
    rule_of_law_justice = pd.read_csv('mo ibrahim rule of law - score and rank.csv')[['Country', 'Year', 'Rule of Law & Justice (score and rank)']]
get_4_4_3_1c()F
# Function to get and save Reduce Corruption indicator - World Bank CPIA
def get_4_4_3_1d():
    cpia_reduce_corruption = wb.data.DataFrame('IQ.CPA.PUBS.XQ', wb.region.members('AFR'), db=31)
    cpia_reduce_corruption.to_csv('4.4.3.1d_Reduce_Corruption.csv', index=False)
get_4_4_3_1d()
# Function to get and save Sound Institutions indicator - World Bank CPIA
def get_4_4_3_1e():
    cpia_sound_institutions = wb.data.DataFrame('IQ.CPA.TRAN.XQ', wb.region.members('AFR'), db=31)
    cpia_sound_institutions.to_csv('4.4.3.1e_Sound_Institutions.csv', index=False)

# Function to get and save Identity Documentation indicator - World Bank ID4D
def get_4_4_3_1f():
    id4d_identity_documentation = wb.data.DataFrame('SP.REG.BRTH.ZS', wb.region.members('AFR'), db=89)
    id4d_identity_documentation.to_csv('4.4.3.1f_Identity_Documentation.csv', index=False)
get_4_4_3_1f()
# Function to get and save Public Access to Information indicator - World Justice Project
def get_4_4_3_1g():
    public_access_information = pd.read_excel('C:/Users/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'Factor 3: Open Government']]
    public_access_information.to_csv('4.4.3.1g_Public_Access_to_Information.csv', index=False)
get_4_4_3_1g()
# Function to get and save Institutions to Combat Crime indicator - World Justice Project
def get_4_4_3_1h():
    institutions_combat_crime = pd.read_excel('C:/Users/wjp rule of law.xlsxx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'Factor 5: Order and Security', 'Factor 7: Civil Justice', 'Factor 8: Criminal Justice']]
    institutions_combat_crime.to_csv('4.4.3.1h_Institutions_to_Combat_Crime.csv', index=False)
get_4_4_3_1h()
git add etl.py


# indicator 4.4.3.2
def get_4_4_3_2():

    # get all IMF ISORA data
    imf_isora_resources_ict_df = pd.read_excel('data/imf isora resources and ICT infrastructure.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_rstaff_metrics_df = pd.read_excel('data/imf isora staff metrics.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_stakeholder_df = pd.read_excel('data/imf isora stakeholder interactions.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_op_metrics_audit_df = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_op_metrics_payments_df = pd.read_excel('data/imf isora op metrics payments and arrears.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_op_metrics_registration_df = pd.read_excel('data/imf isora op metrics registration and filing.xlsx', engine='openpyxl', sheet_name=None)

    return {
        'imf_isora_resources_ict_df': imf_isora_resources_ict_df,
        'imf_isora_rstaff_metrics_df': imf_isora_rstaff_metrics_df,
        'imf_isora_stakeholder_df': imf_isora_stakeholder_df,
        'imf_isora_op_metrics_audit_df': imf_isora_op_metrics_audit_df,
        'imf_isora_op_metrics_payments_df': imf_isora_op_metrics_payments_df,
        'imf_isora_op_metrics_registration_df': imf_isora_op_metrics_registration_df
    }


# indicator 4.4.4.2
def get_4_4_4_2():

    # get tax justice network data
    df_unilateralCross_url = "https://data.taxjustice.net/api/data/download?dataset=unilateral_cross&keys=country_name%2Ciso3&variables=fsi_2011_value%2Cfsi_2013_value%2Cfsi_2015_value%2Cfsi_2018_value%2Cfsi_2020_value%2Cfsi_2022_value%2Cfsi_2011_gsw%2Cfsi_2013_gsw%2Cfsi_2015_gsw%2Cfsi_2018_gsw%2Cfsi_2020_gsw%2Cfsi_2022_gsw%2Cfsi_2011_rank%2Cfsi_2013_rank%2Cfsi_2015_rank%2Cfsi_2018_rank%2Cfsi_2020_rank%2Cfsi_2022_rank%2Cfsi_2011_score%2Cfsi_2013_score%2Cfsi_2015_score%2Cfsi_2018_score%2Cfsi_2020_score%2Cfsi_2022_score&format=csv&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQ4OTQsInR5cGUiOiJkb3dubG9hZCIsImlhdCI6MTcyNjY5MDE2MSwiZXhwIjoxNzI2NjkxOTYxfQ.Hf8ycDkeciGz6WxNhWXriuFMBL5GZnp52lpeNPFg8Q0"
    df_unilateralCross = pd.read_csv(df_unilateralCross_url)

    # TODO: figure out why Pandas cant parse df

    return df_unilateralCross


# indicator 4.4.5.1 
def get_4_4_5_1():

    # read in data and extract indicators
    usaid_df = pd.read_excel('data/USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
    indicator4_4_5_1 = usaid_df[usaid_df['country_id'].isin(africa_m49)][['country_name', 'year', 'Tax buoyancy [by_tax]']]

    return indicator4_4_5_1


# indicator 4.4.5.2
def get_4_4_5_2():

    # get tax justice network data
    df_unilateralCross_url = "https://data.taxjustice.net/api/data/download?dataset=unilateral_cross&keys=country_name%2Ciso3&variables=fsi_2011_value%2Cfsi_2013_value%2Cfsi_2015_value%2Cfsi_2018_value%2Cfsi_2020_value%2Cfsi_2022_value%2Cfsi_2011_gsw%2Cfsi_2013_gsw%2Cfsi_2015_gsw%2Cfsi_2018_gsw%2Cfsi_2020_gsw%2Cfsi_2022_gsw%2Cfsi_2011_rank%2Cfsi_2013_rank%2Cfsi_2015_rank%2Cfsi_2018_rank%2Cfsi_2020_rank%2Cfsi_2022_rank%2Cfsi_2011_score%2Cfsi_2013_score%2Cfsi_2015_score%2Cfsi_2018_score%2Cfsi_2020_score%2Cfsi_2022_score&format=csv&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQ4OTQsInR5cGUiOiJkb3dubG9hZCIsImlhdCI6MTcyNjY5MDE2MSwiZXhwIjoxNzI2NjkxOTYxfQ.Hf8ycDkeciGz6WxNhWXriuFMBL5GZnp52lpeNPFg8Q0"
    df_unilateralCross = pd.read_csv(df_unilateralCross_url)

    # TODO: figure out why Pandas cant parse df

    return df_unilateralCross


# TODO: indicator 4.4.6.1 
""" NEED TO REGISTER WITH GOLD MINING DATABASE - WE DON'T NEED TO WORRY ABOUT THIS ONE FOR NOW """


if __name__ == '__main__':
    get_4_4_3_2()