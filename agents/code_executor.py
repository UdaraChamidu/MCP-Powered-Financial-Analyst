import logging
import traceback

def execute(analysis_callable):
    """
    Agent 3: Code Executor
    Runs the callable and returns result.
    """
    try:
        res = analysis_callable()
        logging.info("Execution successful.")
        return {"success": True, "result": res}
    except Exception as err:
        tb = traceback.format_exc()
        logging.error(f"Execution failed: {err}")
        return {"success": False, "error": str(err), "traceback": tb}
