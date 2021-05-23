import pandas as pd
import numpy as np
from plotly.offline import *

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from scipy import stats

from plotly.subplots import make_subplots
from plotly.offline import *

df1 = pd.read_csv('C:/Users/benno/OneDrive/Python/NYCDSA/Final project/Datasets/Finalproject_maindf.csv')
df2 = pd.read_csv('C:/Users/benno/OneDrive/Python/NYCDSA/Final project/Datasets/Finalproject_dfbars.csv')

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])


app.layout = html.Div([
	html.H1('AB Testing',
		style={'textAlign':'center',
				}),
	html.H2('Which segment performs the best over time?',
		style={'textAlign':'center',
				'font-size':'1em'
				}),

	dcc.Checklist(
		id='main-selector',
		options=[
			{'label':'a','value':'a'},
			{'label':'b','value':'b'},
			{'label':'c','value':'c'},
			{'label':'d','value':'d'},
			{'label':'e','value':'e'},
			{'label':'f','value':'f'},
			{'label':'g','value':'g'},
			{'label':'h','value':'h'},
			{'label':'i','value':'i'},
			{'label':'j','value':'j'},
			{'label':'k','value':'k'},
			{'label':'l','value':'l'},
			{'label':'m','value':'m'},
			{'label':'n','value':'n'},
			{'label':'o','value':'o'},
			{'label':'p','value':'p'},
			{'label':'q','value':'q'},
			{'label':'r','value':'r'},
			{'label':'s','value':'s'},
			{'label':'t','value':'t'},
			{'label':'u','value':'u'},
			{'label':'v','value':'v'},
			{'label':'w','value':'w'},
			{'label':'x','value':'x'},
			{'label':'y','value':'y'},
			{'label':'z','value':'z'},
		],
		value=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
		labelStyle={'display':'absolute'},
		style={'width':'15%',
		'z-index':'900',
		'height':'100%',
		'position':'absolute',
		}

		),

	dcc.Graph(
		id='main-graph',
		),

	dcc.Graph(
		id='dashboard-top',
		style={'margin':'0 ,0, 10em, 0'}
		),
	],
	)

@app.callback(
	Output('main-graph','figure'),
	Output('dashboard-top','figure'),
	Input('main-selector','value')
	)
def update_figure(selected_cats):

    fig = make_subplots(rows=1,cols=1,specs=[[{'type':'scene'}]])

    newdf = []

    for i in np.unique(selected_cats):
    	newdf.append(df1[df1.namecol == i])

    for i in newdf:
        fig.add_scatter3d(x=i.year,
        y=i.namecol,
        z=i.count1,
        mode='lines+markers',
        line={'color':'darkblue'},
        marker={'color':i.count1,'symbol':'diamond','size':4},
        row=1,col=1)

    fig.update_layout(

        title={'text':'Category Performance by Year'},
        scene={
        'xaxis_title':'Year',
        'yaxis_title':'Segment',
        'zaxis_title':'Performance',
        },
        height=900,
        # width=2100,
        showlegend = False,
        )

    fig2 = make_subplots(rows=4,cols=4,specs=[[{'type':'table'},{'rowspan':2,'colspan':3},None,None],[{'type':'scene'},None,None,None],[{'rowspan':2,}, {'rowspan':2,'colspan':3},None,None],[None, None, None, None]],subplot_titles=('ANOVA','Flattened Year','Full Data','Performance by Year','Length by Year'))

    df_agg = df1.groupby(['year']).agg({'count1':np.sum, 'length':np.mean}).reset_index().set_index('year')    
    df_agg.name = 'agg'

    f, p = stats.f_oneway(*[np.random.choice(i.count1, size=40, replace=True).tolist() for i in newdf])

    fig2.add_table(header=dict(values=['Stat','Score']),
                 cells=dict(values=[['F','P'],[f.round(4),p.round(4)]]),
                  columnwidth=[100,400],
                 row=1,col=1)

    fig2.add_scatter(x=df_agg.length,
                    y = df_agg.count1,
                    name=str(df_agg.name),
                    mode='markers',
                    marker={'color':df_agg.count1},
                    row=1,col=2,)
    

    fig2.add_scatter3d(x=df_agg.index,
                      y=df_agg.count1,
                      z=df_agg.length,
                      name=str(df_agg.name),
                      mode='markers',
                      marker={'color':df_agg.count1},
                      scene='scene',
                      row=2,col=1,)   

    fig2.add_scatter(x=df_agg.index,
                    y = df_agg.count1,
                    name=str(df_agg.name),
                    mode='lines',
                    marker={'color':'darkblue'},
                    fill='tonexty',
                    row=3,col=1,)

    fig2.add_scatter(x=df_agg.index,
                    y = df_agg.length,
                    name=str(df_agg.name),
                    mode='markers',
                    marker={'color':df_agg.length},
                    row=3,col=2,)
     
    


    fig2.update_layout(height=900,
                     showlegend=False)

    fig2.update_yaxes({'title':{'text':'Performance','font':{'size':10}}}, row=1,col=4)    
    fig2.update_xaxes({'title':{'text':'Word Length','font':{'size':10}}}, row=1,col=4)    
    
    fig2.update_yaxes({'title':{'text':'Performance','font':{'size':10}}}, row=2,col=1)    
    fig2.update_xaxes({'title':{'text':'Year','font':{'size':10}}}, row=2,col=1)   
    
    fig2.update_yaxes({'title':{'text':'Word Length','font':{'size':10}}}, row=2,col=4)    
    fig2.update_xaxes({'title':{'text':'Year','font':{'size':10}}}, row=2,col=4)    

    fig2.update_scenes({'xaxis':{'title':{'text':'Year', 'font':{'size':10}}},
                       'yaxis':{'title':{'text':'Performance', 'font':{'size':10}}},
                       'zaxis':{'title':{'text':'Word Length', 'font':{'size':10}}}})

    return fig, fig2

if __name__ == '__main__':
	app.run_server(debug=True)


# Dash html code in python
# html.Div([
#     html.H1('First Dash App'),
#     html.Div([
#         html.P("Dash converts Python classes into HTML"),
#         html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
#     ])
# ])

