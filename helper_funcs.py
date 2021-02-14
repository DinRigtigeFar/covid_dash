import pandas as pd
from os import listdir, path

from graphFuncs import animation_world_map, animation_us_map

def make_clean_df(to_clean):
	"""
	Small function to clean cases and deaths dataframes
	"""

	# Make some updates to the dataframe to sum Australia, Canada and China provinces as one country
	bad1 = 'Australian Capital TerritoryNew South WalesNorthern TerritoryQueenslandSouth AustraliaTasmaniaVictoriaWestern Australia'
	bad1_lat = -26.4390917
	bad1_lon = 133.281323

	bad2 = 'AlbertaBritish ColumbiaDiamond PrincessGrand PrincessManitobaNew BrunswickNewfoundland and LabradorNorthwest TerritoriesNova ScotiaNunavutOntarioPrince Edward IslandQuebecRepatriated TravellersSaskatchewanYukon'
	bad2_lat = 56.0
	bad2_lon = -96.0

	bad3 = 'AnhuiBeijingChongqingFujianGansuGuangdongGuangxiGuizhouHainanHebeiHeilongjiangHenanHong KongHubeiHunanInner MongoliaJiangsuJiangxiJilinLiaoningMacauNingxiaQinghaiShaanxiShandongShanghaiShanxiSichuanTianjinTibetXinjiangYunnanZhejiang'
	bad3_lat = 35.8592948
	bad3_lon = 104.1361118
	# Append the countries to the dataframe
	to_clean = to_clean.append(to_clean[to_clean['Country/Region']=='Australia'].sum(), ignore_index=True)
	to_clean = to_clean.append(to_clean[to_clean['Country/Region']=='Canada'].sum(), ignore_index=True)
	to_clean = to_clean.append(to_clean[to_clean['Country/Region']=='China'].sum(), ignore_index=True)
	# Find all to_clean where province/state is not NaN and update the country with that name
	to_clean.loc[to_clean['Province/State'].isnull()==False, ['Country/Region']] = to_clean['Province/State']
	# Make the lat/long and Country name the correct one for the 3 bad countries
	to_clean.loc[to_clean['Country/Region']==bad1, ['Lat']] = bad1_lat
	to_clean.loc[to_clean['Country/Region']==bad1, ['Long']] = bad1_lon
	to_clean.loc[to_clean['Country/Region']==bad1, ['Country/Region']] = 'Australia'
	to_clean.loc[to_clean['Country/Region']==bad2, ['Lat']] = bad2_lat
	to_clean.loc[to_clean['Country/Region']==bad2, ['Long']] = bad2_lon
	to_clean.loc[to_clean['Country/Region']==bad2, ['Country/Region']] = 'Canada'
	to_clean.loc[to_clean['Country/Region']==bad3, ['Lat']] = bad3_lat
	to_clean.loc[to_clean['Country/Region']==bad3, ['Long']] = bad3_lon
	to_clean.loc[to_clean['Country/Region']==bad3, ['Country/Region']] = 'China'
	# Sort the dataframe so order is by country again
	to_clean = to_clean.sort_values(by=['Country/Region'])

	return to_clean

############################## The following is for the world app layout ##############################

deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
cases = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
popsizes = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv')

# If province_state has a value, make that value the country_region instead
popsizes.loc[popsizes['Province_State'].isnull()==False, ['Country_Region']] = popsizes['Province_State']

deaths = make_clean_df(deaths)
cases = make_clean_df(cases)

# Make the date "tidy" so it can be visualized in an animation map
melted_cases = cases.melt(id_vars=['Province/State','Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Cumulative_Cases')

# Downsample the data to update on a weekly basis instead of daily
melted_cases = melted_cases.set_index(['Date'])

melted_cases.index = pd.to_datetime(melted_cases.index)

downsample = melted_cases.groupby(['Country/Region']).resample('W', origin='start').mean()
melted_cases = downsample.reset_index()
melted_cases['Date'] = melted_cases['Date'].astype(str)

# Make a static animation map
ani_map = animation_world_map(melted_cases)

regions = {}
reg_dir = 'regions'
# Open file with countries in both cases and popsizes
for i in listdir(reg_dir):
	name = i.split('.')[0]
	with open(path.join(reg_dir,i), 'r') as f:
		regions[name] = tuple(j.strip() for j in f)


############################## The following is for the US only layout ##############################

# Read the data
us_time_cases = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")

# Make the date "tidy" so it can be visualized in an animation map
melt_us_cases = us_time_cases.melt(id_vars=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_','Combined_Key'], var_name='Date', value_name='Cumulative_Cases')

# Downsample the data to update on a weekly basis instead of daily
melt_us_cases = melt_us_cases.set_index(['Date'])

melt_us_cases.index = pd.to_datetime(melt_us_cases.index)

downsample = melt_us_cases.groupby(['Province_State','Admin2']).resample('W', origin='start').mean()
melt_us_cases = downsample.reset_index()
melt_us_cases['Date'] = melt_us_cases['Date'].astype(str)

# Make a static animation map
ani_us_map = animation_us_map(melt_us_cases)