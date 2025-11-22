from plotly.graph_objs import Figure, Scatter, Candlestick, Bar
import plotly.io as pio 
import random
from typing import Union
import plotly.express as px
from plotly.subplots import make_subplots
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
		    xaxis=dict(type='date'),
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
	figure = make_subplots(rows=2, cols=1, shared_xaxes=True, 
			               vertical_spacing=0.30, subplot_titles=(title.split(' ')[0], M.VOLUME), 
			               row_width=[0.2, 0.7])
	figure = setting_layout(figure,title,x_axis,y_axis)

	figure.add_trace(Candlestick( x=data[M.DATE],
							           open=data[M.OPEN],
							           high=data[M.HIGH],
							           low=data[M.LOW],
							           close=data[M.CLOSE],
							           name =title.split(' ')[0]),row=1, col=1)

	figure.add_trace(Bar(x=data[M.DATE], y=data[M.VOLUME], showlegend=True, name=M.VOLUME,marker=dict(color=generator_colour())), row=2, col=1)
	figure.update_layout(xaxis_rangeslider_visible=True)

	return figure

def create_multiple_axes_figure(data, 
							    title,
							    x_axis,
							    y_axis,
							    main_y_axis):
	fig = Figure()
	fig.add_trace(Scatter( x= data[x_axis], y = data[main_y_axis], name = main_y_axis,line = {'color' : generator_colour()} ))
	fig.layout['yaxis'] = {'title' : main_y_axis} 
	for i,y in enumerate(y_axis):
		if main_y_axis == y : continue
		#fig.add_trace(Scatter( x= data[x_axis], y = data[y], name = y ,yaxis=f'y{i+2}',line = {'color' : generator_colour()} ))
		fig.add_trace(Scatter( x= data[x_axis], y = data[y], name = y ,line = {'color' : generator_colour()} ))
		#fig.layout[f'yaxis{i+2}'] = {'title' : y, 'anchor' : 'free', 'overlaying' : 'y', 'side' : 'right', 'position' :0.02*(i) }
	fig = setting_layout(fig,title,x_axis,main_y_axis )
	return fig

def adding_horizontal_line(figure, value , name ):
	color = generator_colour() 
	figure.add_hline(y=value, annotation_text= name, 
		              annotation_position="bottom right",
		              annotation_font_size=13,
		              annotation_font_color=color ,line= {'color' :color })
	return figure

def adding_vertical_line(figure, value, name):
	color = generator_colour() 
	figure.add_vline(x=value, annotation_text=name, 
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
