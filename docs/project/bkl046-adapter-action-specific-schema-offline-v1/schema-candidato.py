"""Offline action-specific schema candidate for the pinned research contract."""
from copy import deepcopy

def build_schema(schema, state):
    props = schema["properties"]
    branches = []
    for action in props["action"]["enum"]:
        shaped = deepcopy(props)
        shaped["action"]["enum"] = [action]
        if action == "TEST":
            shaped["checkpointId"]["enum"] = [None]
            steps = [step for step in shaped["step"]["anyOf"] if step.get("type") != "null"]
            for step in steps:
                proc = step["properties"]["process"]["enum"]
                if proc == ["VIVIDNESS"]:
                    step["properties"]["parameters"]["properties"]["saturation"].update(minimum=0,maximum=.25)
            if not steps:
                continue
            shaped["step"] = {"anyOf":steps}
            past = [row.get("step") for row in state["checkpoints"].values()
                    if row.get("parentId")==state["selectedId"] and row.get("stage")==state["stage"]
                    and isinstance(row.get("step"), dict)]
            if past:
                shaped["step"]["not"] = {"anyOf":[{"const":step} for step in past]}
        else:
            shaped["step"] = {"type":"null"}
            shaped["checkpointId"]["enum"] = ([choice for choice in props["checkpointId"]["enum"] if choice is not None]
                                              if action == "SELECT" else [None])
        branches.append({**schema,"properties":shaped})
    return {"anyOf":branches}


def local_conforms(schema, value, primitive_conforms):
    """Evaluate the archived subset plus the candidate's const and not."""
    if "const" in schema and schema["const"] != value:
        return False
    if "not" in schema and local_conforms(schema["not"],value,primitive_conforms):
        return False
    if "anyOf" in schema and not any(local_conforms(part,value,primitive_conforms) for part in schema["anyOf"]):
        return False
    if schema.get("type") == "object":
        fields=schema["properties"]
        return isinstance(value,dict) and set(value)==set(fields) and all(
            local_conforms(item,value[key],primitive_conforms) for key,item in fields.items())
    rest={k:v for k,v in schema.items() if k not in ("const","not","anyOf")}
    return primitive_conforms(rest,value)
