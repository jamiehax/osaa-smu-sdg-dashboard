import pandas as pd
import wbgapi as wb
import re


# iso3 country code reference 
iso3_reference_df = pd.read_csv('iso3_country_reference.csv')

# list of african countries iso3 and m49 codes
africa_iso3 = list(wb.region.members('AFR'))
africa_m49 = iso3_reference_df[iso3_reference_df['iso3'].isin(africa_iso3)]['m49'].tolist()


# indicator 4.1.1.1
def get_4_1_1_1():
    indicator4_1_1_1 = wb.data.DataFrame('PI-01', wb.region.members('AFR'), db=67)
    return indicator4_1_1_1


# indicator 4.1.1.2
def get_4_1_1_2():
    indicator4_1_1_2 = wb.data.DataFrame('PI-02', wb.region.members('AFR'), db=67)
    return indicator4_1_1_2


# indicator 4.1.1.3
def get_4_1_1_3():
    indicator4_1_1_3 = wb.data.DataFrame('PI-03', wb.region.members('AFR'), db=67)
    return indicator4_1_1_3


# indicator 4.2.1.1
def get_4_2_1_1():
    indicator4_2_1_1 = wb.data.DataFrame('GC.TAX.TOTL.GD.ZS', wb.region.members('AFR'))
    return indicator4_2_1_1


# indicator 4.2.1.2
def get_4_2_1_2():

    # read in data
    ataf_df = pd.read_excel('data/ataf_data.xlsx', sheet_name='Sheet1', engine='openpyxl')

    # split country and year using regex
    def extract_country_year(val):
        match = re.match(r"(.*)\s(\d{4})", str(val))
        if match:
            country = match.group(1)
            year = match.group(2)
            return country, year
        return [None, None]
    
    # convert blank cells or '/' to NaN
    def clean_values(val):
        if val == "/" or pd.isnull(val):
            return pd.NA
        return val

    # extract country-year combinations from row 3 (columns B onwards)
    country_year_row = ataf_df.iloc[2, 1:]
    countries_years = country_year_row.apply(extract_country_year)
    country_years_df = pd.DataFrame(countries_years.tolist(), columns=["Country", "Year"])

    # rows that contain indicators
    indicator_rows = [
        3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 
        40, 41, 42, 43, 44, 45, 46, 47, 
        51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
        65, 66, 67, 68, 
        71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 
        83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 
        95, 96, 97, 98, 99, 100
    ]


    # extract indicators names and values
    indicator_data = {}
    for row in indicator_rows:
        indicator_name = ataf_df.iloc[row, 0]  # indicator name is in column A
        indicator_values = ataf_df.iloc[row, 1:].apply(clean_values).reset_index(drop=True)  # values are in columns B onwards
        indicator_data[indicator_name] = indicator_values

    # combine the country-year dataframe with the indicator data
    result_df = pd.concat([country_years_df.reset_index(drop=True), pd.DataFrame(indicator_data)], axis=1)

    return result_df


# indicator 4.2.2.1
def get_4_2_2_1():

    # read in data
    usaid_df = pd.read_excel('data/USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')

    # extract indicator column
    indicator4_2_2_1 = usaid_df[usaid_df['country_id'].isin(africa_m49)][['country_name', 'year', 'Tax effort (ratio) [tax_eff]']]

    return indicator4_2_2_1


# indicator 4.2.2.2
def get_4_2_2_2():

    # read in data
    ataf_df = pd.read_excel('data/ataf_data.xlsx', sheet_name='Sheet1', engine='openpyxl')

    # function to split country and year from name
    def extract_country_year(val):
        match = re.match(r"(.*)\s(\d{4})", str(val))
        if match:
            country = match.group(1)
            year = match.group(2)
            return country, year
        return [None, None]
    
    # convert blank cells or '/' to NaN
    def clean_values(val):
        if val == "/" or pd.isnull(val):
            return pd.NA
        return val

    # extract country-year name and split
    country_year_row = ataf_df.iloc[2, 1:]
    countries_years = country_year_row.apply(extract_country_year)
    country_years_df = pd.DataFrame(countries_years.tolist(), columns=["Country", "Year"])

    # rows with indicators
    indicator_rows = [
        3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 
        40, 41, 42, 43, 44, 45, 46, 47, 
        51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
        65, 66, 67, 68, 
        71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 
        83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 
        95, 96, 97, 98, 99, 100
    ]


    # extract indicators names and values
    indicator_data = {}
    for row in indicator_rows:
        indicator_name = ataf_df.iloc[row, 0]  # indicator name in column A
        indicator_values = ataf_df.iloc[row, 1:].apply(clean_values).reset_index(drop=True)  # values from columns B onwards
        indicator_data[indicator_name] = indicator_values

    # combine the country-year dataframe with the indicator data
    result_df = pd.concat([country_years_df.reset_index(drop=True), pd.DataFrame(indicator_data)], axis=1)

    return result_df


# indicator 4.3.1.1
def get_4_3_1_1():

    # get market cap and GDP
    market_cap = wb.data.DataFrame('CM.MKT.LCAP.CD', wb.region.members('AFR'))
    gdp = wb.data.DataFrame('NY.GDP.MKTP.CD', wb.region.members('AFR'))

    # calculate indicator
    indicator4_3_1_1 = (market_cap / gdp) * 100
    indicator4_3_1_1 = indicator4_3_1_1.reset_index()

    # make long format
    indicator4_3_1_1_long = pd.melt(indicator4_3_1_1, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_1_1_long['year'] = indicator4_3_1_1_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_1_1_long['indicator description'] = 'Market capitalization of listed domestic companies (current US$) divided by GDP (current US$)'
    indicator4_3_1_1_long['indicator code'] = 'CM.MKT.LCAP.CD / NY.GDP.MKTP.CD'

    # Rename 'economy' column to 'iso3'
    indicator4_3_1_1_long = indicator4_3_1_1_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_1_1_long = indicator4_3_1_1_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]

    return indicator4_3_1_1_long


# indicator 4.3.1.2
def get_4_3_1_2():
    indicator4_3_1_2 = wb.data.DataFrame('DT.NFL.BOND.CD', wb.region.members('AFR')).reset_index()

    # make long format
    indicator4_3_1_2_long = pd.melt(indicator4_3_1_2, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_1_2_long['year'] = indicator4_3_1_2_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_1_2_long['indicator description'] = 'Portfolio investment, bonds (PPG + PNG) (NFL, current US$)'
    indicator4_3_1_2_long['indicator code'] = 'DT.NFL.BOND.CD'

    # Rename 'economy' column to 'iso3'
    indicator4_3_1_2_long = indicator4_3_1_2_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_1_2_long = indicator4_3_1_2_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]

    return indicator4_3_1_2_long


# indicator 4.3.1.3
def get_4_3_1_3():

    # get reserves and debt
    reserves = wb.data.DataFrame('BN.RES.INCL.CD', wb.region.members('AFR'))
    debt = wb.data.DataFrame('DT.DOD.DSTC.CD', wb.region.members('AFR'))

    # calculate indicator
    indicator4_3_1_3 = reserves / debt
    indicator4_3_1_3 = indicator4_3_1_3.reset_index()

    # make long format
    indicator4_3_1_3_long = pd.melt(indicator4_3_1_3, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_1_3_long['year'] = indicator4_3_1_3_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_1_3_long['indicator description'] = 'Reserves and related items (BoP, current US$) divided by External debt stocks, short-term (DOD, current US$)'
    indicator4_3_1_3_long['indicator code'] = 'BN.RES.INCL.CD / DT.DOD.DSTC.CD'

    # Rename 'economy' column to 'iso3'
    indicator4_3_1_3_long = indicator4_3_1_3_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_1_3_long = indicator4_3_1_3_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]

    return indicator4_3_1_3_long


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
    indicator4_3_2_1 = indicator4_3_2_1.reset_index()

    # make long format
    indicator4_3_2_1_long = pd.melt(indicator4_3_2_1, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_2_1_long['year'] = indicator4_3_2_1_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_2_1_long['indicator description'] = '(0.4 * Bank capital to assets ratio (%)) + (0.3 * Bank liquid reserves to bank assets ratio (%)) + (0.3 * Domestic credit provided by financial sector (% of GDP))'
    indicator4_3_2_1_long['indicator code'] = '(0.4 * FB.BNK.CAPA.ZS) + (0.3 * FD.RES.LIQU.AS.ZS) + (0.3 * FS.AST.DOMS.GD.ZS)'

    # Rename 'economy' column to 'iso3'
    indicator4_3_2_1_long = indicator4_3_2_1_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_2_1_long = indicator4_3_2_1_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]
    
    return indicator4_3_2_1_long


# indicator 4.3.2.2
def get_4_3_2_2():
    indicator4_3_2_2 = wb.data.DataFrame('FS.AST.DOMS.GD.ZS', wb.region.members('AFR')).reset_index()

    # make long format
    indicator4_3_2_2_long = pd.melt(indicator4_3_2_2, id_vars=['economy'], var_name='year', value_name='value')

    # extract year value
    indicator4_3_2_2_long['year'] = indicator4_3_2_2_long['year'].str.extract(r'(\d{4})')

    # add indicator code and description
    indicator4_3_2_2_long['indicator description'] = 'Domestic credit provided by financial sector (% of GDP)'
    indicator4_3_2_2_long['indicator code'] = 'FS.AST.DOMS.GD.ZS'

    # Rename 'economy' column to 'iso3'
    indicator4_3_2_2_long = indicator4_3_2_2_long.rename(columns={'economy': 'iso3'})

    # reorder columns
    indicator4_3_2_2_long = indicator4_3_2_2_long[['iso3', 'year', 'indicator description', 'indicator code', 'value']]

    return indicator4_3_2_2_long



# TODO: indicator 4.3.3.1
""" FIND SOURCE FOR PENSION / SOVREIGN WEALTH FUNDS - DONT WORRY ABOUT THIS FOR NOW """


# TODO: indicator 4.4.1.1
""" SUM BELOW INDICATORS AS PERCENTAGE OF GDP """



# indicator 4.4.2.1
def get_4_4_2_1():

    # indicator4_4_2_1 = pd.read_excel('data/gfi trade mispricing.xlsx', skiprows=4, engine='openpyxl', sheet_name='Table A')


    # indicator4_4_2_1.columns = ['Index', 'Country', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', 'Average']
    # indicator4_4_2_1 = indicator4_4_2_1.drop(columns=['Index'])
    # indicator4_4_2_1 = indicator4_4_2_1.dropna(subset=['Country']).replace('N/A', pd.NA)
    # indicator4_4_2_1['Country'] = indicator4_4_2_1['Country'].astype(str)
    # indicator4_4_2_1['iso3'] = indicator4_4_2_1['Country'].apply(lambda x: wb.economy.coder(x) if pd.notnull(x) else None)

    # TODO: get trade mis-invoicing and calculate indicator 4.4.2.1 - DONT WORRY ABOUT THIS FOR NOW

    def add_indicator_cols(df, code, description):
        df['indicator_code'] = code
        df['indicator_description'] = description
        return df

    gfi_table_a = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name='Table A').drop(columns='Unnamed: 0')
    gfi_table_a_long = pd.melt(gfi_table_a, id_vars=['Unnamed: 1'], var_name='year', value_name='value').rename(columns={"Unnamed: 1": 'country'})
    gfi_table_a_long = add_indicator_cols(gfi_table_a_long, "Table A", "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries  and 36 Advanced Economies, 2009-2018, in USD Millions")

    gfi_table_c = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name='Table C').drop(columns='Unnamed: 0')
    gfi_table_c_long = pd.melt(gfi_table_c, id_vars=['Unnamed: 1'], var_name='year', value_name='value').rename(columns={"Unnamed: 1": 'country'})
    gfi_table_c_long = add_indicator_cols(gfi_table_c_long, "Table C", "  The Total Value Gaps Identified Between 134 Developing Countries and 36 Advanced Economies, 2009-2018, as a Percent of Total Trade")
                                      
    gfi_table_e = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name='Table E').drop(columns='Unnamed: 0')
    gfi_table_e_long = pd.melt(gfi_table_e, id_vars=['Unnamed: 1'], var_name='year', value_name='value').rename(columns={"Unnamed: 1": 'country'})
    gfi_table_e_long = add_indicator_cols(gfi_table_e_long, "Table E", "  The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries  and all of their Global Trading Partners, 2009-2018 in USD Millions")
                                          
    gfi_table_g = pd.read_excel('data/gfi trade mispricing.xlsx', engine='openpyxl', skiprows=4, sheet_name='Table G').drop(columns='Unnamed: 0')
    gfi_table_g_long = pd.melt(gfi_table_g, id_vars=['Unnamed: 1'], var_name='year', value_name='value').rename(columns={"Unnamed: 1": 'country'})
    gfi_table_g_long = add_indicator_cols(gfi_table_g_long, "Table G", "  The Total Value Gaps Identified in Trade Between 134 Developing Countries and all of their Trading Partners, 2009-2018 as a Percent of Total Trade")
                                          
    indicator4_4_2_1 = pd.concat([gfi_table_a_long, gfi_table_c_long, gfi_table_e_long, gfi_table_g_long])
    
    return indicator4_4_2_1


# indicator 4.4.2.2
def get_4_4_2_2():
    imf_isora_df_1 = pd.read_excel('data/IMF ISORA.xlsx', engine='openpyxl', skiprows=5, skipfooter=3, sheet_name="Registration of personal income").rename(columns={"Unnamed: 0": 'country'})
    imf_isora_df_1_long = pd.melt(imf_isora_df_1, id_vars='country', var_name='year', value_name='value')
    imf_isora_df_1_long['indicator code'] = imf_isora_df_1_long['year'].apply(
        lambda x: 'PIT_Population' if '.1' in x else 'PIT_Labor_Force'
    )

    imf_isora_df_1_long['indicator description'] = imf_isora_df_1_long['indicator code'].map({
        'PIT_Labor_Force': 'Active taxpayers on PIT register as percentage of Labor Force',
        'PIT_Population': 'Active taxpayers on PIT register as percentage of Population'
    })

    imf_isora_df_1_long['year'] = imf_isora_df_1_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_df_2 = pd.read_excel('data/IMF ISORA.xlsx', engine='openpyxl', skiprows=5, skipfooter=3, sheet_name="Percentage inactive taxpayers o").rename(columns={"Unnamed: 0": 'country'})
    imf_isora_df_2_long = pd.melt(imf_isora_df_2, id_vars='country', var_name='year', value_name='value')
    imf_isora_df_2_long['indicator code'] = imf_isora_df_2_long['year'].apply(
        lambda x: (
            'On CIT register' if '.1' in x else
            'On VAT register' if '.2' in x else
            'On PAYE register' if '.3' in x else
            'On Excise register' if '.4' in x else
            'On PIT register'
        )
    )

    imf_isora_df_2_long['indicator description'] = imf_isora_df_2_long['indicator code'].map({
        'On CIT register': 'On CIT register',
        'On VAT register': 'On VAT register',
        'On PAYE register': 'On PAYE register',
        'On Excise register': 'On Excise register',
        'On PIT register': 'On PIT register'
    })
    imf_isora_df_2_long['year'] = imf_isora_df_2_long['year'].str.replace(r'\.\d+', '', regex=True)
    
    indicator4_4_2_2 = pd.concat([imf_isora_df_1_long, imf_isora_df_2_long])

    return indicator4_4_2_2


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
    indicator4_4_2_3.columns = ['Country', 'year', 'Total_Sale']
    indicator4_4_2_3['iso3'] = indicator4_4_2_3['Country'].apply(lambda x: wb.economy.coder(x) if pd.notnull(x) else None)

    indicator4_4_2_3 = indicator4_4_2_3.drop(columns='Country').rename(columns={'Total_Sale': 'value'})
    indicator4_4_2_3['indicator description'] = 'The amount of drugs seized in kilograms multiplied by the drug price in kilograms. Exlcludes all siezures not measured in grams or kilograms.'
    indicator4_4_2_3['indicatore code'] = 'Monetary losses (in USD) to drug sales'

    return indicator4_4_2_3


# indicator 4.4.2.4 
def get_4_4_2_4():
    wb_corruption_score = wb.data.DataFrame('CC.EST', wb.region.members('AFR'), db=3).reset_index().melt(id_vars=['economy'], var_name='year', value_name='wb corruption score').rename(columns={'economy': 'iso3'})
    wb_corruption_score['year'] = wb_corruption_score['year'].str.replace('YR', '')
    wb_corruption_score['wb normalized corruption score'] = wb_corruption_score.groupby('year')['wb corruption score'].transform(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )

    wb_corruption_score['wb corruption score weight'] = wb_corruption_score['wb normalized corruption score']
    total_weights = wb_corruption_score.groupby('year')['wb corruption score weight'].sum().reset_index()
    total_weights = total_weights.rename(columns={'wb corruption score weight': 'wb corruption score total weight'})
    wb_corruption_score = wb_corruption_score.merge(total_weights, on='year')

    wb_corruption_score['wb corruption score country share'] = (wb_corruption_score['wb corruption score weight'] / wb_corruption_score['wb corruption score total weight']) * 148

    wjp_absence_of_corruption = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country Code', 'Year', 'Factor 2: Absence of Corruption']].rename(columns={'Country Code': 'iso3', 'Year': 'year'})
    wjp_absence_of_corruption['year'] = wjp_absence_of_corruption['year'].astype(str)

    def expand_years(row):
        if '-' in row['year']:
            start, end = map(int, row['year'].split('-'))
            return [{'iso3': row['iso3'], 'year': year, 'Factor 2: Absence of Corruption': row['Factor 2: Absence of Corruption']}
                    for year in range(start, end + 1)]
        else:
            return [row]
        
    wjp_absence_of_corruption_expanded = pd.DataFrame([entry for row in wjp_absence_of_corruption.to_dict(orient='records') for entry in expand_years(row)])

    """ 
        TODO: add afrobarometer data and calculate indicator 4.4.2.4
        Afrobarometer data is stored as .sav files right now, and I cant figure out how to convert them to csv.
        Theres a command line tool and an online tool but neither have worked for me.
    """

    indicator4_4_2_4 = pd.merge(wb_corruption_score, wjp_absence_of_corruption_expanded, on=['iso3', 'year'], how='left')
    indicator4_4_2_4 = pd.melt(indicator4_4_2_4, id_vars=['iso3', 'year'], var_name='indicator description', value_name='value')

    return indicator4_4_2_4



# indicator 4.4.3.1
def get_4_4_3_1():

    # get wjp indicators
    wjp_rule_of_law = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'WJP Rule of Law Index: Overall Score']]
    wjp_open_government = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'Factor 3: Open Government']]
    wjp_combat_crime = pd.read_excel('data/wjp rule of law.xlsx', engine='openpyxl', sheet_name='Historical Data')[['Country', 'Year', 'Factor 5: Order and Security', 'Factor 7: Civil Justice', 'Factor 8: Criminal Justice']]

    # get CPIA indicators
    cpia_public_sector_management = wb.data.DataFrame('IQ.CPA.PUBS.XQ', wb.region.members('AFR'), db=31)
    cpia_public_sector_management = wb.data.DataFrame('IQ.CPA.TRAN.XQ', wb.region.members('AFR'), db=31)

    # get ID4D indicators
    id4d_birth_registration = wb.data.DataFrame('SP.REG.BRTH.ZS', wb.region.members('AFR'), db=89)
    id4d_birth_certification = wb.data.DataFrame('ID.OWN.BRTH.ZS', wb.region.members('AFR'), db=89)
    id4d_id_ownership = wb.data.DataFrame('ID.OWN.TOTL.ZS', wb.region.members('AFR'), db=89)

    # return all together
    return pd.concat([wjp_rule_of_law, wjp_open_government, wjp_combat_crime, cpia_public_sector_management, cpia_public_sector_management, id4d_birth_registration, id4d_birth_certification, id4d_id_ownership])


# indicator 4.4.3.2
def get_4_4_3_2():

    # get all IMF ISORA data
    # imf_isora_stakeholder_df = pd.read_excel('data/imf isora stakeholder interactions.xlsx', engine='openpyxl', sheet_name=None)
    # imf_isora_op_metrics_payments_df = pd.read_excel('data/imf isora op metrics payments and arrears.xlsx', engine='openpyxl', sheet_name=None)
    # imf_isora_op_metrics_registration_df = pd.read_excel('data/imf isora op metrics registration and filing.xlsx', engine='openpyxl', sheet_name=None)

    imf_isora_resources_ict_df_1 = pd.read_excel('data/imf isora resources and ICT infrastructure.xlsx', skiprows=6, engine='openpyxl', sheet_name='Tax administration expenditures').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_resources_ict_df_1_long = pd.melt(imf_isora_resources_ict_df_1, id_vars='country', var_name='year', value_name='value')
    imf_isora_resources_ict_df_1_long['indicator code'] = imf_isora_resources_ict_df_1_long['year'].apply(
        lambda x: (
            'Salary expenditure - Derived' if '.1' in x else
            'Information and communications technology expenditure - Derived' if '.2' in x else
            'Capital expenditure - Derived' if '.3' in x else
            'Operating expenditure - Derived'
        )
    )
    imf_isora_resources_ict_df_1_long['indicator description'] = imf_isora_resources_ict_df_1_long['indicator code'].map({
        'Salary expenditure - Derived': 'Salary expenditure - Derived',
        'Information and communications technology expenditure - Derived': 'Information and communications technology expenditure - Derived',
        'Capital expenditure - Derived': 'Capital expenditure - Derived',
        'Operating expenditure - Derived': 'Operating expenditure - Derived',
    })
    imf_isora_resources_ict_df_1_long['year'] = imf_isora_resources_ict_df_1_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_resources_ict_df_2 = pd.read_excel('data/imf isora resources and ICT infrastructure.xlsx', skiprows=7, engine='openpyxl', sheet_name='Tax administration staff total ').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_resources_ict_df_2_long = pd.melt(imf_isora_resources_ict_df_2, id_vars='country', var_name='year', value_name='value')
    imf_isora_resources_ict_df_2_long['indicator code'] = imf_isora_resources_ict_df_2_long['year'].apply(
        lambda x: (
            'FTEs by function of the tax administration-Registration, taxpayer services, returns and payment processing' if '.1' in x else
            'FTEs by function of the tax administration-Audit, investigation and other verification' if '.2' in x else
            'FTEs by function of the tax administration-Enforced debt collection and related functions' if '.3' in x else
            'FTEs by function of the tax administration-Other functions' if '.4' in x else
            'Percentage of staff working on headquarter functions' if '.5' in x else
            'Total tax administration FTEs - Derived'
        )
    )
    imf_isora_resources_ict_df_2_long['indicator description'] = imf_isora_resources_ict_df_2_long['indicator code'].map({
        'FTEs by function of the tax administration-Registration, taxpayer services, returns and payment processing': 'FTEs by function of the tax administration-Registration, taxpayer services, returns and payment processing',
        'FTEs by function of the tax administration-Audit, investigation and other verification': 'FTEs by function of the tax administration-Audit, investigation and other verification',
        'FTEs by function of the tax administration-Enforced debt collection and related functions': 'FTEs by function of the tax administration-Enforced debt collection and related functions',
        'FTEs by function of the tax administration-Other functions': 'FTEs by function of the tax administration-Other functions',
        'Percentage of staff working on headquarter functions': 'Percentage of staff working on headquarter functions',
        'Total tax administration FTEs - Derived': 'Total tax administration FTEs - Derived'
    })
    imf_isora_resources_ict_df_2_long['year'] = imf_isora_resources_ict_df_2_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_resources_ict_df_3 = pd.read_excel('data/imf isora resources and ICT infrastructure.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Operational ICT solutions').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_resources_ict_df_3_long = pd.melt(imf_isora_resources_ict_df_3, id_vars='country', var_name='year', value_name='value')
    imf_isora_resources_ict_df_3_long['indicator code'] = imf_isora_resources_ict_df_3_long['year'].apply(
        lambda x: (
            'Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)' if '.1' in x else
            'Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)' if '.2' in x else
            'Operational ICT solutions of the administration are…-Custom built'
        )
    )
    imf_isora_resources_ict_df_3_long['indicator description'] = imf_isora_resources_ict_df_3_long['indicator code'].map({
        'Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)': 'Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)',
        'Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)': 'Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)',
        'Operational ICT solutions of the administration are…-Custom built': 'Operational ICT solutions of the administration are…-Custom built'
    })
    imf_isora_resources_ict_df_3_long['year'] = imf_isora_resources_ict_df_3_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_resources_ict_df = pd.concat([imf_isora_resources_ict_df_1_long, imf_isora_resources_ict_df_2_long, imf_isora_resources_ict_df_3_long])


    imf_isora_staff_metrics_df_1 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=6, skipfooter=2, engine='openpyxl', sheet_name='Staff strength levels').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_1_long = pd.melt(imf_isora_staff_metrics_df_1, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_1_long['indicator code'] = imf_isora_staff_metrics_df_1_long['year'].apply(
        lambda x: (
            'Staff strength levels -Departures in FY' if '.1' in x else
            'Staff strength levels -Recruitments in FY' if '.2' in x else
            'Staff strength levels -No. at end of FY' if '.3' in x else
            'Staff strength levels -No. at start of FY'
        )
    )
    imf_isora_staff_metrics_df_1_long['indicator description'] = imf_isora_staff_metrics_df_1_long['indicator code'].map({
        'Staff strength levels -Departures in FY': 'Staff strength levels -Departures in FY',
        'Staff strength levels -Recruitments in FY': 'Staff strength levels -Recruitments in FY',
        'Staff strength levels -No. at end of FY': 'Staff strength levels -No. at end of FY',
        'Staff strength levels -No. at start of FY': 'Staff strength levels -No. at start of FY',
    })
    imf_isora_staff_metrics_df_1_long['year'] = imf_isora_staff_metrics_df_1_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_staff_metrics_df_2 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=6, skipfooter=2, engine='openpyxl', sheet_name='Staff academic qualifications').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_2_long = pd.melt(imf_isora_staff_metrics_df_2, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_2_long['indicator code'] = imf_isora_staff_metrics_df_2_long['year'].apply(
        lambda x: (
            'Academic qualifications (No. of staff at the end of FY)-Bachelors degree' if '.1' in x else
            'Academic qualifications (No. of staff at the end of FY)-Masters degree (or above)'
        )
    )
    imf_isora_staff_metrics_df_2_long['indicator description'] = imf_isora_staff_metrics_df_2_long['indicator code'].map({
        'Academic qualifications (No. of staff at the end of FY)-Masters degree (or above)': 'Academic qualifications (No. of staff at the end of FY)-Masters degree (or above)',
        'Academic qualifications (No. of staff at the end of FY)-Bachelors degree': 'Academic qualifications (No. of staff at the end of FY)-Bachelors degree',
    })
    imf_isora_staff_metrics_df_2_long['year'] = imf_isora_staff_metrics_df_2_long['year'].str.replace(r'\.\d+', '', regex=True)
    
    imf_isora_staff_metrics_df_3 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=6, skipfooter=2, engine='openpyxl', sheet_name='Staff age distribution').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_3_long = pd.melt(imf_isora_staff_metrics_df_3, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_3_long['indicator code'] = imf_isora_staff_metrics_df_3_long['year'].apply(
        lambda x: (
            'Age distribution (No. of staff at the end of FY)-25-34 years' if '.1' in x else
            'Age distribution (No. of staff at the end of FY)-35-44 years' if '.2' in x else
            'Age distribution (No. of staff at the end of FY)-45-54 years' if '.3' in x else
            'Age distribution (No. of staff at the end of FY)-55-64 years' if '.4' in x else
            'Age distribution (No. of staff at the end of FY)-Over 64 years' if '.5' in x else
            'Age distribution (No. of staff at the end of FY)-Under 25 years'
        )
    )
    imf_isora_staff_metrics_df_3_long['indicator description'] = imf_isora_staff_metrics_df_3_long['indicator code'].map({
        'Age distribution (No. of staff at the end of FY)-Under 25 years': 'Age distribution (No. of staff at the end of FY)-Under 25 years',
        'Age distribution (No. of staff at the end of FY)-25-34 years': 'Age distribution (No. of staff at the end of FY)-25-34 years',
        'Age distribution (No. of staff at the end of FY)-35-44 years': 'Age distribution (No. of staff at the end of FY)-35-44 years',
        'Age distribution (No. of staff at the end of FY)-45-54 years': 'Age distribution (No. of staff at the end of FY)-45-54 years',
        'Age distribution (No. of staff at the end of FY)-55-64 years': 'Age distribution (No. of staff at the end of FY)-55-64 years',
        'Age distribution (No. of staff at the end of FY)-Over 64 years': 'Age distribution (No. of staff at the end of FY)-Over 64 years',
    })
    imf_isora_staff_metrics_df_3_long['year'] = imf_isora_staff_metrics_df_3_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_staff_metrics_df_4 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=6, skipfooter=2, engine='openpyxl', sheet_name='Staff length of service').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_4_long = pd.melt(imf_isora_staff_metrics_df_4, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_4_long['indicator code'] = imf_isora_staff_metrics_df_4_long['year'].apply(
        lambda x: (
            'Length of service (No. of staff at the end of FY)-5-9 years' if '.1' in x else
            'Length of service (No. of staff at the end of FY)-10-19 years' if '.2' in x else
            'Length of service (No. of staff at the end of FY)-Over 19 years' if '.3' in x else
            'Length of service (No. of staff at the end of FY)-Under 5 years'
        )
    )
    imf_isora_staff_metrics_df_4_long['indicator description'] = imf_isora_staff_metrics_df_4_long['indicator code'].map({
        'Length of service (No. of staff at the end of FY)-Under 5 years': 'Length of service (No. of staff at the end of FY)-Under 5 years',
        'Length of service (No. of staff at the end of FY)-5-9 years': 'Length of service (No. of staff at the end of FY)-5-9 years',
        'Length of service (No. of staff at the end of FY)-10-19 years': 'Length of service (No. of staff at the end of FY)-10-19 years',
        'Length of service (No. of staff at the end of FY)-Over 19 years': 'Length of service (No. of staff at the end of FY)-Over 19 years',
    })
    imf_isora_staff_metrics_df_4_long['year'] = imf_isora_staff_metrics_df_4_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_staff_metrics_df_5 = pd.read_excel('data/imf isora staff metrics.xlsx', skiprows=7, skipfooter=2, engine='openpyxl', sheet_name='Staff gender distribution').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_staff_metrics_df_5_long = pd.melt(imf_isora_staff_metrics_df_5, id_vars='country', var_name='year', value_name='value')
    imf_isora_staff_metrics_df_5_long['indicator code'] = imf_isora_staff_metrics_df_5_long['year'].apply(
        lambda x: (
            'Gender distribution (No. of staff at the end of FY)-All staff-Female' if '.1' in x else
            'Gender distribution (No. of staff at the end of FY)-All staff-Other' if '.2' in x else
            'Gender distribution (No. of staff at the end of FY)-Executives only-Male' if '.3' in x else
            'Gender distribution (No. of staff at the end of FY)-Executives only-Female' if '.4' in x else
            'Gender distribution (No. of staff at the end of FY)-Executives only-Other' if '.5' in x else
            'Gender distribution (No. of staff at the end of FY)-All staff-Male'
        )
    )
    imf_isora_staff_metrics_df_5_long['indicator description'] = imf_isora_staff_metrics_df_5_long['indicator code'].map({
        'Gender distribution (No. of staff at the end of FY)-All staff-Male': 'Gender distribution (No. of staff at the end of FY)-All staff-Male',
        'Gender distribution (No. of staff at the end of FY)-All staff-Female': 'Gender distribution (No. of staff at the end of FY)-All staff-Female',
        'Gender distribution (No. of staff at the end of FY)-All staff-Other': 'Gender distribution (No. of staff at the end of FY)-All staff-Other',
        'Gender distribution (No. of staff at the end of FY)-Executives only-Male': 'Gender distribution (No. of staff at the end of FY)-Executives only-Male',
        'Gender distribution (No. of staff at the end of FY)-Executives only-Female': 'Gender distribution (No. of staff at the end of FY)-Executives only-Female',
        'Gender distribution (No. of staff at the end of FY)-Executives only-Other': 'Gender distribution (No. of staff at the end of FY)-Executives only-Other',
    })
    imf_isora_staff_metrics_df_5_long['year'] = imf_isora_staff_metrics_df_5_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_staff_metrics_df = pd.concat([imf_isora_staff_metrics_df_1_long, imf_isora_staff_metrics_df_2_long, imf_isora_staff_metrics_df_3_long, imf_isora_staff_metrics_df_4_long, imf_isora_staff_metrics_df_5_long])


    imf_isora_op_metrics_audit_df_1 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Audit and verification').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_1_long = pd.melt(imf_isora_op_metrics_audit_df_1, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_1_long['indicator code'] = imf_isora_op_metrics_audit_df_1_long['year'].apply(
        lambda x: (
            'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits where a tax adjustment was made' if '.1' in x else
            'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits completed'
        )
    )
    imf_isora_op_metrics_audit_df_1_long['indicator description'] = imf_isora_op_metrics_audit_df_1_long['indicator code'].map({
        'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits completed': 'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits completed',
        'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits where a tax adjustment was made': 'Details on all audits and verifiction actions undertaken (excluding electronic compliance checks)-No. of audits where a tax adjustment was made',
    })
    imf_isora_op_metrics_audit_df_1_long['year'] = imf_isora_op_metrics_audit_df_1_long['year'].str.replace(r'\.\d+', '', regex=True)
    
    imf_isora_op_metrics_audit_df_2 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Value of additional assessments').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_2_long = pd.melt(imf_isora_op_metrics_audit_df_2, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_2_long['indicator code'] = imf_isora_op_metrics_audit_df_2_long['year'].apply(
        lambda x: (
            'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Electronic compliance checks' if '.1' in x else
            'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Total' if '.2' in x else
            'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-All audits (excluded electronic compliance checks)'
        )
    )
    imf_isora_op_metrics_audit_df_2_long['indicator description'] = imf_isora_op_metrics_audit_df_2_long['indicator code'].map({
        'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-All audits (excluded electronic compliance checks)': 'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-All audits (excluded electronic compliance checks)',
        'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Electronic compliance checks': 'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Electronic compliance checks',
        'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Total': 'Value of additional assessments raised from audits and verification actions (including penalties and interest) (in thousands in local currency)-Total',
    })
    imf_isora_op_metrics_audit_df_2_long['year'] = imf_isora_op_metrics_audit_df_2_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_op_metrics_audit_df_3 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Value of additional assessm_0').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_3_long = pd.melt(imf_isora_op_metrics_audit_df_3, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_3_long['indicator code'] = imf_isora_op_metrics_audit_df_3_long['year'].apply(
        lambda x: (
            'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Personal income tax' if '.1' in x else
            'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Value added tax' if '.2' in x else
            'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Tax withheld by employers from employees		' if '.3' in x else
            'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax'
        )
    )
    imf_isora_op_metrics_audit_df_3_long['indicator description'] = imf_isora_op_metrics_audit_df_3_long['indicator code'].map({
        'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax': 'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax',
        'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Personal income tax': 'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Personal income tax',
        'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Value added tax': 'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Value added tax',
        'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Tax withheld by employers from employees': 'Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Tax withheld by employers from employees',
    })
    imf_isora_op_metrics_audit_df_3_long['year'] = imf_isora_op_metrics_audit_df_3_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_op_metrics_audit_df_4 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=6, engine='openpyxl', sheet_name='Tax crime investigation').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_4_long = pd.melt(imf_isora_op_metrics_audit_df_4, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_4_long['indicator code'] = imf_isora_op_metrics_audit_df_4_long['year'].apply(
        lambda x: (
            'Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency' if '.1' in x else
            'Role of the administration in tax crime investigations - Other agency conducts investigations' if '.2' in x else
            'No. of tax crime investigation cases referred for prosecution during the fiscal year (where the tax administration has responsibility)' if '.3' in x else
            'Role of the administration in tax crime investigations - Directing and conducting investigations'
        )
    )
    imf_isora_op_metrics_audit_df_4_long['indicator description'] = imf_isora_op_metrics_audit_df_4_long['indicator code'].map({
        'Role of the administration in tax crime investigations - Directing and conducting investigations': 'Role of the administration in tax crime investigations - Directing and conducting investigations',
        'Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency': 'Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency',
        'Role of the administration in tax crime investigations - Other agency conducts investigations': 'Role of the administration in tax crime investigations - Other agency conducts investigations',
        'No. of tax crime investigation cases referred for prosecution during the fiscal year (where the tax administration has responsibility)': 'No. of tax crime investigation cases referred for prosecution during the fiscal year (where the tax administration has responsibility)',
    })
    imf_isora_op_metrics_audit_df_4_long['year'] = imf_isora_op_metrics_audit_df_4_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_op_metrics_audit_df_5 = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', skiprows=6, skipfooter=3, engine='openpyxl', sheet_name='Dispute resolution review proce').rename(columns={'Unnamed: 0': 'country'})
    imf_isora_op_metrics_audit_df_5_long = pd.melt(imf_isora_op_metrics_audit_df_5, id_vars='country', var_name='year', value_name='value')
    imf_isora_op_metrics_audit_df_5_long['indicator code'] = imf_isora_op_metrics_audit_df_5_long['year'].apply(
        lambda x: (
            'Mechanisms available for taxpayers to challenge assessments-Independent review by external body' if '.1' in x else
            'Mechanisms available for taxpayers to challenge assessments-Independent review by a higher appellate court' if '.2' in x else
            'Taxpayers must first pursue internal review where an internal review is permissible' if '.3' in x else
            'Mechanisms available for taxpayers to challenge assessments-Internal review by tax administration'
        )
    )
    imf_isora_op_metrics_audit_df_5_long['indicator description'] = imf_isora_op_metrics_audit_df_5_long['indicator code'].map({
        'Mechanisms available for taxpayers to challenge assessments-Internal review by tax administration': 'Mechanisms available for taxpayers to challenge assessments-Internal review by tax administration',
        'Mechanisms available for taxpayers to challenge assessments-Independent review by external body': 'Mechanisms available for taxpayers to challenge assessments-Independent review by external body',
        'Mechanisms available for taxpayers to challenge assessments-Independent review by a higher appellate court': 'Mechanisms available for taxpayers to challenge assessments-Independent review by a higher appellate court',
        'Taxpayers must first pursue internal review where an internal review is permissible': 'Taxpayers must first pursue internal review where an internal review is permissible',
    })
    imf_isora_op_metrics_audit_df_5_long['year'] = imf_isora_op_metrics_audit_df_5_long['year'].str.replace(r'\.\d+', '', regex=True)

    imf_isora_op_metrics_audit_df = pd.concat([imf_isora_op_metrics_audit_df_1_long, imf_isora_op_metrics_audit_df_2_long, imf_isora_op_metrics_audit_df_3_long, imf_isora_op_metrics_audit_df_4_long, imf_isora_op_metrics_audit_df_5_long])

    indicator4_4_3_2 = pd.concat([imf_isora_resources_ict_df, imf_isora_staff_metrics_df, imf_isora_op_metrics_audit_df])
    return indicator4_4_3_2


# indicator 4.4.4.2
def get_4_4_4_2():

    tjn_df = pd.read_csv('data/tjn data.csv').rename(columns={'country_name': 'Country'}).drop(columns=['cthi_2019_score', 'cthi_2021_score', 'cthi_2019_rank', 'cthi_2021_rank', 'cthi_2019_share', 'cthi_2021_share', 'sotj20_loss_corp_musd', 'sotj21_loss_corp_musd', 'sotj23_loss_corp_musd', 'sotj20_loss_total_share_healthexpenses', 'sotj21_loss_total_share_healthexpenses', 'sotj23_loss_total_musd', 'sotj23_loss_total_share_healthexpenses'])
    tjn_df_long = pd.melt(tjn_df, id_vars=['Country', 'iso3'], var_name='year', value_name='value')
    tjn_df_long['year'] = tjn_df_long['year'].str.extract(r'(\d{4})')
    tjn_df_long['indicator code'] = 'FSI'
    tjn_df_long['indicator description'] = 'Financial Secrecy Index'

    return tjn_df_long


# indicator 4.4.5.1 
def get_4_4_5_1():

    # read in data and extract indicators
    usaid_df = pd.read_excel('data/USAID tax effort and buyancy.xlsx', engine='openpyxl', sheet_name='Data')
    indicator4_4_5_1 = usaid_df[['country_name', 'country_id', 'year', 'Tax buoyancy [by_tax]']].rename(columns={"country_name": 'country', 'country_id': 'm49', 'Tax buoyancy [by_tax]': 'value'})
    indicator4_4_5_1['indicator code'] = "Tax buoyancy [by_tax]"
    indicator4_4_5_1['indicator description'] = "Tax buoyancy [by_tax]"

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

    # df_4_3_1_1 = get_4_3_1_1().to_csv("indicator_data_files/indicator 4.3.1.1.csv")

    # df_4_3_1_2 = get_4_3_1_2().to_csv("indicator_data_files/indicator 4.3.1.2.csv")

    # df_4_3_1_3 = get_4_3_1_3().to_csv("indicator_data_files/indicator 4.3.1.3.csv")

    # df_4_3_2_1 = get_4_3_2_1().to_csv("indicator_data_files/indicator 4.3.2.1.csv")

    # df_4_3_2_2 = get_4_3_2_2().to_csv("indicator_data_files/indicator 4.3.2.2.csv")

    # df_4_4_2_1 = get_4_4_2_1().to_csv("indicator_data_files/indicator 4.4.2.1.csv")

    # df_4_4_2_2 = get_4_4_2_2().to_csv("indicator_data_files/indicator 4.4.2.2.csv")

    # df_4_4_2_3 = get_4_4_2_3().to_csv("indicator_data_files/indicator 4.4.2.3.csv")

    # df_4_4_2_4 = get_4_4_2_4().to_csv("indicator_data_files/indicator 4.4.2.4.csv")

    # df_4_4_3_2 = get_4_4_3_2().to_csv("indicator_data_files/indicator 4.4.3.2.csv")

    # df_4_4_4_2 = get_4_4_4_2().to_csv("indicator_data_files/indicator 4.4.4.2.csv")

    # df_4_4_5_1 = get_4_4_5_1().to_csv("indicator_data_files/indicator 4.4.5.1.csv")

    exit()