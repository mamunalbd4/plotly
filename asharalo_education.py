import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Load data from the URL
url = "https://raw.githubusercontent.com/mamunalbd4/asharalo/main/asharalofinal.csv"
data = pd.read_csv(url)

# Create the Dash App
app = dash.Dash(__name__)

# Define the available options for the dropdown
gender_options = [{'label': 'All', 'value': 'All'}] + [{'label': gender, 'value': gender} for gender in data['Gender'].unique()]
disability_options = [{'label': 'All', 'value': 'All'}] + [{'label': option, 'value': option} for option in data['Have a disability golden citizen card?'].unique()]

# Filter out "Not Applicable" values from the initial data
data_filtered = data[(data["Does the child / person go to school / study?"] != "Not Applicable") &
                     (data["Educational Qualification of the child / individual (Enter the class he / she is passing at last):"] != "Not Applicable") &
                     (data["If yes, what kind of school do you go to?"] != "Not Applicable") &
                     (data["Has the Children/Person get Education stipend "] != "Not Applicable")]

app.layout = html.Div([
    html.H1(
        "Ashar Alo Project Education Summary",
        style={'text-align': 'center', 'margin-top': '20px'}),  # Center the heading horizontally and add margin at the top

    html.Div([
        html.Label("Filter by Gender:"),
        dcc.Dropdown(
            id='gender-dropdown',
            options=gender_options,
            value='All'
        ),
    ], style={'width': '45%', 'display': 'inline-block', 'margin-top': '20px', 'margin-left': '10%'}),

    html.Div([
        html.Label("Filter by Disability/Golden Citizen Card:"),
        dcc.Dropdown(
            id='disability-dropdown',
            options=disability_options,
            value='All'
        ),
    ], style={'width': '45%', 'display': 'inline-block', 'margin-top': '20px'}),

    dcc.Graph(
        id='school-bar-chart',
        style={'margin-top': '20px'}
    ),

    dcc.Graph(
        id='qualification-pie-chart',
        style={'margin-top': '20px'}
    ),

    dcc.Graph(
        id='school-type-bar-chart',
        style={'margin-top': '20px'}
    ),

    dcc.Graph(
        id='stipend-bar-chart',
        style={'margin-top': '20px'}
    ),

    dcc.Graph(
        id='stipend-pie-chart',
        style={'margin-top': '20px'}
    )
])

# Create a callback to update all charts based on the selected options
@app.callback(
    [Output('school-bar-chart', 'figure'),
     Output('qualification-pie-chart', 'figure'),
     Output('school-type-bar-chart', 'figure'),
     Output('stipend-bar-chart', 'figure'),
     Output('stipend-pie-chart', 'figure')],
    [Input('gender-dropdown', 'value'),
     Input('disability-dropdown', 'value')]
)
def update_charts(selected_gender, selected_disability):
    # Filter data based on selected options and exclude "Not Applicable"
    filtered_data = data_filtered.copy()
    
    if selected_gender != 'All':
        filtered_data = filtered_data[filtered_data['Gender'] == selected_gender]
    
    if selected_disability != 'All':
        filtered_data = filtered_data[filtered_data['Have a disability golden citizen card?'] == selected_disability]

    # Recalculate counts for all charts
    school_counts = filtered_data["Does the child / person go to school / study?"].value_counts()
    qualification_counts = filtered_data["Educational Qualification of the child / individual (Enter the class he / she is passing at last):"].value_counts()
    school_type_counts = filtered_data["If yes, what kind of school do you go to?"].value_counts()
    stipend_counts = filtered_data["Has the Children/Person get Education stipend "].value_counts()

    # Create figures for all charts
    school_bar_chart = {
        'data': [{'x': school_counts.index, 'y': school_counts.values, 'type': 'bar', 'name': 'School Attendance'}],
        'layout': {'title': 'Does the child/person go to school/study?'}
    }

    qualification_pie_chart = {
        'data': [{'labels': qualification_counts.index, 'values': qualification_counts.values, 'type': 'pie', 'name': 'Educational Qualification'}],
        'layout': {'title': 'Educational Qualification of the child/individual'}
    }

    school_type_bar_chart = {
        'data': [{'x': school_type_counts.index, 'y': school_type_counts.values, 'type': 'bar', 'name': 'School Type'}],
        'layout': {'title': 'Types of Schools Attended'}
    }

    stipend_bar_chart = {
        'data': [{'x': stipend_counts.index, 'y': stipend_counts.values, 'type': 'bar', 'name': 'Stipend Status'}],
        'layout': {'title': 'Education Stipend Status'}
    }

    stipend_pie_chart = {
        'data': [{'labels': stipend_counts.index, 'values': stipend_counts.values, 'type': 'pie', 'name': 'Stipend Status'}],
        'layout': {'title': 'Education Stipend Status'}
    }

    return school_bar_chart, qualification_pie_chart, school_type_bar_chart, stipend_bar_chart, stipend_pie_chart

if __name__ == '__main__':
    app.run_server(debug=True)
