# src/dashboard/dashboard_app.py
import pandas as pd
import numpy as np
from datetime import timedelta
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# -------------------------
# Load data
# -------------------------
RECS = "data/recommendations/daily_price_recommendation.csv"
TOP = "data/recommendations/top_products.csv"

df = pd.read_csv(RECS, parse_dates=['event_date'])
top_products = pd.read_csv(TOP)

# ensure numeric types
df['predicted_quantity'] = pd.to_numeric(df['predicted_quantity'], errors='coerce').fillna(0)
df['recommended_price'] = pd.to_numeric(df.get('recommended_price', df.get('rec_price', 'avg_price')), errors='coerce')
df['avg_price'] = pd.to_numeric(df['avg_price'], errors='coerce')

# derived revenue (using recommended price if present, otherwise avg_price)
df['revenue'] = df['predicted_quantity'] * df['recommended_price'].fillna(df['avg_price'])

# default products (top by revenue)
default_products = list(top_products['product_name'].head(6).values) if not top_products.empty else list(df['product_name'].unique()[:6])

# Color palette (fancy & elegant)
PALETTE = ["#FFD369", "#6C5B7B", "#355C7D", "#2A9D8F", "#F08A5D", "#7FB069", "#9B59B6", "#E76F51", "#4D9078"]

# -------------------------
# Initialize app
# -------------------------
app = dash.Dash(__name__)
app.title = "Dynamic Pricing Dashboard"

# -------------------------
# Layout
# -------------------------
app.layout = html.Div([
    html.Div([
        html.H1("📊 Dynamic Pricing Dashboard",
                style={'textAlign': 'center', 'color': '#FFD369', 'marginBottom': '6px'}),
        html.Div("Interactive visual analysis — filter by product & date range", style={'textAlign': 'center', 'color': '#cfd7c7', 'marginBottom': '20px'})
    ]),

    # Controls row
    html.Div([
        html.Div([
            html.Label("Select products", style={'color': '#cfd7c7'}),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': p, 'value': p} for p in df['product_name'].sort_values().unique()],
                value=default_products,
                multi=True,
                placeholder="Choose products...",
                style={'minWidth': '280px'}
            )
        ], style={'flex': '1', 'minWidth': '280px', 'marginRight': '12px'}),

        html.Div([
            html.Label("Date range", style={'color': '#cfd7c7'}),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=df['event_date'].min(),
                max_date_allowed=df['event_date'].max(),
                start_date=(df['event_date'].max() - pd.Timedelta(days=60)).date(),
                end_date=df['event_date'].max().date(),
                display_format='YYYY-MM-DD',
                minimum_nights=0,
                style={'color': '#000'}
            )
        ], style={'marginRight': '12px'}),

        html.Div([
            html.Label("Top N (pie/bar)", style={'color': '#cfd7c7'}),
            dcc.Slider(id='top-n', min=3, max=15, step=1, value=6,
                       marks={3: '3', 6: '6', 10: '10', 15: '15'})
        ], style={'flex': '1', 'minWidth': '220px', 'paddingTop': '6px'})
    ], style={'display': 'flex', 'gap': '12px', 'marginBottom': '18px', 'alignItems': 'center'}),

    # KPI cards
    html.Div([
        html.Div([
            html.Div("Total Revenue", style={'color': '#cfd7c7'}),
            html.H2(id='kpi-revenue', style={'color': '#ffffff', 'marginTop': '6px'})
        ], style={'backgroundColor': '#2b3a2f', 'padding': '12px', 'borderRadius': '8px', 'flex': '1', 'textAlign': 'center', 'marginRight': '12px'}),

        html.Div([
            html.Div("Total Predicted Qty", style={'color': '#cfd7c7'}),
            html.H2(id='kpi-qty', style={'color': '#ffffff', 'marginTop': '6px'})
        ], style={'backgroundColor': '#2b3a2f', 'padding': '12px', 'borderRadius': '8px', 'flex': '1', 'textAlign': 'center', 'marginRight': '12px'}),

        html.Div([
            html.Div("Avg Recommended Price", style={'color': '#cfd7c7'}),
            html.H2(id='kpi-price', style={'color': '#ffffff', 'marginTop': '6px'})
        ], style={'backgroundColor': '#2b3a2f', 'padding': '12px', 'borderRadius': '8px', 'flex': '1', 'textAlign': 'center'})
    ], style={'display': 'flex', 'marginBottom': '20px'}),

    # Tabs for charts
    dcc.Tabs([
        dcc.Tab(label='Line (Revenue)', children=[
            dcc.Graph(id='line-chart', config={'displayModeBar': True})
        ]),
        dcc.Tab(label='Dot (Predicted Qty)', children=[
            dcc.Graph(id='dot-chart')
        ]),
        dcc.Tab(label='Bar (Top Products)', children=[
            dcc.Graph(id='bar-chart')
        ]),
        dcc.Tab(label='Pie / Donut', children=[
            dcc.Graph(id='pie-chart')
        ]),
        dcc.Tab(label='Scatter (Price vs Qty)', children=[
            dcc.Graph(id='scatter-chart')
        ])
    ], style={'fontSize': '15px'}, colors={'border': '#222831', 'primary': '#FFD369', 'background': '#393E46'}),

    html.Div(style={'height': '30px'})  # spacer
], style={'backgroundColor': '#222831', 'padding': '18px', 'fontFamily': 'Arial, sans-serif'})

# -------------------------
# Helper: filter df
# -------------------------
def filter_df(products, start_date, end_date):
    d = df.copy()
    if products:
        d = d[d['product_name'].isin(products)]
    if start_date:
        d = d[d['event_date'] >= pd.to_datetime(start_date)]
    if end_date:
        d = d[d['event_date'] <= pd.to_datetime(end_date)]
    return d

# -------------------------
# Callbacks
# -------------------------
@app.callback(
    Output('kpi-revenue', 'children'),
    Output('kpi-qty', 'children'),
    Output('kpi-price', 'children'),
    Input('product-dropdown', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_kpis(products, start_date, end_date):
    d = filter_df(products, start_date, end_date)
    total_rev = d['revenue'].sum()
    total_qty = d['predicted_quantity'].sum()
    avg_price = d['recommended_price'].mean() if 'recommended_price' in d.columns else d['avg_price'].mean()
    return f"${total_rev:,.2f}", f"{total_qty:,.0f}", f"${(avg_price if not np.isnan(avg_price) else 0):.2f}"

@app.callback(
    Output('line-chart', 'figure'),
    Input('product-dropdown', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_line_chart(products, start_date, end_date):
    d = filter_df(products, start_date, end_date)
    if d.empty:
        fig = px.line(title="No data for selection")
        fig.update_layout(template='plotly_dark')
        return fig

    # aggregate daily revenue by date and product (so multiple products are separate lines)
    agg = d.groupby(['event_date', 'product_name'])['revenue'].sum().reset_index()
    agg = agg.sort_values('event_date')
    fig = px.line(agg, x='event_date', y='revenue', color='product_name',
                  markers=True, line_shape='spline', template='plotly_dark',
                  color_discrete_sequence=PALETTE)
    fig.update_layout(title="Daily Revenue (selected products)",
                      xaxis_title="Date", yaxis_title="Revenue ($)",
                      hovermode='x unified')
    fig.update_yaxes(tickprefix="$", separatethousands=True)
    fig.update_xaxes(rangeslider_visible=True)
    return fig

@app.callback(
    Output('dot-chart', 'figure'),
    Input('product-dropdown', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_dot_chart(products, start_date, end_date):
    d = filter_df(products, start_date, end_date)
    if d.empty:
        fig = px.scatter(title="No data for selection")
        fig.update_layout(template='plotly_dark')
        return fig

    # show predicted quantity distribution (aggregate by product, show latest day for clarity)
    latest = d.groupby(['product_name', 'event_date'])['predicted_quantity'].sum().reset_index()
    latest_date = latest['event_date'].max()
    latest = latest[latest['event_date'] == latest_date]
    latest = latest.sort_values('predicted_quantity', ascending=False)
    fig = px.scatter(latest, x='product_name', y='predicted_quantity', size='predicted_quantity',
                     hover_data=['event_date'], template='plotly_dark', color_discrete_sequence=PALETTE)
    fig.update_layout(title=f"Predicted Quantity per Product (latest date: {latest_date.date()})",
                      xaxis_tickangle=-45)
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    Input('product-dropdown', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('top-n', 'value')
)
def update_bar_chart(products, start_date, end_date, top_n):
    d = filter_df(products, start_date, end_date)
    if d.empty:
        fig = px.bar(title="No data for selection")
        fig.update_layout(template='plotly_dark')
        return fig

    agg = d.groupby('product_name')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
    top = agg.head(top_n)
    fig = px.bar(top, x='product_name', y='revenue', template='plotly_dark',
                 color='product_name', color_discrete_sequence=PALETTE)
    fig.update_layout(title=f"Top {top_n} Products by Revenue", xaxis_tickangle=-45)
    fig.update_yaxes(tickprefix="$", separatethousands=True)
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    Input('product-dropdown', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('top-n', 'value')
)
def update_pie_chart(products, start_date, end_date, top_n):
    d = filter_df(products, start_date, end_date)
    if d.empty:
        fig = px.pie(title="No data for selection")
        fig.update_layout(template='plotly_dark')
        return fig

    agg = d.groupby('product_name')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
    if len(agg) > top_n:
        top = agg.head(top_n).copy()
        other_sum = agg['revenue'].iloc[top_n:].sum()
        top = top.append({'product_name': 'Other', 'revenue': other_sum}, ignore_index=True)
    else:
        top = agg
    fig = px.pie(top, names='product_name', values='revenue', hole=0.45, template='plotly_dark',
                 color_discrete_sequence=PALETTE)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title=f"Revenue share (Top {top_n})")
    return fig

@app.callback(
    Output('scatter-chart', 'figure'),
    Input('product-dropdown', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_scatter(products, start_date, end_date):
    d = filter_df(products, start_date, end_date)
    if d.empty:
        fig = px.scatter(title="No data for selection")
        fig.update_layout(template='plotly_dark')
        return fig

    # aggregate per product to keep scatter readable
    agg = d.groupby('product_name').agg(avg_price=('avg_price', 'mean'),
                                        avg_pred_qty=('predicted_quantity', 'mean'),
                                        total_revenue=('revenue', 'sum'),
                                        count_days=('event_date', 'nunique')).reset_index()
    fig = px.scatter(agg, x='avg_price', y='avg_pred_qty',
                     size='total_revenue', color='product_name',
                     hover_data=['product_name', 'total_revenue', 'count_days'],
                     template='plotly_dark', color_discrete_sequence=PALETTE)
    fig.update_layout(title="Avg Price vs Avg Predicted Quantity (per product)",
                      xaxis_title="Avg Price ($)", yaxis_title="Avg Predicted Qty")
    fig.update_xaxes(tickprefix="$")
    return fig

# -------------------------
# Run server
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
