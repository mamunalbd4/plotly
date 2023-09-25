import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import dash_table
import pandas as pd
from dash.dependencies import Input, Output

# Load the CSV data
url = "https://raw.githubusercontent.com/mamunalbd4/asharalo/main/asharalofinal.csv"
df = pd.read_csv(url)

# Initialize the Dash app
app = dash.Dash(__name__)

# Create unique lists for District, Upazilla, Union, and Name of the village
districts = df['District'].unique()
upazilas = df['Upazilla'].unique()
unions = df['Union'].unique()
villages = df['Name of the village'].unique()

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H1("Ashar Alo project location-wise personal information", style={'text-align': 'center'}),
        html.H3("District, Upazilla, Union", style={'text-align': 'center'}),
        html.Div(id='data-count', style={'text-align': 'center', 'font-weight': 'bold', 'margin-top': '10px'}),
        
        html.Div([
            html.H4("Age Range", style={'text-align': 'center', 'color': 'blue'}),
            dcc.RangeSlider(
                id='age-slider',
                marks={i: str(i) for i in range(0, 101, 10)},
                min=0,
                max=100,
                step=1,
                value=[0, 100]
            ),
            
        ], style={'margin': '20px'}),
        
        html.Div([
            dcc.RadioItems(
                id='gender-radio',
                options=[
                    {'label': 'All Genders', 'value': 'All'},
                    {'label': 'Male', 'value': 'Male'},
                    {'label': 'Female', 'value': 'Female'},
                    {'label': 'Other', 'value': 'Other'}
                ],
                value='All',
                labelStyle={'display': 'block', 'text-align': 'center', 'margin-top': '10px'}  # Center-align labels
            )
        ], style={'text-align': 'center'}),  # Center-align the radio buttons
        
        dcc.Dropdown(
            id='district-dropdown',
            options=[{'label': district, 'value': district} for district in districts],
            multi=True,
            value=[]
        ),
        
        dcc.Dropdown(
            id='upazilla-dropdown',
            multi=True,
            value=[]
        ),
        
        dcc.Dropdown(
            id='union-dropdown',
            multi=True,
            value=[]
        ),
        
        dcc.Dropdown(
            id='village-dropdown',
            multi=True,
            value=[]
        ),
        
        dash_table.DataTable(
            id='datatable',
            columns=[
                {"name": "Name of child / person", "id": "Name of child / person"},
                {"name": "Age", "id": "Age"},
                {"name": "Father's name of the child / person", "id": "Father's name of the child / person"},
                {"name": "Mother name of the child / person", "id": "Mother name of the child / person"},
                {"name": "Gender", "id": "Gender"},
                {"name": "District", "id": "District"},
                {"name": "Upazilla", "id": "Upazilla"},
                {"name": "Union", "id": "Union"},
                {"name": "Name of the village", "id": "Name of the village"},
            ],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
        ),
    ], style={'margin': 'auto', 'max-width': '800px'}),  # Center-align the container
])

# Callbacks to update dropdown options based on selection, age range, and gender
@app.callback(
    Output('upazilla-dropdown', 'options'),
    Input('district-dropdown', 'value')
)
def update_upazilla_options(selected_districts):
    filtered_df = df[df['District'].isin(selected_districts)]
    return [{'label': upazilla, 'value': upazilla} for upazilla in filtered_df['Upazilla'].unique()]

@app.callback(
    Output('union-dropdown', 'options'),
    Input('upazilla-dropdown', 'value')
)
def update_union_options(selected_upazillas):
    filtered_df = df[df['Upazilla'].isin(selected_upazillas)]
    return [{'label': union, 'value': union} for union in filtered_df['Union'].unique()]

@app.callback(
    Output('village-dropdown', 'options'),
    Input('union-dropdown', 'value')
)
def update_village_options(selected_unions):
    filtered_df = df[df['Union'].isin(selected_unions)]
    return [{'label': village, 'value': village} for village in filtered_df['Name of the village'].unique()]

# Callback to update the table based on dropdown selections, age range, and gender
@app.callback(
    Output('datatable', 'data'),
    Output('data-count', 'children'),
    Input('district-dropdown', 'value'),
    Input('upazilla-dropdown', 'value'),
    Input('union-dropdown', 'value'),
    Input('village-dropdown', 'value'),
    Input('age-slider', 'value'),
    Input('gender-radio', 'value')
)
def update_table(selected_districts, selected_upazillas, selected_unions, selected_villages, age_range, selected_gender):
    min_age, max_age = age_range
    filtered_df = df[
        (df['District'].isin(selected_districts)) &
        (df['Upazilla'].isin(selected_upazillas)) &
        (df['Union'].isin(selected_unions)) &
        (df['Name of the village'].isin(selected_villages)) &
        (df['Age'] >= min_age) &
        (df['Age'] <= max_age)
    ]
    
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    data_count = len(filtered_df)
    data_count_text = f"Total Data Records: {data_count}"
    
    return filtered_df.to_dict('records'), data_count_text

if __name__ == '__main__':
    app.run_server(debug=True)
