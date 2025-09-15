# dashboard_app.py
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# ===== Load Data =====
df = pd.read_csv("data/recommendations/daily_price_recommendation.csv", parse_dates=['event_date'])
mapping_df = pd.read_csv("data/product_mapping.csv")

# Merge product names
df = df.merge(mapping_df, on='stock_code', how='left')

# ===== Dash App =====
app = dash.Dash(__name__)
app.title = "Dynamic Pricing Dashboard"

# ===== Layout =====
app.layout = html.Div(
    style={'backgroundColor': '#1b2a1f', 'color': 'white', 'font-family': 'Arial, sans-serif', 'padding': '20px'},
    children=[
        html.H1("Dynamic Pricing Dashboard", style={'textAlign': 'center', 'color': '#a0b394'}),
        
        html.Div([
            html.Label("Select Products:", style={'color': '#c0d6b5', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='product_dropdown',
                options=[{'label': name, 'value': code} for code, name in zip(mapping_df['stock_code'], mapping_df['product_name'])],
                multi=True,
                value=mapping_df['stock_code'][:5].tolist(),
                style={'backgroundColor': '#2f3e2f', 'color': '#a0b394', 'font-weight': 'bold'}
            )
        ], style={'margin-bottom': '25px', 'width': '50%'}),
        
        html.Div([
            html.Div([dcc.Graph(id='bar_chart')], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='line_chart')], style={'width': '48%', 'display': 'inline-block', 'float':'right'}),
        ], style={'margin-bottom': '25px'}),
        
        html.Div([
            html.Div([dcc.Graph(id='donut_chart')], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='scatter_chart')], style={'width': '48%', 'display': 'inline-block', 'float':'right'}),
        ], style={'margin-bottom': '25px'}),
        
        html.Div([
            html.Div([dcc.Graph(id='box_chart')], style={'width': '48%', 'display': 'inline-block'}),
        ])
    ]
)

# ===== Callbacks =====
@app.callback(
    Output('bar_chart', 'figure'),
    Output('line_chart', 'figure'),
    Output('donut_chart', 'figure'),
    Output('scatter_chart', 'figure'),
    Output('box_chart', 'figure'),
    Input('product_dropdown', 'value')
)
def update_charts(selected_products):
    filtered_df = df[df['stock_code'].isin(selected_products)]
    
    color_seq = px.colors.sequential.Viridis

    # Bar chart
    fig_bar = px.bar(
        filtered_df,
        x="event_date", y="daily_revenue",
        color="product_name",
        title="Daily Revenue",
        color_discrete_sequence=color_seq
    )
    fig_bar.update_layout(plot_bgcolor='#1b2a1f', paper_bgcolor='#1b2a1f', font_color='white')

    # Line chart
    fig_line = px.line(
        filtered_df,
        x="event_date", y="predicted_quantity",
        color="product_name",
        title="Predicted Quantity Over Time",
        color_discrete_sequence=color_seq
    )
    fig_line.update_layout(plot_bgcolor='#1b2a1f', paper_bgcolor='#1b2a1f', font_color='white')

    # Donut chart
    revenue_sum = filtered_df.groupby("product_name")["daily_revenue"].sum().reset_index()
    fig_donut = px.pie(
        revenue_sum,
        names="product_name",
        values="daily_revenue",
        hole=0.4,
        title="Revenue Share",
        color_discrete_sequence=color_seq
    )
    fig_donut.update_layout(plot_bgcolor='#1b2a1f', paper_bgcolor='#1b2a1f', font_color='white')

    # Scatter chart
    fig_scatter = px.scatter(
        filtered_df,
        x="recommended_price",
        y="predicted_quantity",
        size="daily_revenue",
        color="avg_price",
        hover_data=["event_date", "product_name", "daily_quantity", "daily_revenue"],
        color_continuous_scale=color_seq,
        title="Recommended Price vs Predicted Quantity"
    )
    fig_scatter.update_layout(plot_bgcolor='#1b2a1f', paper_bgcolor='#1b2a1f', font_color='white')

    # Box chart
    fig_box = px.box(
        filtered_df,
        x="product_name",
        y="recommended_price",
        title="Recommended Price Distribution",
        color="product_name",
        color_discrete_sequence=color_seq
    )
    fig_box.update_layout(plot_bgcolor='#1b2a1f', paper_bgcolor='#1b2a1f', font_color='white')

    return fig_bar, fig_line, fig_donut, fig_scatter, fig_box

# ===== Run App =====
if __name__ == '__main__':
    app.run(debug=True)
