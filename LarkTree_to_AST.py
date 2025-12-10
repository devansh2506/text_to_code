from lark import Transformer


class DSLTransformer(Transformer):
    def start(self, items):
        return {
            "entry": items[0],
            "exit": items[1]
        }

    def entry(self, items):
        return items  # Returns list of rules

    def exit(self, items):
        return items  # Returns list of rules

    def rule(self, items):
        # rule: RULE_NAME ":" expr [LOGIC_OP]
        # items will be [RULE_NAME, expr] or [RULE_NAME, expr, LOGIC_OP]
        
        rule_name = items[0]
        expression = items[1]
        logic_op = items[2] if len(items) > 2 else None
        
        return {
            "rule_name": rule_name,
            "expression": expression,
            "logic_op": logic_op
        }

    def expr(self, items):
        # expr: indicator OP value
        return {
            "indicator": items[0],
            "operator": items[1],
            "value": items[2]
        }

    def indicator(self, items):
        # indicator: BASE_INDICATOR | SMA | EMA | RSI | ATR | MACD
        return items[0]

    def value(self, items):
        # value: NUMBER | indicator
        return items[0]

    # Terminals
    def RULE_NAME(self, token):
        return str(token)

    def LOGIC_OP(self, token):
        return str(token)

    def OP(self, token):
        return str(token)

    def BASE_INDICATOR(self, token):
        return str(token)

    def SMA(self, token):
        return str(token)

    def EMA(self, token):
        return str(token)

    def RSI(self, token):
        return str(token)

    def ATR(self, token):
        return str(token)

    def MACD(self, token):
        return str(token)

    def NUMBER(self, token):
        try:
            return int(token)
        except ValueError:
            return float(token)



def transform_tree_to_ast(tree):
    transformer = DSLTransformer()
    ast = transformer.transform(tree)
    return ast