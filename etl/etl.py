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



# indicator 4.4.3.1
def get_4_4_2_1():

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
    imf_isora_resources_ict_df = pd.read_excel('data/imf isora resources and ICT infrastructure.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_rstaff_metrics_df = pd.read_excel('data/imf isora staff metrics.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_stakeholder_df = pd.read_excel('data/imf isora stakeholder interactions.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_op_metrics_audit_df = pd.read_excel('data/imf isora op metrics audit, criminal investigations, dispute resolution.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_op_metrics_payments_df = pd.read_excel('data/imf isora op metrics payments and arrears.xlsx', engine='openpyxl', sheet_name=None)
    imf_isora_op_metrics_registration_df = pd.read_excel('data/imf isora op metrics registration and filing.xlsx', engine='openpyxl', sheet_name=None)

    return pd.concat([imf_isora_resources_ict_df, imf_isora_rstaff_metrics_df, imf_isora_stakeholder_df, imf_isora_op_metrics_audit_df, imf_isora_op_metrics_payments_df, imf_isora_op_metrics_registration_df])


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
    get_4_4_4_2()