import psutil
import time
import json
import requests

def bytes_to_mb(bytes):
    return bytes / (1024 ** 2)

def collect_metrics():

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    network_io = psutil.net_io_counters()

    metrics = {
        "timestamp": timestamp,
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_used_mb": bytes_to_mb(memory.used),
        "disk_usage_percent": disk_usage.percent,
        "bytes_sent_mb": bytes_to_mb(network_io.bytes_sent),
        "bytes_received_mb": bytes_to_mb(network_io.bytes_recv)
    }

    return metrics

def convert_metrics_to_json(metrics):
    json_string = json.dumps(metrics)
    return json_string

def send_post_to_app(json_data, url):
    try:
        response = requests.post(url, json=json_data)

        if response.status_code == 200:
            print("Success! Response from server:", response.text)
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(f"Response Body:", response.text)

    except requests.exceptions.ConnectionError:
        print(f"Failed to connect to {url}.")
        print(f"Please ensure your Spring Boot Application is running.")
    
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    while True:
        data = collect_metrics()
        json_data = convert_metrics_to_json(data)
        print(data)
        print(json_data)
        time.sleep(5)
