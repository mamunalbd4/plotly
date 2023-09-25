import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd

# Load data from the CSV file
url = 'https://raw.githubusercontent.com/mamunalbd4/asharalo/main/asharalofinal.csv'
df = pd.read_csv(url)

# Filter out rows with blank values in the 'Person's monthly income?' column
df = df.dropna(subset=["Person's monthly income?"], how="any")

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app with center-aligned dropdown menus and CSS styling
app.layout = html.Div([
    html.H1("Person Income Situation", style={'textAlign': 'center'}),  # Center-align the header
    
    # Center-aligned div for "gender" dropdown
    html.Div([
        html.Label("Select gender:", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='gender-dropdown',
            options=[
                {'label': 'All', 'value': 'All'},  # Default option
                {'label': 'Male', 'value': 'Male'},
                {'label': 'Female', 'value': 'Female'},
                {'label': 'Other', 'value': 'Other'}
            ],
            value='All',  # Default value
        ),
    ], style={'text-align': 'center'}),
    
    # Center-aligned div for "Have a disability golden citizen card?" dropdown
    html.Div([
        html.Label("Have a disability golden citizen card?", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='disability-dropdown',
            options=[
                {'label': 'All', 'value': 'All'},  # Default option
                {'label': 'Yes', 'value': 'Yes'},
                {'label': 'No', 'value': 'No'}
            ],
            value='All',  # Default value
        ),
    ], style={'text-align': 'center'}),
    
    # Center-aligned div for "Is the person Skilled?" dropdown
    html.Div([
        html.Label("Is the person Skilled?", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='skilled-dropdown',
            options=[
                {'label': 'All', 'value': 'All'},  # Default option
                {'label': 'Yes', 'value': 'Yes'},
                {'label': 'No', 'value': 'No'}
            ],
            value='All',  # Default value
        ),
    ], style={'text-align': 'center'}),
    
    dcc.Graph(id='income-sum-count-bar-chart'),  # Bar chart for income section
    
    html.H2("Person's Occupation", style={'textAlign': 'center'}),  # Center-align the occupation header
    
    dcc.Graph(id='occupation-pie-chart'),  # Pie chart for occupation section
    
    html.H2("Age for Occ", style={'textAlign': 'center'}),  # Center-align the age header
    
    dcc.Graph(id='age-for-occ-bar-chart'),  # Bar chart for age section
    
    html.H2("Occupation Table", style={'textAlign': 'center'}),  # Center-align the table header
    
    # DataTable for occupation table
    dash_table.DataTable(
        id='occupation-table',
        columns=[
            {"name": "Occupation", "id": "Occupation"},
            {"name": "Income Category", "id": "Income Category"},
            {"name": "Total Count", "id": "Total Count"},
        ],
        style_table={'overflowX': 'scroll'},
    ),
])

# Define callback to update the bar chart for income based on dropdown values
@app.callback(
    Output('income-sum-count-bar-chart', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('disability-dropdown', 'value'),
    Input('skilled-dropdown', 'value')
)
def update_income_bar_chart(selected_gender, selected_disability, selected_skilled):
    filtered_df = df.copy()
    
    # Apply filter based on selected gender, but ignore 'All'
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    # Apply filter based on selected disability status, but ignore 'All'
    if selected_disability != 'All':
        filtered_df = filtered_df[filtered_df['Have a disability golden citizen card?'] == selected_disability]
    
    # Apply filter based on selected skilled status, but ignore 'All'
    if selected_skilled != 'All':
        filtered_df = filtered_df[filtered_df['Is the person Skilled?'] == selected_skilled]
    
    # Recalculate the sum of counts for the filtered data
    filtered_sum_count_df = filtered_df.groupby(["Person's monthly income?"]).size().reset_index(name='Sum of Counts')
    
    # Create and return the updated income bar chart
    income_bar_chart_fig = px.bar(
        filtered_sum_count_df,
        x="Person's monthly income?",
        y='Sum of Counts',
        title="Income Distribution",
        color="Person's monthly income?"
    )
    
    return income_bar_chart_fig

# Define callback to update the pie chart for occupation based on dropdown values
@app.callback(
    Output('occupation-pie-chart', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('disability-dropdown', 'value'),
    Input('skilled-dropdown', 'value')
)
def update_occupation_pie_chart(selected_gender, selected_disability, selected_skilled):
    filtered_df = df.copy()
    
    # Apply filter based on selected gender, but ignore 'All'
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    # Apply filter based on selected disability status, but ignore 'All'
    if selected_disability != 'All':
        filtered_df = filtered_df[filtered_df['Have a disability golden citizen card?'] == selected_disability]
    
    # Apply filter based on selected skilled status, but ignore 'All'
    if selected_skilled != 'All':
        filtered_df = filtered_df[filtered_df['Is the person Skilled?'] == selected_skilled]
    
    # Filter out rows with blank values in the 'Person's occupation?' column
    filtered_df = filtered_df.dropna(subset=["Person's occupation?"], how="any")
    
    # Calculate the count of each occupation
    occupation_count_df = filtered_df['Person\'s occupation?'].value_counts().reset_index()
    occupation_count_df.columns = ['Occupation', 'Count']
    
    # Create and return the occupation pie chart
    occupation_pie_chart_fig = px.pie(
        occupation_count_df,
        names='Occupation',
        values='Count',
        title="Occupation Distribution",
    )
    
    return occupation_pie_chart_fig

# Define callback to update the bar chart for age based on dropdown values
@app.callback(
    Output('age-for-occ-bar-chart', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('disability-dropdown', 'value'),
    Input('skilled-dropdown', 'value')
)
def update_age_for_occ_bar_chart(selected_gender, selected_disability, selected_skilled):
    filtered_df = df.copy()
    
    # Apply filter based on selected gender, but ignore 'All'
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    # Apply filter based on selected disability status, but ignore 'All'
    if selected_disability != 'All':
        filtered_df = filtered_df[filtered_df['Have a disability golden citizen card?'] == selected_disability]
    
    # Apply filter based on selected skilled status, but ignore 'All'
    if selected_skilled != 'All':
        filtered_df = filtered_df[filtered_df['Is the person Skilled?'] == selected_skilled]
    
    # Filter out rows with blank values in the 'Age for Occ' column
    filtered_df = filtered_df.dropna(subset=["Age for Occ"], how="any")
    
    # Recalculate the sum of counts for the filtered data
    age_for_occ_sum_count_df = filtered_df.groupby(["Age for Occ"]).size().reset_index(name='Sum of Counts')
    
    # Create and return the age for occupation bar chart
    age_for_occ_bar_chart_fig = px.bar(
        age_for_occ_sum_count_df,
        x="Age for Occ",
        y='Sum of Counts',
        title="Age for Occupation Distribution",
        color="Age for Occ",
    )
    
    return age_for_occ_bar_chart_fig

# Define callback to update the occupation table based on dropdown values
@app.callback(
    Output('occupation-table', 'data'),
    Input('gender-dropdown', 'value'),
    Input('disability-dropdown', 'value'),
    Input('skilled-dropdown', 'value')
)
def update_occupation_table(selected_gender, selected_disability, selected_skilled):
    filtered_df = df.copy()
    
    # Apply filter based on selected gender, but ignore 'All'
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    # Apply filter based on selected disability status, but ignore 'All'
    if selected_disability != 'All':
        filtered_df = filtered_df[filtered_df['Have a disability golden citizen card?'] == selected_disability]
    
    # Apply filter based on selected skilled status, but ignore 'All'
    if selected_skilled != 'All':
        filtered_df = filtered_df[filtered_df['Is the person Skilled?'] == selected_skilled]
    
    # Filter out rows with blank values in the 'Person's occupation?' and 'Person's monthly income?' columns
    filtered_df = filtered_df.dropna(subset=["Person's occupation?", "Person's monthly income?"], how="any")
    
    # Group by both 'Person's occupation?' and 'Person's monthly income?' and calculate the total count
    occupation_table_df = filtered_df.groupby(["Person's occupation?", "Person's monthly income?"]).size().reset_index(name='Total Count')
    occupation_table_df.columns = ['Occupation', 'Income Category', 'Total Count']
    
    return occupation_table_df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
