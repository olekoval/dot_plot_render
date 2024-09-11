#!/usr/bin/env python

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Завантаження даних
df = pd.read_csv('ehr_684rows.csv')

# Ініціалізація додатка Dash
app = Dash(__name__)

# Оформлення макету
app.layout = html.Div([
    html.H1(children='Dot plot', style={'textAlign':'center'}),
    dcc.Graph(id='graph-content')
])

# Callback для оновлення графіку
@callback(
    Output('graph-content', 'figure'),
    Input('graph-content', 'id')  # Додаємо Input для активації callback
)
def dot(_):  # Параметр "_" щоб позначити невикористаний Input
    # Обчислення кількості для віку
    df['Count_вік'] = df.groupby('Вік').cumcount() + 1  # !!! 
    mx = df['Count_вік'].max()
    mx_age = df['Вік'].max()
    mn_age = df['Вік'].min()

    # Створення графіку
    fig = px.scatter(df, x='Вік', y='Count_вік')
    # Настройка розміру точок
    fig.update_traces(marker=dict(size=10)) 
    # Настройка осі Y для відображення лише цілих чисел
    fig.update_yaxes(tickmode='linear', dtick=1)
    # Настройка діапазону значень осі Y
    fig.update_yaxes(range=[0, mx + 1])
    # Настройка діапазону значень осі X
    fig.update_xaxes(range=[mn_age - 1, mx_age + 1])

    return fig
    
# Зазначаємо сервер
server = app.server
# Запуск додатка
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




