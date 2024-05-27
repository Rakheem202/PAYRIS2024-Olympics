import time
import random
import csv
from datetime import datetime, timedelta

# Define resources, response codes, events, and some example user demographics
resources = ["/index.html", "/images/games.jpg", "/searchsports.php", "/Athletics.html", "/football.html", "/basketball.html", "/tennis.html", "/cycling.html", "/boxing.html", "/fencing.html", "/rowing.html", "/swimming.html", "/volleyball.html", "/gymnastics.html"]
response_codes = [200, 301, 304, 404, 500]
events = ["Live", "Recorded"]
sports = ["Football", "Basketball", "Tennis", "Swimming", "Athletics", "Cycling", "Boxing", "Fencing", "Rowing", "Volleyball", "Gymnastics"]
countries = ["USA", "Canada", "UK", "Germany", "France", "Botswana", "South Africa", "Ghana", "Jamaica", "Japan", "Australia", "China"]
genders = ["Male", "Female"]
age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]

# Function to generate a random IP address
def generate_ip():
  return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

# Function to generate a random user ID
def generate_user_id():
  return f"UID{random.randint(1000, 9999)}"

# Function to generate a random session ID
def generate_session_id():
  return f"SID{random.randint(1000, 9999)}"

# Function to generate a random page view count
def generate_page_view():
  return random.randint(1, 10)


# Function to generate a log entry
def generate_log_entry():
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  ip_address = generate_ip()
  user_id = generate_user_id()
  session_id = generate_session_id()
  page_view = generate_page_view()
  request_type = "GET"
  resource = random.choice(resources)
  response_code = random.choice(response_codes)
  event = random.choice(events)
  sport = random.choice(sports)
  country = random.choice(countries)
  gender = random.choice(genders)
  age_group = random.choice(age_groups)
  visit_duration = random.randint(1, 120)# Duration in minutes
  session_start = datetime.now()  # Capture session start time
  return [timestamp, ip_address, user_id, session_id, page_view, request_type, resource, response_code, event, sport, country, gender, age_group, visit_duration, session_start]

# Function to write log entry to CSV file
def write_to_csv(file_name, entry):
  with open(file_name, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(entry)

# Main function to generate logs indefinitely
def generate_logs(file_name):
  global concurrent_viewers, unique_viewers, peak_viewers, user_watch_times
  concurrent_viewers = 0
  unique_viewers = set()
  peak_viewers = 0
  user_watch_times = {}  # Dictionary to store user watch times

  while True:
    log_entry = generate_log_entry()
    print(log_entry)
    write_to_csv(file_name, log_entry)

    # Update viewer metrics
    concurrent_viewers += 1
    peak_viewers = max(peak_viewers, concurrent_viewers)
    unique_viewers.add(log_entry[2])

    # Update watch time (if session ends)
    session_id = log_entry[3]
    if session_id not in user_watch_times:
      user_watch_times[session_id] = log_entry[14]
    else:
      watch_time = (datetime.now() - user_watch_times[session_id]).seconds / 60
      # Update a separate data structure for watch time
            # Update watch time (if session ends)
      watch_time = (datetime.now() - user_watch_times[session_id]).seconds / 60
      concurrent_viewers -= 1
      del user_watch_times[session_id]
      # You can store the watch time in a separate data structure for further analysis

    # Update content performance metrics (basic example)
    resource = log_entry[6]
    if resource not in content_performance:
        content_performance[resource] = 0
    content_performance[resource] += 1  # Increment counter for accessed resource

    time.sleep(5)

# Define additional data structures
content_performance = {}  # Dictionary to track resource access counts

if __name__ == "__main__":
  # Define the CSV file name
  csv_file_name = "Paris2024.csv"

  # Write header to CSV file
  with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "IP Address", "user_id", "session_id", "page_view", "Request Type", "Resource", "Response Code", "Event", "Sport", "Country", "Gender", "Age Group", "Visit Duration", "Session Start"])

  # Generate logs indefinitely
  generate_logs(csv_file_name)

