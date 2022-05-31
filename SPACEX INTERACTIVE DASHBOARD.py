# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

s = list(set(list(spacex_df['Launch Site'])))
olist = []
olist.append({'label': 'All Sites', 'value': 'ALL'})
for i in s:
    olist.append({'label' : i, 'value' : i })

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                        
                                dcc.Dropdown(id='site-dropdown', 
                                             options = olist,
                                             placeholder = 'Select a Launch Site here'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([], id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 10000: '10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([], id='success-payload-scatter-chart')
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='children'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names= 'Launch Site', 
        title='Total success launches by site')
        return dcc.Graph(figure=fig)
    elif entered_site is not None:
        dls = spacex_df[spacex_df['Launch Site'] == str(entered_site)]
        fig = px.pie(dls, names='class', 
        title='Total success launches by '+str(entered_site))
        return dcc.Graph(figure=fig)

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='children'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, entered_payload):
    print(entered_payload)
    if entered_site == 'ALL':
        dls = spacex_df
        dls = dls[dls['Payload Mass (kg)'] > entered_payload[0]]
        dls = dls[dls['Payload Mass (kg)'] < entered_payload[1]]
        dls.reset_index(inplace=True)
        fig = px.scatter(dls,
        x = dls['Payload Mass (kg)'], 
        y = dls['class'], 
        color='Booster Version', 
        title='Correlation between payload and success for sites')
        return dcc.Graph(figure=fig)
    elif entered_site is not None:
        dls = spacex_df[spacex_df['Launch Site'] == str(entered_site)]
        dls = dls[dls['Payload Mass (kg)'] > entered_payload[0]]
        dls = dls[dls['Payload Mass (kg)'] < entered_payload[1]]
        dls.reset_index(inplace=True)
        fig = px.scatter(dls,
        x = dls['Payload Mass (kg)'], 
        y = dls['class'], 
        color='Booster Version', 
        title='Correlation between payload and success for site')
        return dcc.Graph(figure=fig)




# Run the app
if __name__ == '__main__':
    app.run_server()
