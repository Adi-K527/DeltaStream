import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

# Databricks configuration
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
CLUSTER_ID = os.getenv("CLUSTER_ID")
EMAIL = os.getenv("EMAIL")

def submit_job(notebook, poll_interval=10):
    url_submit = f"{DATABRICKS_HOST}/api/2.1/jobs/runs/submit"
    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}

    payload = {
        "run_name": f"Airflow Notebook Run - {notebook}",
        "existing_cluster_id": CLUSTER_ID,
        "notebook_task": {
            "notebook_path": f"/Workspace/Users/{EMAIL}/DeltaStream/databricks/{notebook}",
            "base_parameters": {"Kafka Instance IP": "44.203.83.38:9092"}
        }
    }

    response = requests.post(url_submit, json=payload, headers=headers)
    response.raise_for_status()
    run_info = response.json()
    run_id = run_info["run_id"]
    print(f"Notebook {notebook} submitted, run_id={run_id}")

    url_get = f"{DATABRICKS_HOST}/api/2.1/jobs/runs/get"
    while True:
        r = requests.get(url_get, params={"run_id": run_id}, headers=headers)
        r.raise_for_status()
        run_status = r.json()["state"]
        life_cycle = run_status.get("life_cycle_state")
        result_state = run_status.get("result_state")
        print(f"Run {run_id} status: {life_cycle}")

        if life_cycle in ("TERMINATED", "SKIPPED", "INTERNAL_ERROR"):
            if result_state == "SUCCESS":
                print(f"Notebook {notebook} completed successfully!")
            else:
                print(f"Notebook {notebook} failed or skipped. Result: {result_state}")
            break

        time.sleep(poll_interval)

    return run_info



def transform_data_bronze():
    submit_job("Bronze")


def transform_data_silver():
    submit_job("Silver")


def transform_data_gold():
    submit_job("Gold")