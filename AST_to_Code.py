import re

def translate_indicator(ind_str):
    """
    Translates DSL indicator strings to Python Pandas/TA-Lib code.
    Assumes 'df' is a Pandas DataFrame with standard OHLCV columns (lowercase).
    """
    if isinstance(ind_str, (int, float)):
        return str(ind_str)
    
    ind_str = ind_str.strip()
    
    # Basic columns
    if ind_str in ['close', 'open', 'high', 'low', 'volume']:
        return f"df['{ind_str}'].iloc[-1]"
    
    # Simple Moving Average: sma(period)
    match = re.match(r'sma\((\d+)\)', ind_str, re.IGNORECASE)
    if match:
        period = match.group(1)
        return f"df['close'].rolling({period}).mean().iloc[-1]"
        
    # Exponential Moving Average: ema(period)
    match = re.match(r'ema\((\d+)\)', ind_str, re.IGNORECASE)
    if match:
        period = match.group(1)
        return f"df['close'].ewm(span={period}, adjust=False).mean().iloc[-1]"
    
    # RSI: rsi(period)
    # Using a simple custom calculation or assuming pandas_ta
    match = re.match(r'rsi\((\d+)\)', ind_str, re.IGNORECASE)
    if match:
        period = match.group(1)
        return f"calculate_rsi(df['close'], {period}).iloc[-1]"

    # MACD: macd()
    if ind_str.lower() == 'macd()':
         return f"calculate_macd(df['close']).iloc[-1]"

    # Fallback for unknown
    return ind_str

def generate_condition_string(rules):
    if not rules:
        return "False"
        
    code_parts = []
    
    for i, rule in enumerate(rules):
        expr = rule['expression']
        logic = rule.get('logic_op')
        
        lhs = translate_indicator(expr['indicator'])
        op = expr['operator']
        rhs = translate_indicator(expr['value'])
        
        # Construct comparison: e.g. (df['close'] > 100)
        condition_str = f"({lhs} {op} {rhs})"
        code_parts.append(condition_str)

        if logic:
            py_logic = "and" if logic.upper() == "AND" else "or"
            code_parts.append(f" {py_logic} ")
            
    return "".join(code_parts)

def generate_full_code(ast_data, nl_query="", dsl_text=""):
    entry_rules = ast_data.get('entry', [])
    exit_rules = ast_data.get('exit', [])
    
    entry_code = generate_condition_string(entry_rules)
    exit_code = generate_condition_string(exit_rules)
    
    # Escape triple quotes in strings to avoid breaking the template
    nl_query_safe = nl_query.replace('"""', '\\"\\"\\"')
    dsl_text_safe = dsl_text.replace('"""', '\\"\\"\\"')
    ast_safe = str(ast_data).replace('"""', '\\"\\"\\"')

    template = f"""import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# Metadata
# -----------------------------------------------------------------------------
NL_QUERY = \"\"\"{nl_query_safe}\"\"\"
DSL_TEXT = \"\"\"{dsl_text_safe}\"\"\"
AST_DATA = \"\"\"{ast_safe}\"\"\"

# -----------------------------------------------------------------------------
# Indicator Helper Functions
# -----------------------------------------------------------------------------

def calculate_rsi(series, period):
    if len(series) < period:
        return pd.Series([50]*len(series)) # Default or NaN
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(pd.to_numeric(period)).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(pd.to_numeric(period)).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    # signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd

# -----------------------------------------------------------------------------
# Strategy Logic
# -----------------------------------------------------------------------------

def entry_rule(df):
    try:
        return {entry_code}
    except Exception:
        return False

def exit_rule(df):
    try:
        return {exit_code}
    except Exception:
        return False

# -----------------------------------------------------------------------------
# Backtest Engine
# -----------------------------------------------------------------------------

def run_backtest():
    # Load Data
    try:
        df = pd.read_csv('synthetic_OHLCV.csv')
        df['date'] = pd.to_datetime(df['date'])
    except FileNotFoundError:
        print("Error: synthetic_OHLCV.csv not found.")
        return

    in_position = False
    entry_price = 0.0
    entry_date = None
    trades = []
    
    # Portfolio for Drawdown calc
    initial_capital = 10000.0
    capital = initial_capital
    portfolio_values = []

    # Iteration (Warmup period assumed 20 for indicators)
    for i in range(20, len(df)):
        # Simulate 'Live' by slicing up to current index
        window = df.iloc[:i+1]
        current_price = window['close'].iloc[-1]
        current_date = window['date'].iloc[-1]
        
        # Portfolio Value Tracking
        current_val = capital
        if in_position:
            # If holding, value is capital (cash) + unrealized PnL logic OR just shares value
            # Simple interaction: One share per trade? Or all in?
            # Let's assume we buy 1 share for simplicity, or fixed amount.
            # To match specific return % logic, let's track trade PnL % independently 
            # or simulate 1 unit to get price diff.
            pass
        
        if not in_position:
            if entry_rule(window):
                in_position = True
                entry_price = current_price
                entry_date = current_date
        else:
            if exit_rule(window):
                in_position = False
                exit_price = current_price
                exit_date = current_date
                
                pnl = exit_price - entry_price
                return_pct = (pnl / entry_price) * 100
                
                trades.append({{
                    'Entry Date': entry_date,
                    'Exit Date': exit_date,
                    'Entry Price': entry_price,
                    'Exit Price': exit_price,
                    'PnL': pnl,
                    'Return %': return_pct
                }})
                
                # Update capital - simplistically adding PnL for Total Return Calc relative to 1 share price? 
                # Or just sum Returns %.
                # Let's accumulate percent return for "Total Return" to match user example logic (Sum of % or Compound?).
                # User asked: "Entry price / exit price, Profit/loss, Total return".
                # Usually Total Return is compounded or Sum of PnL / Start Capital.
                # Use Simple Sum of PnL for now.
                capital += pnl
    
    # -----------------------------------------------------------------------------
    # Metrics & Reporting
    # -----------------------------------------------------------------------------
    
    trades_df = pd.DataFrame(trades)
    
    if not trades_df.empty:
        total_pnl = trades_df['PnL'].sum()
        total_return_pct = (trades_df['Return %'].sum()) # Simple sum of trade returns
        
        # Max Drawdown Approximation
        # Construct equity curve from trade results
        equity = [initial_capital]
        for pnl in trades_df['PnL']:
            equity.append(equity[-1] + pnl)
        
        equity_series = pd.Series(equity)
        rolling_max = equity_series.cummax()
        drawdown = (equity_series - rolling_max) / rolling_max
        max_drawdown_pct = drawdown.min() * 100
        
        trade_count = len(trades)
    else:
        total_pnl = 0.0
        total_return_pct = 0.0
        max_drawdown_pct = 0.0
        trade_count = 0
        
    
    # Save Report
    trades_df.to_csv('report.csv', index=False)
    
    # Print Final Format
    print("Natural Language Input:")
    print(f'"{nl_query.strip()}"')
    print("\\nGenerated DSL:")
    print(DSL_TEXT.strip())
    print("\\nParsed AST:", AST_DATA)
    print("\\nBacktest Result:")
    print(f"Total Return: {{total_return_pct:.1f}}%")
    print(f"Max Drawdown: {{max_drawdown_pct:.1f}}%")
    print(f"Trades: {{trade_count}}")
    print("Entry/Exit Log:")
    
    if not trades_df.empty:
        for _, row in trades_df.iterrows():
            print(f"- Enter: {{row['Entry Date'].date()}} at {{row['Entry Price']}}")
            print(f"- Exit: {{row['Exit Date'].date()}} at {{row['Exit Price']}}")

if __name__ == "__main__":
    run_backtest()
"""
    return template