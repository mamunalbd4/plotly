import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load the CSV data into a Pandas DataFrame
url = 'https://raw.githubusercontent.com/mamunalbd4/asharalo/main/asharalofinal.csv'
df = pd.read_csv(url)

# Define the categories based on the corrected column names
categories = [
    "Has the Children/Person get Disability/Other Allowens",
    "Has the Children/Person get Education stipend ",
    "Has the Children/Person get Health sevices ( Govt./ Non- Govt. )",
    "Has the Children/Person get Training service",
    "Has the Children/Person get Rehabilitation allowance ",
    "Has the Children/Person get Rehabilition Service (Govt. or Private)",
    "In health rehabilitation service did you get Asisstive devices?",
    "In health rehabilitation service did you get Therapy",
    "In health rehabilitation service did you get Operation",
    "In health rehabilitation service did you get Both (Asisstive device and Therapy) "
]

# Initialize the Dash app
app = dash.Dash(__name__)
server=app.server

# Define the layout of the Dash app with CSS styling for center alignment
app.layout = html.Div([
    html.Div(
        html.H1("Allowance and Services Provide Information", style={'textAlign': 'center'}),
        style={'margin-top': '20px'}
    ),
    *[dcc.Graph(
        id=f'pie-chart-{category}',
        figure={
            'data': [
                {
                    'labels': ['Yes', 'No'],
                    'values': [df[category].value_counts().get('Yes', 0), df[category].value_counts().get('No', 0)],
                    'type': 'pie'
                }
            ],
            'layout': {
                'title': f'Distribution of {category}'
            }
        }
    ) for category in categories]
])

if __name__ == '__main__':
    app.run_server(debug=True)
