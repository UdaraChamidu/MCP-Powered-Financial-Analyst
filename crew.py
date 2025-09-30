import logging
from agents.query_parser import parse_query
from agents.code_writer import code_writer
from agents.code_executor import execute

def run_query(query: str):
    logging.info(f"Input query: {query}")

    try:
        structured = parse_query(query)
    except Exception as e:
        return {"success": False, "stage": "parse", "error": str(e)}

    try:
        analysis_fn = code_writer(structured)
    except Exception as e:
        return {"success": False, "stage": "code_writer", "error": str(e)}

    exec_res = execute(analysis_fn)
    if not exec_res["success"]:
        return {"success": False, "stage": "execute", "error": exec_res["error"]}

    return {"success": True, "stage": "done", "data": exec_res["result"]}
