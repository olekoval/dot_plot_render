#!/usr/bin/env python

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Завантаження даних
df = pd.read_csv('ehr_684rows.csv')

# Ініціалізація додатка Dash
app = Dash(__name__)

# Оформлення макету
app.layout = html.Div([
    html.H1(children='Dot plot', style={'textAlign':'center'}),
    dcc.Dropdown([0.25, 0.50, 0.75, 1], 1, id='percent-dropdown'),
    dcc.Graph(id='dot-plot-content'),
    html.H1(children='Box plot', style={'textAlign':'center'}),
    dcc.Graph(id='box-plot-content')
])

# Callback для оновлення графіків
@callback(
    [Output('dot-plot-content', 'figure'),
     Output('box-plot-content', 'figure')],
    Input('percent-dropdown', 'value')
)
def update_graphs(value):
    dff = df.sample(frac=value)
    
    # Обчислення кількості для віку (dot plot)
    dff['Count_вік'] = dff.groupby('Вік').cumcount() + 1
    mx = dff['Count_вік'].max()
    mx_age = dff['Вік'].max()
    mn_age = dff['Вік'].min()

    # Створення dot plot
    dot_fig = px.scatter(dff, x='Вік', y='Count_вік')
    dot_fig.update_traces(marker=dict(size=10 + (1 / value)))
    dot_fig.update_yaxes(tickmode='linear', dtick=1)
    dot_fig.update_yaxes(range=[0, mx + 1])
    dot_fig.update_xaxes(range=[mn_age - 1, mx_age + 1])

    # Створення box plot
    box_fig = go.Figure()
    box_fig.add_trace(go.Box(x=dff['Вік']))
    box_fig.update_xaxes(range=[mn_age - 1, mx_age + 1])

    return dot_fig, box_fig

# Зазначаємо сервер
server = app.server

# Запуск додатка
if __name__ == '__main__':
    app.run_server(debug=True)
