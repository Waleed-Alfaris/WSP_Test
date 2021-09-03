#import required packages and vega_dataset
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from vega_datasets import data

#initialize dash app
app = dash.Dash(__name__)

# load the data
df = data.barley()

# 'yield' is a reserved varibale name in python. Will rename for ease of writing code
df.rename(columns={'yield' : 'Total_Yield'}, inplace=True)

#dashboard layout
app.layout = html.Div([
    
    html.H1('WSP Test Task', style={'text-align': 'center'}),
    
    dcc.Dropdown(id = 'select_plot',
                options = [
                    {'label':'Sum Of Yield', 'value':'Sum of Yield'},
                    {'label':'Median of Yield', 'value':'Median of Yield'}],
                multi = False,
                value = 'Sum of Yield',
                style = {'width': '40%'} 
                ),
    
    html.Div(id = 'output_container', children = []),
    html.Br(),
    
    dcc.Graph(id = 'my_plot', figure = {})
])

#connect plots with Dash Components
@app.callback([
    Output(component_id = 'output_container', component_property = 'children'),
    Output(component_id = 'my_plot', component_property = 'figure'),
    Input(component_id = 'select_plot', component_property = 'value')
             ])

def update_graph(option):
    container = 'The plot selected by the user was: {}'.format(option)
    
    #Sum Of Yield
    #plotly express
    if option == 'Sum of Yield':
        fig = px.bar(
        df, 
        x = 'variety', 
        y = 'Total_Yield', 
        color = 'site', 
        barmode = 'stack',
        labels = dict(Total_Yield= '<b>Sum of Yield</b>', variety= '<b>Variety</b>', site='<b>site</b>')
                    )

        fig.update_xaxes(ticks='outside', tickangle = -90)

        fig.update_yaxes(ticks='outside')

        fig.update_layout(autosize = False,
                          width = 500,
                          height = 600,
                          yaxis_range = [0,500],
                          yaxis = dict(
                                      tick0 = 0,
                                      dtick = 50
                                      )
                         )

        fig.update_traces(marker_line_width=0)
        
    elif option == 'Median of Yield':
    #find the median annual yield per site
        df_median = df.groupby(by=['site', 'year']).median().reset_index()

        #initialize figure
        fig = go.Figure()

        #iteratively add traces for each site
        for site in df_median['site'].unique().tolist():
            fig.add_trace(go.Scatter(x=df_median.loc[df_median['site']==site,'year'],
                                     y=df_median.loc[df_median['site']==site,'Total_Yield'],
                                     mode='lines', 
                                     name = site,
                                     showlegend=True
                                    )
                         )

        #format plot
        fig.update_layout(yaxis = dict(
                                      tickmode = 'linear',
                                      tick0 = 0,
                                      dtick = 5
                                      ),

                          yaxis_range = [0,55],
                          xaxis = dict(
                                      tickmode = 'linear',
                                      tick0 = 1930,
                                      dtick = 1,
                                      ),

                          xaxis_range = [1931,1932],
                          margin = dict(l=20, r=20, t=20, b=20, pad=20),
                          legend = dict(
                                       title = '<b>site</b>',
                                       y = 1,
                                       x = 1.5,
                                       ),
                          autosize = False,
                          width = 400,
                          height = 600
                         )

        fig.update_xaxes(
                        title_text = '<b>Year</b>',
                        ticks = 'outside',
                        tickangle = -90
                        )

        fig.update_yaxes(
                        title_text = '<b>Median of Yield</b>',
                        ticks = 'outside'
                        )
        
    return container, fig

#run the plotly Dashboard
if __name__ == '__main__':
    app.run_server()