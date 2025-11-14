from plotly.graph_objs import Figure, Scatter, Candlestick
import plotly.io as pio 
import random
from typing import Union
import plotly.express as px
from .measure import Measure as M


colors = ['#1F77B4']

class GRAPH():
	font_family="Courier New"
	font_color="blue"
	title_font_family="Times New Roman"
	title_font_color="blue"
	title_font_size = 20
	legend_title_font_color="green"

def generator_colour():
	global colors
	
	color =  '#' + ''.join([random.choice('ABCDEF0123456789') for i in range(6)]) 
	if color in colors:
		generator_colour()
	else:
		colors.append(color)	
		return color 

def setting_layout(figure,title,x_axis,y_axis):

	figure.update_layout(
		    font_family= GRAPH.font_family,
		    font_color=GRAPH.font_color,
		    title_font_family=GRAPH.title_font_family,
		    title_font_color=GRAPH.title_font_color,
		    legend_title_font_color=GRAPH.legend_title_font_color,
		    title=dict(text=title , font=dict(size=GRAPH.title_font_size), yref='paper'),
		    xaxis_title=x_axis ,
		    xaxis=dict(type='category'),
    		yaxis_title=y_axis
    )

	return figure

def create_figure( data, 
				   title,
				   x_axis,
				   y_axis):
	
	figure = Figure(Scatter(x=data[x_axis], y=data[y_axis],mode='lines', line = {'color' : generator_colour()}))
	figure = setting_layout(figure,title,x_axis,y_axis )
	
	return figure	

def create_candlestick( data, 
				    	title,
				        x_axis,
				        y_axis):

	figure = Figure(data=[Candlestick( x=data[M.DATE],
							           open=data[M.OPEN],
							           high=data[M.HIGH],
							           low=data[M.LOW],
							           close=data[M.CLOSE])])
	figure = setting_layout(figure,title,x_axis,y_axis )
	return figure

def create_multiple_axes_figure(data, 
							    title,
							    x_axis,
							    y_axis,
							    main_y_axis):
	fig = go.Figure()
	fig.add_trace(go.Scatter( x= data[x_axis], y = data[main_y_axis], name = main_y_axis,line = {'color' : generator_colour()} ))
	fig.layout['yaxis'] = {'title' : main_y_axis} 
	for i,y in enumerate(y_axis):
		fig.add_trace(go.Scatter( x= data[x_axis], y = data[y], name = y ,yaxis=f'y{i+2}',line = {'color' : generator_colour()} ))
		fig.layout[f'yaxis{i+2}'] = {'title' : y, 'anchor' : 'free', 'overlaying' : 'y', 'side' : 'right', 'position' :0.05*(i) } 
	return fig

def adding_horizontal_line(figure, value, name = 'avg'):
	color = generator_colour() 
	figure.add_hline(y=value, annotation_text='{:.4f}'.format(value), 
		              annotation_position="bottom right",
		              annotation_font_size=13,
		              annotation_font_color=color ,line= {'color' :color })
	return figure

def adding_line(figure,
				data, 
				name,
				x_axis,
				y_axis  ):
	color = generator_colour()
	# check we need to add two lines same colour
	figure.add_trace(Scatter(x=data[x_axis], y=data[y_axis], mode='lines', name = name, line = {'color' : color}))
	return figure	


def plot(figure, folder_path, file_name = None, extension = 'html', PLOT = False, SAVE = False):

	if PLOT:
		iplot(figure)
	if SAVE:
		figure.write_html(f'{folder_path}/{file_name}.{extension}')
