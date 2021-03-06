import os
import dash
import dash_html_components as html
import dash_table
import dash_core_components as dcc
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

bc_beers_exploration = pd.read_csv("bc_beers_final.csv", index_col=0)
beers = bc_beers_exploration['Beer name_x'].unique()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.H2('BC Beer Recommender System'),
    html.Div('''
    Once I moved to BC, I was overwhelmed by the number of beer brands available.
    I have always been a beer enthusiast and love to try new beers, but it was so hard to keep it up with the innovations and that is what motivated me to create a beer recommender system using deep learning.
    '''),
    html.Div('''
    The primary goal of this project was to create an engine that would learn from data about the beers, existing users and recommend beers to those users based on their preferences. I used a neural network model for that.
    
    The second goal was to be able to learn about the beers and their features to recommend to new users (cold start).
    '''),
    html.H6("Here is the result of this project! Go ahead and select one of your favourite beers and check what the model recommends based on what it learned from data."),
    dcc.Dropdown(
        id='beer_input',
        options=[{'label': v, 'value': v} for v in beers],
        value='Bavarian Copper Bock'
    ),
    html.Div(id='dd-output-container'),
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('beer_input', 'value')])
def update_output(value):
    temp = find_similarity(value)
    return  dash_table.DataTable(
        data=temp.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in temp.columns],
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'},
        dropdown={

            'Recommendation': {
                'options': [
                    {'label': i, 'value': i}
                    for i in temp['Recommendation'].unique()
                ]
            }
        }
    )


def find_similarity(beerInput):
    cosine_list = []
    beer_name1 = []
    beer_name2 = []
    beer_brewery_list = []
    beer_style_list = []
    beer_abv_list = []

    for i in range(0, bc_beers_exploration.shape[0]):
        tent1 = bc_beers_exploration.iloc[i, 10:60]
        tent2 = bc_beers_exploration[bc_beers_exploration["Beer name_x"] == beerInput]
        tent3 = tent2.iloc[0, 10:60]
        cosine = np.dot(tent3, tent1)

        beer1 = tent2.iloc[0, 1]
        beer2 = bc_beers_exploration.iloc[i, 1]
        beer_brewery = bc_beers_exploration.iloc[i, 2]
        beer_style = bc_beers_exploration.iloc[i, 3]
        beer_abv = bc_beers_exploration.iloc[i, 4]
        cosine_list.append(cosine)
        beer_name1.append(beer1)
        beer_name2.append(beer2)
        beer_brewery_list.append(beer_brewery)
        beer_style_list.append(beer_style)
        beer_abv_list.append(beer_abv)

    cosine_df = pd.DataFrame({"Beer": beer_name1, "Recommendation": beer_name2, "Brewery": beer_brewery_list, "Style": beer_style_list,"ABV": beer_abv_list, "Match": cosine_list})
    cosine_df = cosine_df.sort_values(by="Match", ascending=False)
    cosine_df["Match"] = cosine_df["Match"].round(decimals = 2)
    return cosine_df.iloc[1:10,1:]


if __name__ == '__main__':
    app.run_server(debug=True)