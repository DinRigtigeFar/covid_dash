from os import environ

import plotly.express as px
import plotly.graph_objs as go

colorscheme = px.colors.cyclical.IceFire
colorscheme += px.colors.diverging.Portland

mapbox_access_token = environ['MAPBOX_KEY']

def base_graph(dataframe, dict_of_countries_and_popsize, scale=1, dtd=True, death=False):
	"""
	Function that returns a plotly graph object with the option of scaling it
	"""
	plots = []
	plots_dtd = []

	for country, popsize in dict_of_countries_and_popsize.items():
		# Day to day? Make data ready
		if dtd:
			try:
				day_to_day_cases = dataframe[dataframe["Country/Region"]
											 == country].iloc[-1]
				tmp = day_to_day_cases[day_to_day_cases != 0].iloc[4:]
				case_day_to_day = [y-x for x, y in zip(tmp, tmp[1:])]
			except Exception as e:
				print(f'Failed due to error: {e}')
		# Make plots
		try:
			cases = dataframe[dataframe["Country/Region"] == country].iloc[-1]
			if scale != 1:
				y_day = cases[cases != 0].iloc[4:]/(popsize/scale)
				
				if dtd:
					y_dtd = [i/(popsize/scale) for i in case_day_to_day]

			else:
				y_day = cases[cases != 0].iloc[4:]			
				if dtd:
					y_dtd = case_day_to_day

			trace1 = {
				"name": country,
				"mode": "lines",
				"type": "scatter",
				"x": cases[cases != 0].index[4:],
				"y": y_day,
			}
			if dtd:

				dtd_plot = {
					"name": country,
					"mode": "lines",
					"type": "scatter",
					"x": day_to_day_cases[day_to_day_cases != 0].index[4:],
					"y": y_dtd,
				}

				plots_dtd.append(dtd_plot)
			plots.append(trace1)
		except Exception as e:
			print(f'Failed due to error: {e}')
	if scale != 1:
		if not death:
			layout = {
						"title": f"COVID-19 cases per {int(scale/1000)}K capita per country",'xaxis_title':"Date",
						'yaxis_title':"Cases of COVID-19 scaled"}
			if dtd:
				layout_dtd = {
							"title": f"New COVID-19 cases per day per {int(scale/1000)}K capita",'xaxis_title':"Date",
						'yaxis_title':"Cases of COVID-19 scaled"}
		else:
			layout = {
						"title": f"COVID-19 deaths per {int(scale/1000)}K capita per country",'xaxis_title':"Date",
						'yaxis_title':"Deaths of COVID-19 scaled"}
			if dtd:
				layout_dtd = {
							"title": f"New COVID-19 deaths per day per {int(scale/1000)}K capita",'xaxis_title':"Date",
						'yaxis_title':"Deaths of COVID-19 scaled"}
	else:
		if not death:
			layout = {"title": "COVID-19 cases per country",'xaxis_title':"Date",
						'yaxis_title':"Cases of COVID-19"}
			if dtd:
				layout_dtd = {
							"title": "New COVID-19 cases per day per country",'xaxis_title':"Date",
						'yaxis_title':"Cases of COVID-19"}
		else:
			layout = {"title": "COVID-19 deaths per country",'xaxis_title':"Date",
						'yaxis_title':"Deaths of COVID-19"}
			if dtd:
				layout_dtd = {
							"title": "New COVID-19 deaths per day per country",'xaxis_title':"Date",
						'yaxis_title':"Deaths of COVID-19"}
	fig = go.Figure(data=plots, layout=layout)
	fig.update_xaxes(tickangle=30, title_font=dict(size=16), nticks=20)
	fig
	try:
		fig_dtd = go.Figure(data=plots_dtd, layout=layout_dtd)
		fig_dtd.update_xaxes(tickangle=30, title_font=dict(size=16), nticks=20)
		return fig, fig_dtd
	except:
		pass
	
	return fig


def pie_part_chart(dataframe, dict_of_countries_and_popsize, scale=1):
	"""
	Function that returns a pie chart of the specified countries
	"""
	real_labs = [i for i in dict_of_countries_and_popsize.keys()]
	cases = []
	for i in real_labs:
		cases.append(dataframe[dataframe["Country/Region"]
						  == i].iloc[-1])
	y = [case.iloc[-1] for case in cases]

	if scale != 1:
		popsize = [i for i in dict_of_countries_and_popsize.values()]
		y2 = [i/(k/scale) for i,k in zip(y,popsize)]
		prelim = go.Pie(
			labels=real_labs,
			values=y2,
			name='pieFraction'
		)
		layout = {'title': f'Fraction of COVID cases between selected countries scaled to {int(scale/1000)}K'}
	else:
		prelim = go.Pie(
			labels=real_labs,
			values=y,
			name='pieFraction'
		)
		layout = {'title': 'Fraction of COVID cases between selected countries'}
	fig = go.Figure(data=[prelim], layout=layout)
	fig.update_layout({'height': 800})
	fig.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='label+value')
	return fig


def map_graph(dataframe, dict_of_countries_and_popsize, scale):
	"""
	Function that returns a map of the inpput
	"""

	
	lat = []
	lon = []
	total_infected = []
	

	for i in dict_of_countries_and_popsize.keys():
		lat.append(float(dataframe[dataframe["Country/Region"] == i].iloc[0]['Lat']))
		lon.append(float(dataframe[dataframe["Country/Region"] == i].iloc[0]['Long']))

		total_infected.append(dataframe[dataframe["Country/Region"] == i].iloc[0])
	
	y = [case.iloc[-1] for case in total_infected]
	if scale != 1:
		if len(y) == 273:
			pre_size = [k/(i/scale) if k/(i/scale)>=1 else 1 for k,i in zip(y, dict_of_countries_and_popsize.values())]
			sizes = [i/sum(pre_size)*4000 for i in pre_size]
		else:
			pre_size = [k/(i/scale) for k,i in zip(y, dict_of_countries_and_popsize.values())]
			sizes = [i/sum(pre_size)*400 for i in pre_size]
	else:
		if len(y) == 273:
			pre_size = [k/(i) if k/(i)>=1 else 1 for k,i in zip(y, dict_of_countries_and_popsize.values())]
			sizes = [i/sum(pre_size)*4000 for i in pre_size]
		else:
			pre_size = [k/(i) for k,i in zip(y, dict_of_countries_and_popsize.values())]
			sizes = [i/sum(pre_size)*400 for i in pre_size]
	fig = go.Figure(go.Scattermapbox(
        lat=lat,
        lon=lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=sizes
        ),
		
        text=[i for i in dict_of_countries_and_popsize.keys()],
		hovertext=[f'Infected in {c}: {i}' for i,c in zip(y,dict_of_countries_and_popsize.keys())]
    ))

	fig.update_layout(
		autosize=True,
		hovermode='closest',
		height=1200,
		mapbox=dict(
			accesstoken=mapbox_access_token,
			bearing=0,
			center=dict(
				lat=28,
				lon=20
			),
			pitch=0,
			zoom=1.8
		),
		title='COVID-19 cases by country'
	)

	return fig


def animation_world_map(dataframe_melted):
	"""
	Function that illustrates the development of COVID-19 on a worldwide scale
	"""

	fig = px.scatter_mapbox(
		data_frame=dataframe_melted,
        lat='Lat',
        lon='Long',
        color='Cumulative_Cases',
		animation_frame='Date',
		animation_group='Country/Region',
        size='Cumulative_Cases',
		size_max=100,
		hover_name='Country/Region',
		hover_data={'Date':True, 'Cumulative_Cases':True, 'Lat':False, 'Long':False},
    )
	fig.update_layout(
		autosize=True,
		hovermode='closest',
		height=1200,
		mapbox=dict(
			accesstoken=mapbox_access_token,
			bearing=0,
			center=dict(
				lat=28,
				lon=20
			),
			pitch=0,
			zoom=1.8
		),
		title='Development of the COVID-19 pandemic',
		transition = {'duration': 500},
	)
	fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
	fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["redraw"] = True

	return fig

def animation_us_map(dataframe_melted):
	"""
	Function that illustrates the development of COVID-19 in the US alone
	"""

	fig = px.scatter_mapbox(
		data_frame=dataframe_melted,
        lat='Lat',
        lon='Long_',
        color='Cumulative_Cases',
		animation_frame='Date',
		animation_group='Admin2',
        size='Cumulative_Cases',
		size_max=100,
		hover_name='Admin2',
		hover_data={'Date':True, 'Cumulative_Cases':True, 'Lat':False, 'Long_':False},
    )
	fig.update_layout(
		autosize=True,
		hovermode='closest',
		height=1200,
		mapbox=dict(
			accesstoken=mapbox_access_token,
			bearing=0,
			center=dict(
				lat=38,
				lon=-97
			),
			pitch=0,
			zoom=4
		),
		title='Development of the COVID-19 pandemic in the US',
		transition = {'duration': 500},
	)
	fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
	fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["redraw"] = True

	return fig

	