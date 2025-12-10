def json_to_dsl_text(dsl_json_input):
    # Ensure dsl_json is a dict
    dsl_json = dsl_json_input
    if isinstance(dsl_json, list):
        dsl_json = dsl_json[0]

    lines = []

    entry_items = dsl_json.get("entry", [])
    lines.append("ENTRY:")

    rule_count = 1
    for item in entry_items:
        # CASE 1: Condition object
        if "indicator" in item:
            indicator = item["indicator"]
            operator = item["operator"]
            value = item["value"]

            value_str = str(value) if isinstance(value, (int, float)) else value

            lines.append(f"RULE{rule_count}: {indicator} {operator} {value_str}")
            rule_count += 1

        # CASE 2: Logic object → add logic to previous rule line
        elif "logic" in item:
            logic = item["logic"].upper()
            lines[-1] = lines[-1] + f" {logic}"


    exit_items = dsl_json.get("exit", [])
    lines.append("EXIT:")

    rule_count = 1
    for item in exit_items:
        if "indicator" in item:
            indicator = item["indicator"]
            operator = item["operator"]
            value = item["value"]

            value_str = str(value) if isinstance(value, (int, float)) else value

            lines.append(f"RULE{rule_count}: {indicator} {operator} {value_str}")
            rule_count += 1

        elif "logic" in item:
            logic = item["logic"].upper()
            lines[-1] = lines[-1] + f" {logic}"

    return "\n".join(lines)