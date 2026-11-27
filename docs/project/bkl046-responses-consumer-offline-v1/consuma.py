"""Parse a simulated Responses body for the frozen single-decision experiment."""
import json
import math
import re


class RejectedResponse(ValueError):
    pass


def distinct_pairs(pairs):
    value={}
    for key,item in pairs:
        if key in value:
            raise RejectedResponse("DUPLICATE_JSON_KEY")
        value[key]=item
    return value


def invalid_constant(_):
    raise RejectedResponse("NONFINITE_JSON_NUMBER")


def finite_float(value):
    number=float(value)
    if not math.isfinite(number):
        raise RejectedResponse("NONFINITE_JSON_NUMBER")
    return number


def parse_json(raw):
    try:
        return json.loads(raw,object_pairs_hook=distinct_pairs,parse_constant=invalid_constant,parse_float=finite_float)
    except RejectedResponse:
        raise
    except (ValueError,UnicodeDecodeError,RecursionError) as error:
        raise RejectedResponse("MALFORMED_JSON") from error


def extract(raw, exact_model, consumed_ids):
    if type(raw) is not bytes or not 0<len(raw)<=65536:
        raise RejectedResponse("RESPONSE_SIZE")
    body=parse_json(raw)
    if not isinstance(body,dict) or body.get("object")!="response":
        raise RejectedResponse("RESPONSE_OBJECT")
    if body.get("status")=="incomplete":
        raise RejectedResponse("RESPONSE_INCOMPLETE")
    if body.get("status")!="completed" or body.get("error") is not None or body.get("incomplete_details") is not None:
        raise RejectedResponse("RESPONSE_NOT_COMPLETED")
    if body.get("model")!=exact_model:
        raise RejectedResponse("MODEL_IDENTITY_MISMATCH")
    identity=body.get("id")
    if type(identity) is not str or not re.fullmatch(r"resp_[A-Za-z0-9_-]{1,160}",identity):
        raise RejectedResponse("RESPONSE_ID")
    if identity in consumed_ids:
        raise RejectedResponse("DUPLICATE_RESPONSE_ID")
    output=body.get("output")
    if type(output) is not list or any(type(item) is not dict for item in output):
        raise RejectedResponse("OUTPUT_STRUCTURE")
    if any(item.get("type") not in ("message","reasoning") for item in output):
        raise RejectedResponse("UNEXPECTED_OUTPUT_ITEM")
    messages=[item for item in output if item.get("type")=="message"]
    if len(messages)!=1 or messages[0].get("role")!="assistant" or messages[0].get("status","completed")!="completed":
        raise RejectedResponse("ASSISTANT_MESSAGE_REQUIRED")
    contents=messages[0].get("content")
    if type(contents) is not list or any(type(item) is not dict for item in contents):
        raise RejectedResponse("CONTENT_STRUCTURE")
    if any(item.get("type")=="refusal" for item in contents):
        raise RejectedResponse("RESPONSE_REFUSAL")
    if len(contents)!=1 or contents[0].get("type")!="output_text" or type(contents[0].get("text")) is not str:
        raise RejectedResponse("SINGLE_STRUCTURED_TEXT_REQUIRED")
    nested=parse_json(contents[0]["text"])
    consumed_ids.add(identity)
    return nested
