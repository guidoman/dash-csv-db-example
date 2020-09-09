import io

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine, text

from my_db import my_data, db_file_name

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

engine = create_engine(f'sqlite:///{db_file_name}', echo=True)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('date-dropdown', 'value')])
def create_graph(yyyymmdd):
    with engine.connect() as conn:
        # Select record matching date
        sel = my_data.select().where(my_data.c.yyyymmdd == yyyymmdd)
        csv = conn.execute(sel).fetchone()[1]
        # Read string as Pandas dataframe
        strbuf = io.StringIO(csv)
        csv_df = pd.read_csv(strbuf)
        # Create a scatter plot with data from the dataframe
        return go.Figure(data=go.Scatter(x=csv_df.x, y=csv_df.y, mode='markers'))


def app_layout():
    csv_dates = get_dates()

    return html.Div(children=[
        html.H1(children='Dash + DB (Sqlite) + SqlAlchemy + CSV'),

        html.Div(children='''
        In this example, you store data in a DB as CSV text. Each CSV is identified by its date (unique ID).
        You select a date from the dropdown and the plot is updated with data read from the DB.
        Interaction with the DB is implemented with SqlAlchemy.  
    '''),

        html.Br(),

        dcc.Dropdown(
            id='date-dropdown',
            options=[{'label': date, 'value': date} for date in csv_dates],
            value=csv_dates[0] if len(csv_dates) else None

        ),
        html.Div(id='dd-output-container'),
        dcc.Graph(
            id='example-graph',
            figure=None
        ),
    ])


def get_dates():
    with engine.connect() as conn:
        result = conn.execute(text('SELECT distinct(yyyymmdd) FROM my_data order by yyyymmdd asc'))
        return [row[0] for row in result]


app.layout = app_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
