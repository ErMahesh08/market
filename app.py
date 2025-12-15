import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd

# --- 1. Initialize the App ---
app = dash.Dash(__name__)
app.title = "Market Watch Pro"

# --- 2. Define the Layout (HTML + Graphs) ---
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'background-color': '#f4f6f9', 'padding': '20px'}, children=[
    
    # Header Section
    html.Div([
        html.H1("Global Market Watch", style={'text-align': 'center', 'color': '#2c3e50'}),
        html.P("Live Financial Data & Graphical Analysis", style={'text-align': 'center', 'color': '#7f8c8d'})
    ]),

    # Control Panel (Dropdown)
    html.Div([
        html.Label("Select Market Asset:", style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[
                {'label': 'Apple Inc. (AAPL)', 'value': 'AAPL'},
                {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
                {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
                {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
                {'label': 'Gold (GC=F)', 'value': 'GC=F'},
                {'label': 'S&P 500 (ES=F)', 'value': 'ES=F'}
            ],
            value='AAPL',  # Default selection
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'text-align': 'center', 'padding': '20px'}),

    # Graphical Feature: Interactive Chart
    html.Div([
        dcc.Graph(id='market-chart', style={'height': '70vh'})
    ], style={'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)', 'background-color': 'white', 'padding': '10px'})
])

# --- 3. The Logic (Callbacks) ---
@app.callback(
    Output('market-chart', 'figure'),
    [Input('stock-dropdown', 'value')]
)
def update_graph(selected_stock):
    # Fetch real data for the selected stock (last 6 months)
    # The progress=False parameter hides the download bar in the terminal
    ticker = yf.Ticker(selected_stock)
    df = ticker.history(period='6mo')

    # Create the Candlestick Chart (Open, High, Low, Close)
    fig = go.Figure()

    # Add the Candlestick trace
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Market Price'
    ))

    # Add a Moving Average line (Trend Indicator)
    if len(df) > 20:
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['MA20'], 
            line=dict(color='orange', width=1), 
            name='20-Day Trend'
        ))

    # Update Layout Styles
    fig.update_layout(
        title=f'{selected_stock} - Price History & Trend Analysis',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_white',
        xaxis_rangeslider_visible=True, # The bottom slider
        hovermode='x unified'
    )

    return fig

# --- 4. Run the Server ---
if __name__ == '__main__':
    # CORRECTED LINE: Using app.run() instead of app.run_server()
    app.run(debug=True)