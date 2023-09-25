import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

# 1. Load the data
data = pd.read_csv('https://raw.githubusercontent.com/mamunalbd4/asharalo/main/asharalofinal.csv')

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

chart_height = 600

# 9. Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Ashar Alo Project Income Situation", style={'textAlign': 'center'}),

    # Gender Dropdown Label with center alignment
    html.Div(
        html.Label("Select Gender:", style={'textAlign': 'center'}),
        style={'textAlign': 'center'}
    ),
    
    # Gender Dropdown
    html.Div([
        dcc.Dropdown(
            id='gender-dropdown',
            options=[
                {'label': 'Male', 'value': 'Male'},
                {'label': 'Female', 'value': 'Female'},
                {'label': 'Others', 'value': 'Others'},
                {'label': 'All', 'value': 'All'}
            ],
            value='All',
            clearable=False,
            style={'width': '50%', 'margin': '20px auto'}
        )
    ]),

    # "Have a disability golden citizen card?" Dropdown Label with center alignment
    html.Div(
        html.Label("Have a disability golden citizen card?", style={'textAlign': 'center'}),
        style={'textAlign': 'center'}
    ),

    # "Have a disability golden citizen card?" Dropdown
    html.Div([
        dcc.Dropdown(
            id='disability-dropdown',
            options=[
                {'label': 'Yes', 'value': 'Yes'},
                {'label': 'No', 'value': 'No'},
                {'label': 'All', 'value': 'All'}
            ],
            value='All',
            clearable=False,
            style={'width': '50%', 'margin': '20px auto'}
        )
    ]),

    # Bar chart: Main Occupation of the Family
    dcc.Graph(id='occupation-bar-chart', figure={}),

    # "Family monthly income?" Pie Chart
    dcc.Graph(id='family-income-pie-chart', figure={}),

    # Bar chart: Grouped by Occupation and Monthly Income
    dcc.Graph(id='grouped-bar-chart', figure={}),

    # Bar chart: Grouped by Occupation and Sum of Total number of family members
    dcc.Graph(id='occupation-total-members-bar-chart', figure={}),

    # ... [Other components go here, same as your initial code]

])

@app.callback(
    Output('family-income-pie-chart', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('disability-dropdown', 'value')
)
def update_family_income_pie_chart(selected_gender, selected_disability):
    if selected_gender != 'All':
        filtered_data = data[data['Gender'] == selected_gender]
    else:
        filtered_data = data.copy()
    
    if selected_disability != 'All':
        filtered_data = filtered_data[filtered_data['Have a disability golden citizen card?'] == selected_disability]
    
    income_counts = filtered_data['Family monthly income?'].value_counts()
    
    return {
        'data': [
            go.Pie(
                labels=income_counts.index,
                values=income_counts.values,
                marker={'colors': colors},
                textinfo='percent+label',
                hole=0.3
            )
        ],
        'layout': go.Layout(
            title='Distribution of Family Monthly Income',
            height=chart_height
        )
    }

@app.callback(
    Output('occupation-bar-chart', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('disability-dropdown', 'value')
)
def update_occupation_chart(selected_gender, selected_disability):
    if selected_gender != 'All':
        filtered_data = data[data['Gender'] == selected_gender]
    else:
        filtered_data = data.copy()
    
    if selected_disability != 'All':
        filtered_data = filtered_data[filtered_data['Have a disability golden citizen card?'] == selected_disability]
    
    occupation_counts = filtered_data['Specify the main occupation of the family'].value_counts()

    return {
        'data': [
            go.Bar(
                x=occupation_counts.index,
                y=occupation_counts.values,
                marker={'color': colors}
            )
        ],
        'layout': go.Layout(
            title='Main Occupation of Families',
            xaxis={'title': 'Occupation'},
            yaxis={'title': 'Count'},
            hovermode='closest',
            height=chart_height
        )
    }

@app.callback(
    Output('grouped-bar-chart', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('disability-dropdown', 'value')
)
def update_grouped_bar_chart(selected_gender, selected_disability):
    if selected_gender != 'All':
        filtered_data = data[data['Gender'] == selected_gender]
    else:
        filtered_data = data.copy()
    
    if selected_disability != 'All':
        filtered_data = filtered_data[filtered_data['Have a disability golden citizen card?'] == selected_disability]
    
    grouped_data = filtered_data.groupby(['Specify the main occupation of the family', 'Family monthly income?']).size().reset_index(name='Count')
    
    return px.bar(grouped_data, x='Specify the main occupation of the family', y='Count', color='Family monthly income?', barmode='group')

@app.callback(
    Output('occupation-total-members-bar-chart', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('disability-dropdown', 'value')
)
def update_occupation_total_members_chart(selected_gender, selected_disability):
    if selected_gender != 'All':
        filtered_data = data[data['Gender'] == selected_gender]
    else:
        filtered_data = data.copy()
    
    if selected_disability != 'All':
        filtered_data = filtered_data[filtered_data['Have a disability golden citizen card?'] == selected_disability]
    
    occupation_total_members = filtered_data.groupby('Specify the main occupation of the family')['Total number of family members'].sum().reset_index()
    
    return {
        'data': [
            go.Bar(
                x=occupation_total_members['Specify the main occupation of the family'],
                y=occupation_total_members['Total number of family members'],
                marker={'color': colors}
            )
        ],
        'layout': go.Layout(
            title='Sum of Total Number of Family Members by Occupation',
            xaxis={'title': 'Occupation'},
            yaxis={'title': 'Total Number of Family Members'},
            hovermode='closest',
            height=chart_height
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
