from text_to_code.NL_to_Json import generate_dsl_json
from text_to_code.json_to_DSL import json_to_dsl_text
from text_to_code.DSL_to_LarkTree import parse_dsl
from text_to_code.LarkTree_to_AST import transform_tree_to_ast
from text_to_code.AST_to_Code import generate_full_code

def run_pipeline(nl_query):
    print("--- 1. Generating JSON ... ---")
    dsl_json = generate_dsl_json(nl_query)
    # print(dsl_json)
    
    print("--- 2. Converting to DSL ... ---")
    dsl_text = json_to_dsl_text(dsl_json)
    # print(dsl_text)
    
    print("--- 3. Parsing to Lark Tree ... ---")
    tree = parse_dsl(dsl_text)
    # print(tree.pretty())
    
    print("--- 4. Transforming to AST ... ---")
    ast = transform_tree_to_ast(tree)
    # print(ast)

    print("--- 5. Generating Python Code ... ---")
    final_code = generate_full_code(ast, nl_query=nl_query, dsl_text=dsl_text)
    
    return final_code

nl_query = input("Input your natural language query: ")

code = run_pipeline(nl_query)
    
print("\n=== FINAL GENERATED STRATEGY ===\n")
print(code)
    
with open("simulator.py", "w") as f:
    f.write(code)
print("\n[Success] Strategy saved to 'simulator.py'")
