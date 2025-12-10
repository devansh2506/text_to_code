from lark import Lark

grammar = r"""
start: entry exit

entry: "ENTRY:" rule*
exit: "EXIT:" rule*

rule: RULE_NAME ":" expr [LOGIC_OP]

expr: indicator OP value

indicator: BASE_INDICATOR
         | SMA
         | EMA
         | RSI
         | ATR
         | MACD

value: NUMBER | indicator

# -----------------------
# INDICATORS
# -----------------------

BASE_INDICATOR: "close" | "open" | "high" | "low" | "volume"

SMA: /sma\(\d+\)/
EMA: /ema\(\d+\)/
RSI: /rsi\(\d+\)/
ATR: /atr\(\d+\)/
MACD: /macd\(\)/

# -----------------------
# OTHER TERMINALS
# -----------------------

RULE_NAME: /RULE[0-9]+/

LOGIC_OP: "AND" | "OR"

OP: ">" | "<" | ">=" | "<=" | "==" | "!="

%import common.NUMBER
%import common.WS
%ignore WS
"""

def parse_dsl(dsl_text):
    parser = Lark(grammar, start="start")
    tree = parser.parse(dsl_text)
    return tree
