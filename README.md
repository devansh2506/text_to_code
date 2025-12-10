# TextToCode (Natural Language Query to code)

This project is an AI-powered pipeline that converts **Natural Language** (English) trading ideas into executable **Python Trading Strategies**. It allows users to describe a strategy in plain English, generates the underlying code, and automatically runs a backtest simulation on synthetic market data.

## Project Overview

The system follows a multi-stage compilation process to ensure accuracy and safety:

1.  **NL to JSON**: Uses an LLM (Gemini) to parse the English query into a structured JSON format.
2.  **JSON to DSL**: Converts the JSON into a Domain Specific Language (DSL).
3.  **DSL to Parse Tree**: Uses the **Lark** parser to validate the grammar and build a parse tree.
4.  **Tree to AST**: Transforms the parse tree into an Abstract Syntax Tree (AST).
5.  **AST to Code**: Compiles the AST into a fully functional Python script (`simulator.py`).
6.  **Simulation**: The generated script runs a backtest engine on OHLCV data and produces a performance report.

## Setup & Requirements

Ensure you have Python installed and the required dependencies:

```bash
pip install pandas numpy google-genai lark
```

*Note: You will need a valid API Key for Google Gemini in `NL_to_Json.py` or configured in your environment.*

## How to Run

1.  **Run the Pipeline**:
    Execute the main script to start the interactive converter:
    ```bash
    python3 run.py
    ```

2.  **Enter your Strategy**:
    When prompted, type your trading strategy in plain English (see examples below).

3.  **View Results**:
    *   The system will generate a file named **`simulator.py`**.
    *   It will automatically execute `simulator.py`.
    *   Final results (Total Return, Max Drawdown, Trades) will be printed to the console.
    *   A detailed trade log is saved to `report.csv`.

## Example Prompts (Try These!)

Since the project currently uses **Synthetic Data** (a simulated 30-day uptrend where price moves from 100 to 165), use these specific prompts to ensure you see active trades and profit taking:

**1. The Profit Taker (Simple Price Target)**
*Captures the trend and exits at a specific price level.*
> "Buy when close is above 102. Sell when close is above 150."

**2. Moving Average with Profit Target**
*Enters based on a trend indicator and exits for profit.*
> "Buy when close is above sma of last 5 days. Sell when close is above 145."

**3. RSI Overbought Strategy**
*Buys early in the trend and exits when the momentum indicator gets too high.*
> "Buy when close is above 105. Sell when rsi of last 14 days is above 70."

## File Structure

*   `run.py`: Main entry point. Coordinates the entire pipeline.
*   `NL_to_Json.py`: Handles the AI prompt engineering.
*   `json_to_DSL.py`: Formatter for the Domain Specific Language.
*   `DSL_to_LarkTree.py`: Defines the grammar and runs the parser.
*   `LarkTree_to_AST.py`: Logic transformer.
*   `AST_to_Code.py`: Code generator and Backtest Engine template.
*   `synthetic_OHLCV.csv`: Sample market data for testing.
