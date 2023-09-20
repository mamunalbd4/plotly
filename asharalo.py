import dash
import dash.dcc as dcc
import dash.html as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load CSV data directly from the provided URL
url = "https://raw.githubusercontent.com/mamunalbd4/asharalo/main/asharalofinal.csv"
df = pd.read_csv(url)

app = dash.Dash(__name__)
server=app.server
# Initialize layout
app.layout = html.Div([
    html.H1("Ashar Alo Project Baseline Survey (Summery)", style={'textAlign': 'center'}),  # Add the header
    dcc.Dropdown(
        id='district-dropdown',
        options=[{'label': district, 'value': district} for district in df['District'].unique()],
        value=df['District'].unique()[0],
        placeholder="Select a District"
    ),
    dcc.Dropdown(
        id='upazilla-dropdown',
        placeholder="Select a Upazilla"
    ),
    dcc.Dropdown(
        id='union-dropdown',
        placeholder="Select a Union"
    ),
    dcc.Dropdown(
        id='village-dropdown',
        placeholder="Select a Village",
        style={'display': 'none'}  # Hiding the dropdown
    ),
    dcc.RadioItems(
        id='gender-radio',
        options=[
            {'label': 'All Genders', 'value': 'All'},
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'},
        ],
        value='All',
        labelStyle={'display': 'block', 'margin-right': '10px'}  # Add margin for spacing
    ),
    dcc.RadioItems(
        id='disability-card-radio',
        options=[
            {'label': 'All Disability Cards', 'value': 'All'},
            {'label': 'Has Disability Card', 'value': 'Yes'},
            {'label': 'No Disability Card', 'value': 'No'},
        ],
        value='All',
        labelStyle={'display': 'block', 'margin-right': '10px'}  # Add margin for spacing
    ),
    dcc.Graph(id='bar-chart')
])

@app.callback(
    Output('upazilla-dropdown', 'options'),
    Input('district-dropdown', 'value')
)
def update_upazilla_dropdown(selected_district):
    upazillas = df[df['District'] == selected_district]['Upazilla'].unique()
    return [{'label': upazilla, 'value': upazilla} for upazilla in upazillas]

@app.callback(
    Output('union-dropdown', 'options'),
    [Input('district-dropdown', 'value'),
     Input('upazilla-dropdown', 'value')]
)
def update_union_dropdown(selected_district, selected_upazilla):
    unions = df[(df['District'] == selected_district) & (df['Upazilla'] == selected_upazilla)]['Union'].unique()
    return [{'label': union, 'value': union} for union in unions]

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('district-dropdown', 'value'),
     Input('upazilla-dropdown', 'value'),
     Input('union-dropdown', 'value'),
     Input('gender-radio', 'value'),
     Input('disability-card-radio', 'value')]
)
def update_bar_chart(selected_district, selected_upazilla, selected_union, selected_gender, selected_disability_card):
    
    # Filter by selected gender
    if selected_gender != 'All':
        filtered_df = df[df['Gender'] == selected_gender]
    else:
        filtered_df = df

    # Filter by selected disability card
    if selected_disability_card != 'All':
        filtered_df = filtered_df[df['Have a disability golden citizen card?'] == selected_disability_card]

    # If only District is selected
    if selected_upazilla is None and selected_union is None:
        filtered_df = filtered_df[filtered_df['District'] == selected_district]
        village_counts = filtered_df['Upazilla'].value_counts().reset_index()
        village_counts.columns = ['Upazilla', 'Village Count']
        fig = px.bar(village_counts, x='Upazilla', y='Village Count', color='Upazilla', 
                     title='Count of Villages per Upazilla',
                     labels={'Upazilla': 'Upazilla', 'Village Count': 'Number of Villages'},
                     height=400)
        return fig
    
    # If District and Upazilla are selected
    elif selected_union is None:
        filtered_df = filtered_df[(filtered_df['District'] == selected_district) & (filtered_df['Upazilla'] == selected_upazilla)]
        village_counts = filtered_df['Union'].value_counts().reset_index()
        village_counts.columns = ['Union', 'Village Count']
        fig = px.bar(village_counts, x='Union', y='Village Count', color='Union',
                     title='Count of Villages per Union',
                     labels={'Union': 'Union', 'Village Count': 'Number of Villages'},
                     height=400)
        return fig

    # If District, Upazilla, and Union are selected
    else:
        filtered_df = filtered_df[
            (filtered_df['District'] == selected_district) & 
            (filtered_df['Upazilla'] == selected_upazilla) & 
            (filtered_df['Union'] == selected_union)
        ]
        village_counts = filtered_df['Name of the village'].value_counts().reset_index()
        village_counts.columns = ['Name of the village', 'Count']
        fig = px.bar(village_counts, x='Name of the village', y='Count', color='Name of the village',
                     title='Data Count per Village in Selected Union',
                     labels={'Name of the village': 'Village', 'Count': 'Data Count'},
                     height=400)
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
