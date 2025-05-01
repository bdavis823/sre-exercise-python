# SRE Take-Home Exercise

## Overview
This tool monitors the availability of a set of HTTP endpoints defined in a YAML file. It periodically checks each endpoint and logs the availability percentage per domain every 15 seconds.

## Requirements
- Python 3.7+
- `requests` and `PyYAML` libraries

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/bdavis823/sre-exercise-python/
   cd sre-exercise-python
   ```
   

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Monitor
Run the script with the provided `sample.yaml`:
```bash
python3 main.py sample.yaml
```

The tool will start logging availability every 15 seconds into `availability.log`.

---

## Fix Summary and Requirements Addressed

### Requirements and How They Were Met

1. **Use YAML Configuration as Command-Line Argument**:
   - Fix: Accepts a YAML file via `sys.argv[1]` and parses it using `PyYAML`.

2. **YAML Format Must Match Provided Sample**:
   - Fix: Supports fields like `url`, `method`, `headers`, `body`, and `name`.

3. **Accurately Determine Endpoint Availability**:
   - Fix: Performs HTTP requests with appropriate headers, method, and body. Evaluates status and response time.

4. **Availability Only if Status is 2xx and Response ≤ 500ms**:
   - Fix: Enforced in the `is_available()` function using strict criteria.

5. **Return Availability by Domain (Not Full URL)**:
   - Fix: Extracts the hostname from each URL using `urllib.parse.urlparse`.

6. **Ignore Port Numbers When Determining Domain**:
   - Fix: Uses `urllib.parse.urlparse.hostname`, which excludes port numbers.

7. **Determine Availability Cumulatively**:
   - Fix: The `domain_stats` dictionary maintains running totals per domain.

8. **Check Cycles Every 15 Seconds Regardless of Endpoint Count**:
   - Fix: Uses `time.sleep(15)` after each full check cycle.

### Code Issues Identified and Fixes

1. **Incorrect Grouping Due to Using Full URLs**:
   - Fix: Used `urllib.parse.urlparse` to isolate domain names only.

2. **Did Not Enforce Both Status Code and Response Time**:
   - Fix: Now checks both `200 ≤ status < 300` and `response time ≤ 500ms`.

3. **Exceptions During Requests Could Crash the Script**:
   - Fix: Wrapped request logic in a `try-except` block for stability.

4. **Log Lacked Clarity, Formatting, and Cumulative Info**:
   - Fix: Added structured domain-level reporting every 15 seconds with timestamps.


### Original Issues Identified:
1. **Missing Method Default**:
   - Fix: If method is not provided in the config, default to `GET`.
2. **Missing Required Fields**:
   - Fix: Add logic to handle absent `headers`, `body`, and `method` keys.
3. **Improper Loop Exit**:
   - Fix: The script runs indefinitely as per the spec. If desired, you can break the loop after N iterations for test purposes.
4. **Unavailable Domain Aggregation**:
   - Fix: Extracted domain from URLs and aggregated statistics per domain.
5. **Log Formatting**:
   - Fix: Structured output with timestamp and domain-based percentage.
6. **Test Coverage**:
   - Fix: Added unit tests for all key functions with mocked network calls.



---

## Example Output (in `availability.log`):
```
Log timestamp: 2025-05-01 13:00:30
------ Availability Report ------
dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 50% availability percentage
---  End of Report ---
```

## Testing
Run tests using:
```bash
python3 -m unittest test_main.py
```

