import functions as func
import data_base_15
import data_base_16
import data_base_17
import data_base_18
import data_base_19

from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import sqlite3 as sql

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.title = 'World Happiness'

con = sql.connect('fifteen.db')
sql_query_15 = pd.read_sql("SELECT * from fifteen_tbl", con)
df15 = pd.DataFrame(sql_query_15, columns=['Country', 'Region', 'Happiness Rank', 'Happiness Score', 'Standard Error',
                                        'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 'Freedom',
                                        'Trust (Government Corruption)', 'Generosity', 'Dystopia Residual'])
con.close()

con = sql.connect('sixteen.db')
sql_query_16 = pd.read_sql('SELECT * FROM sixteen_tbl', con)
df16 = pd.DataFrame(sql_query_16, columns=['Country', 'Region', 'Happiness Rank', 'Happiness Score',
                                           'Lower Confidence Interval', 'Upper Confidence Interval',
                                           'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 'Freedom',
                                           'Trust (Government Corruption)', 'Generosity', 'Dystopia Residual'])
con.close()

con = sql.connect('seventeen.db')
sql_query_17 = pd.read_sql('SELECT * FROM seventeen_tbl', con)
df17 = pd.DataFrame(sql_query_17, columns=['Country', 'Happiness.Rank', 'Happiness.Score', 'Whisker.high',
                                           'Whisker.low', 'Economy..GDP.per.Capita.', 'Family',
                                           'Health..Life.Expectancy.', 'Freedom', 'Generosity',
                                           'Trust..Government.Corruption.', 'Dystopia.Residual'])
con.close()

con = sql.connect('eighteen.db')
sql_query_18 = pd.read_sql('SELECT * FROM eighteen_tbl', con)
df18 = pd.DataFrame(sql_query_18, columns=['Overall rank', 'Country or region', 'Score', 'GDP per capita',
                                           'Social support', 'Healthy life expectancy', 'Freedom to make life choices',
                                           'Generosity', 'Perceptions of corruption'])
con.close()

con = sql.connect('nineteen.db')
sql_query_19 = pd.read_sql('SELECT * FROM nineteen_tbl', con)
df19 = pd.DataFrame(sql_query_19, columns=['Overall rank', 'Country or region', 'Score', 'GDP per capita',
                                           'Social support', 'Healthy life expectancy', 'Freedom to make life choices',
                                           'Generosity', 'Perceptions of corruption'])
con.close()

func.create_region_column(df17, df15, 'Country')
func.create_region_column(df18, df15, 'Country or region')
func.create_region_column(df19, df15, 'Country or region')

df17 = df17.rename(columns={
    'Happiness.Rank': 'Happiness Rank', 'Happiness.Score': 'Happiness Score',
    'Economy..GDP.per.Capita.': 'Economy (GDP per Capita)',
    'Health..Life.Expectancy.': 'Health (Life Expectancy)',
    'Trust..Government.Corruption.': 'Trust (Government Corruption)'
})

df18 = df18.rename(columns={
    'Overall rank': 'Happiness Rank', 'Country or region': 'Country', 'Score': 'Happiness Score',
    'GDP per capita': 'Economy (GDP per Capita)',
    'Social support': 'Family', 'Healthy life expectancy': 'Health (Life Expectancy)',
    'Freedom to make life choices': 'Freedom',
    'Perceptions of corruption': 'Trust (Government Corruption)'
})
df19 = df19.rename(columns={
    'Overall rank': 'Happiness Rank', 'Country or region': 'Country', 'Score': 'Happiness Score',
    'GDP per capita': 'Economy (GDP per Capita)',
    'Social support': 'Family', 'Healthy life expectancy': 'Health (Life Expectancy)',
    'Freedom to make life choices': 'Freedom',
    'Perceptions of corruption': 'Trust (Government Corruption)'
})

dfs = [df15, df16, df17, df18, df19]
df = pd.concat(dfs)
df = df.drop(columns=['Standard Error', 'Dystopia Residual', 'Lower Confidence Interval',
                      'Upper Confidence Interval', 'Whisker.high', 'Whisker.low', 'Dystopia.Residual'])

df = df.reset_index()

CHARTS_TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family='Century Gothic',
                  size=14)
    )
)

year_selector = dcc.Dropdown(
    id='year-selector',
    options=['2015', '2016', '2017', '2018', '2019', 'all'],
    value='2015',
    style={'marginTop': 5},
    clearable=False
)

type_selector = dcc.Dropdown(
    id='type-selector',
    options=['Country', 'Region'],
    value='Region',
    style={'marginTop': 10},
    clearable=False
)

tab1_content = [dbc.Row([
    html.H3('Region/Country ~ Happiness Score'),
    type_selector
], style={'paddingTop': 20}),

    dbc.Row([
        html.Div(id='type-chart')
    ])
]

tab2_content = [dbc.Row(html.Div(id='data-table'), style={'marginTop': 20})]

tab3_content = [dbc.Row(html.Div(id='health-economy-chart'), style={'marginTop': 15}),
                dbc.Row(html.Div(id='happiness-corruption chart'))]

app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(html.H1('World Happiness report visualization'), style={'marginTop': 20}),
            dbc.Col(
                html.Img(src=app.get_asset_url('images/happy-icon.jpg'),
                         style={'width': '100px'}), width={'size': 1}
            )
        ])
    ], className='app-header'),

    html.Div([
        dbc.Row([
            dbc.Col([
                html.H2('Choose year'),
                year_selector
            ]),
            dbc.Col(dbc.Button('Apply', id='submit-val', n_clicks=0, className='me-2'),
                    style={'marginTop': 45})
        ], className='year-selector-row'),

        dbc.Row([
            html.Div([
                dbc.Tabs([
                    dbc.Tab(tab1_content, label='Main Graph'),
                    dbc.Tab(tab2_content, label='Data'),
                    dbc.Tab(tab3_content, label='Another Graphs')
                ])
            ])])
    ], className='app-body')
])


@app.callback(
    Output(component_id='type-chart', component_property='children'),
    Output(component_id='health-economy-chart', component_property='children'),
    Output(component_id='happiness-corruption chart', component_property='children'),
    Output(component_id='data-table', component_property='children'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    State(component_id='year-selector', component_property='value'),
    Input(component_id='type-selector', component_property='value')

)
def update_graph(n, year_chosen, type_chosen):
    def create_main_graph(data_frame):
        fig1 = px.histogram(data_frame, x=type_chosen, y='Happiness Score', histfunc='avg', text_auto=True,
                            height=500)
        fig1.update_layout(template=CHARTS_TEMPLATE)
        fig1.update_xaxes(automargin=True)
        html1 = [dcc.Graph(figure=fig1)]
        return html1

    def create_health_economy_graph(data_frame):
        fig2 = px.scatter(data_frame, x='Economy (GDP per Capita)', y='Health (Life Expectancy)',
                          size='Happiness Score', color='Region', hover_name='Country', size_max=60)
        fig2.update_layout(template=CHARTS_TEMPLATE)
        html2 = [html.H4('Health ~ Economy'), dcc.Graph(figure=fig2)]
        return html2

    def create_happiness_corruption_graph(data_frame):
        fig3 = px.scatter(data_frame, x='Economy (GDP per Capita)', y='Trust (Government Corruption)', render_mode='markers',
                          color='Region')
        fig3.update_layout(template=CHARTS_TEMPLATE)
        html3 = [html.H4('Trust ~ Economy '), dcc.Graph(figure=fig3)]
        return html3

    def create_table(data_frame):
        tbl = dash_table.DataTable(data=data_frame.to_dict('records'),
                                   columns=[{"name": i, "id": i} for i in data_frame.columns],
                                   page_size=40,
                                   style_header={'textAlign': 'center', 'whiteSpace': 'normal', 'height': 'auto'},
                                   style_cell={'textAlign': 'left',
                                               'overflow': 'hidden',
                                               'textOverflow': 'ellipsis',
                                               'maxWidth': 0})
        html5 = [html.H4('Raw Data'), tbl]
        return html5

    if year_chosen == '2015':
        return create_main_graph(df15), create_health_economy_graph(df15), \
            create_happiness_corruption_graph(df15), create_table(df15)
    elif year_chosen == '2016':
        return create_main_graph(df16), create_health_economy_graph(df16), \
            create_happiness_corruption_graph(df16), create_table(df16)
    elif year_chosen == '2017':
        return create_main_graph(df17), create_health_economy_graph(df17), \
            create_happiness_corruption_graph(df17), create_table(df17)
    elif year_chosen == '2018':
        return create_main_graph(df18), create_health_economy_graph(df18), \
            create_happiness_corruption_graph(df18), create_table(df18)
    elif year_chosen == '2019':
        return create_main_graph(df19), create_health_economy_graph(df19), \
            create_happiness_corruption_graph(df19), create_table(df19)
    elif year_chosen == 'all':
        return create_main_graph(df), create_health_economy_graph(df), create_happiness_corruption_graph(df), \
            create_table(df)


if __name__ == '__main__':
    app.run_server(debug=True)
