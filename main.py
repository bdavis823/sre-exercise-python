import json
from datetime import datetime
import yaml
import requests
import time
from collections import defaultdict
from urllib.parse import urlparse


# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# Function to extract domain name from the URL
def extract_domain(url):
    parsed = urlparse(url)
    return parsed.hostname


# Function to make a request to the endpoint and measure time it takes
def request(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        json_body = json.loads(body) if body else None
        starting_time = time.time()
        response = requests.request(method, url, headers=headers, json=json_body)
        duration = (time.time() - starting_time) * 1000
        return response.status_code, duration
    except requests.RequestException:
        return None, None


# Function to check if the request was successful and the duration was under 500 ms
def is_available(status_code, duration):
    return status_code and 200 <= status_code < 300 and duration <= 500


# Function to log the results to a file
def log_result(domain_stats, log_file='availability.log'):
    try:
        with open(log_file, 'a') as log:
            log.write(f"Log timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write("------ Availability Report ------\n")

            for domain, stats in domain_stats.items():
                if stats["total"] > 0:
                    availability = int(100 * stats["up"] / stats["total"])
                    log.write(f"{domain} has {availability}% availability percentage\n")
            log.write("---  End of Report --- \n\n")
    except IOError as e:
        print(f"Error writing to log file: {e}")


# Function to perform health checks
def check_health(endpoint):
    status_code, duration = request(endpoint)
    if status_code is None or duration is None:
        return "DOWN"
    elif is_available(status_code, duration):
        return "UP"
    else:
        return "DOWN"


# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            domain = extract_domain(endpoint['url'])
            result = check_health(endpoint)
            domain_stats[domain]["total"] += 1

            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        log_result(domain_stats, log_file='availability.log')
        print("---")
        time.sleep(15)


# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
