# -- Project System Architecture --

/*
    Project Purpose: Create a full-stack network monitoring dashboard that collects system and network metrics, using python to scrape the data, java + springboot for the backend to        validate the data and provide an API to connect it to the frontend, JS + React which will display the collected data to the user
*/

/*
    Data flow: Python -> Java -> PostgreSQL -> Java -> Client
*/

# Python Agent:
- Collect Metrics: CPU, Memory, Disk Usage and Mock "network latency" stats
- Store the metrics, and print them clearly (FIRST, make sure that the collection works)
- Set up functionality to normalize the data into a dictionary, then serialize to JSON
    - For normalizing, transform the raw data into a structured dictionary where a specific key is used to easily access each corresponding record
- The data being in JSON format enables sending the collected metrics via HTTP
- Add a timestamp to the data in JSON format 

1. Metric Collection System --> stores it into generic list
2. Normalize Metric Data System --> normalizes the data collected into a dictionary
3. Convert Normalized Dict to JSON + Timestamp --> enables sending the metric via HTTP

# Java REST API
* BUILD A STATELESS REST API THAT:
    1. Accepts Metric Data
    2. Validates it
    3. Returns responses

- Create the Spring Boot project
- Implement POST /metrics
- JSON metric data --> Java Data Transfer Object (DTO) mapping
- Input validation
    1. Required fields
        - host-id
        - cpu-usage
            - 0 <= value <= 100
        - memory-usage
            - 0 <= value <= 100
        - disk-usage
            - 0 <= value <= 100
        - timestamp
            - ensure the posted date is not in the future
- Proper HTTP status codes
    1. 201 --> Created
    2. 400 --> Bad Request

1. System to map JSON metric data to Java DTO
2. Input validation System
3. HTTP status codes system

- When input is validated, i.e. the validation passes
    - return a 201 created code
    - return a JSON object
        - message indicating the metric was accepted
        - a status message of success

- When input is NOT validated --> return a 400 bad request code
    - return a JSON object
        - "error" message indicating that the validation failed
        - a details message which will describe what exactly went wrong and what portion of the metric data was not permitted

* FOR TESTING:
    - use 'curl -X POST http://localhost:8080/api/v1/metrics \
        -H "Content-Type: application/json" \
        -d '{"hostid":"node-1", "cpu-usage":120}'
    - the above example would expect a: 400 Bad Request HTTP error code

* NO DATABASE YET

# Python --> Java Integration
- The goal is End-to-End data flow
- Python agent will send the HTTP Post request to the spring boot application
- Important features:
    1. Python agent sending HTTP POST
    2. Retry the logic on failure
    3. Logging
    4. Timeout handling

- This will end up resulting in a working distributed system

# PostgreSQL Integration
- Persist the metrics cleanly
- Important features:
    1. Design the SQL schema
    2. Add JPA (Java Persistence API) entities
    3. Repository layer
    4. Save Metrics
    5. Fetch latest metrics
        - Create indexing on timestamps

# Read APIs (GET Endpoints)
- Expose the data for frontend consumption
- Important features:
    1. Expose GET Endpoints
        - GET /metrics/latest
        - GET /metrics?hostId=&from=&to=
    2. Query Filtering
    3. Pagination --> Break large datasets into smaller, manageable chunks (pages)
    4. Sorting --> allows clients to request the data in a specific order
        - sort by specific fields, in ascending or descending order

# React Frontend (Basic Implementation First)
- Visualize metrics
- Important features (implement in order):
    1. Static layout
    2. API client
    3. Fetch latest metrics
    4. Display values
    5. Auto refresh (polling)

# Charts and UX Improvements
- Provide a more clear and concise visualization system for the metrics
- Important features:
    1. Line charts for metrics
    2. Host selector
    3. Time range picker
    4. Error states

# Dockerization
- Dockerize the different components of the application
- Important dockerize order:
    1. Dockerize Java Backend
    2. Dockerize PostgreSQL
    3. Dockerize Python agent
    4. Dockerize React App
    5. Docker Compose

* Provides service isolation and networking between containers

# Kubernetes Deployment
- Deploy the application using Kubernetes
- Important deployment order:
    1. Deploy backend
    2. Deploy database
    3. Deploy frontend
    4. Services and ingress
    5. Scaling backend pods

* Helps with distinguishing between Pods vs Services, allows for a scaling strategy to   be formulated
