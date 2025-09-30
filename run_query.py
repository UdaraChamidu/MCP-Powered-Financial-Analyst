import sys
import logging
from crew import run_query

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if __name__ == "__main__":
    q = "Plot YTD stock gain of Tesla"
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])

    out = run_query(q)
    if not out["success"]:
        logging.error("Flow failed at stage: %s", out.get("stage"))
        logging.error(out.get("error"))
        sys.exit(1)
    else:
        data = out["data"]
        logging.info("RESULT:")
        for k, v in data.items():
            logging.info(f"  {k}: {v}")
        print("\nPlot saved to:", data["plot_path"])

