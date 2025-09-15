# dashboard_app_v1.py
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

# ===== KPIs calculation =====
total_revenue = df['daily_revenue'].sum()
total_quantity = df['predicted_quantity'].sum()
avg_price = df['recommended_price'].mean()

# ===== Layout =====
app.layout = html.Div(
    style={'backgroundColor': '#1b2a1f', 'color': 'white', 'font-family': 'Arial, sans-serif', 'padding': '20px'},
    children=[
        html.H1("Dynamic Pricing Dashboard", style={'textAlign': 'center', 'color': '#a0b394', 'margin-bottom': '20px'}),
        
        # ===== KPIs =====
        html.Div([
            html.Div([
                html.H4("Total Revenue", style={'color': '#c0d6b5'}),
                html.H2(f"${total_revenue:,.2f}", style={'color': '#ffffff'})
            ], className='kpi-card', style={'padding': '10px', 'margin-right': '20px', 'backgroundColor': '#2b3a2f', 'border-radius': '8px', 'flex': '1'}),

            html.Div([
                html.H4("Total Predicted Quantity", style={'color': '#c0d6b5'}),
                html.H2(f"{total_quantity:,.0f}", style={'color': '#ffffff'})
            ], className='kpi-card', style={'padding': '10px', 'margin-right': '20px', 'backgroundColor': '#2b3a2f', 'border-radius': '8px', 'flex': '1'}),

            html.Div([
                html.H4("Average Recommended Price", style={'color': '#c0d6b5'}),
                html.H2(f"${avg_price:.2f}", style={'color': '#ffffff'})
            ], className='kpi-card', style={'padding': '10px', 'backgroundColor': '#2b3a2f', 'border-radius': '8px', 'flex': '1'}),
        ], style={'display': 'flex', 'margin-bottom': '30px'}),
        
        # Dropdown for selecting products
        html.Div([
            html.Label("Select Products:", style={'color': '#c0d6b5', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='product_dropdown',
                options=[{'label': name, 'value': code} for code, name in zip(df['stock_code'], df['product_name'])],
                multi=True,
                value=df['stock_code'].unique()[:5],
                style={'backgroundColor': '#2b3a2f', 'color': '#ffffff'}
            )
        ], style={'margin-bottom': '25px'}),
        
        # Charts
        html.Div([
            html.Div(dcc.Graph(id='daily_revenue_chart'), style={'flex': '1', 'margin-right': '20px'}),
            html.Div(dcc.Graph(id='top5_revenue_chart'), style={'flex': '1'}),
        ], style={'display': 'flex', 'margin-bottom': '30px'}),
        
        html.Div([
            dcc.Graph(id='scatter_chart')
        ])
    ]
)

# ===== Callbacks =====
@app.callback(
    Output('daily_revenue_chart', 'figure'),
    Output('top5_revenue_chart', 'figure'),
    Output('scatter_chart', 'figure'),
    Input('product_dropdown', 'value')
)
def update_charts(selected_products):
    filtered_df = df[df['stock_code'].isin(selected_products)]

    # ===== Daily Revenue Line Chart =====
    daily_rev = filtered_df.groupby(['event_date']).agg({'daily_revenue':'sum'}).reset_index()
    fig_daily = px.line(
        daily_rev,
        x='event_date', y='daily_revenue',
        title="Daily Revenue for Selected Products",
        markers=True,
        line_shape='spline'
    )
    fig_daily.update_layout(plot_bgcolor='#1b2a1f', paper_bgcolor='#1b2a1f', font_color='white',
                            xaxis_title="Date", yaxis_title="Revenue ($)", title_x=0.5)

    # ===== Top 5 Products Donut =====
    top5 = filtered_df.groupby('product_name')['daily_revenue'].sum().nlargest(5).reset_index()
    fig_top5 = px.pie(
        top5,
        names='product_name',
        values='daily_revenue',
        hole=0.5,
        title="Top 5 Products by Revenue",
        color_discrete_sequence=px.colors.sequential.Aggrnyl
    )
    fig_top5.update_layout(plot_bgcolor='#1b2a1f', paper_bgcolor='#1b2a1f', font_color='white', title_x=0.5)

    # ===== Scatter Chart =====
    fig_scatter = px.scatter(
        filtered_df,
        x='recommended_price',
        y='predicted_quantity',
        size='daily_revenue',
        color='avg_price',
        hover_data=['event_date', 'product_name', 'daily_quantity', 'daily_revenue'],
        color_continuous_scale=px.colors.sequential.Aggrnyl,
        title="Recommended Price vs Predicted Quantity"
    )
    fig_scatter.update_layout(plot_bgcolor='#1b2a1f', paper_bgcolor='#1b2a1f', font_color='white', title_x=0.5)

    return fig_daily, fig_top5, fig_scatter

# ===== Run App =====
if __name__ == '__main__':
    app.run(debug=True)
