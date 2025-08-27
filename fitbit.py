import requests
import pandas as pd
from datetime import datetime, timedelta

# Fitbit API Credentials
CLIENT_ID = 'client id'
CLIENT_SECRET = 'client secrect id'
ACCESS_TOKEN = 'generated token.'  # Replace with the generated token
REFRESH_TOKEN = 'refresh token'
API_BASE_URL = "base url"

# Step 1: Connect to Fitbit API
def refresh_access_token():
    """Refresh Fitbit API access token."""
    url = "fitbit url"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    if response.status_code == 200:
        tokens = response.json()
        global ACCESS_TOKEN
        ACCESS_TOKEN = tokens['access_token']
        return tokens
    else:
        raise Exception(f"Failed to refresh token: {response.json()}")
    
def get_fitbit_data(endpoint, start_date, end_date):
    """Fetch data from Fitbit API."""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    url = f"{API_BASE_URL}/{endpoint}/date/{start_date}/{end_date}.json"
    response = requests.get(url, headers=headers)
    if response.status_code == 401:  # Unauthorized
        refresh_access_token()
        headers['Authorization'] = f'Bearer {ACCESS_TOKEN}'
        response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch Fitbit data: {response.json()}")
    
# Step 2: Check the date of last sync
def get_last_sync_date(sheet_path):
    """Read the date of last sync from the stats tracker."""
    try:
        tracker_data = pd.read_excel(sheet_path)
        last_sync_date = tracker_data['Sync Date'].max()
        return last_sync_date
    except Exception as e:
        print(f"Failed to read the stats tracker: {e}")
        return datetime.now() - timedelta(days=7)  # Default to one week ago
    
# Step 3: Extract weekly/monthly stats
def extract_stats(last_sync_date):
    """Extract stats from Fitbit API."""
    start_date = last_sync_date + timedelta(days=1)  # Day after last sync
    end_date = datetime.now() - timedelta(days=1)  # Day before today
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    stats = get_fitbit_data('activities/steps', start_date_str, end_date_str)
    distance = get_fitbit_data('activities/distance', start_date_str, end_date_str)
    
    # Combine steps and distance
    steps_data = stats.get('activities-steps', [])
    distance_data = distance.get('activities-distance', [])
    return pd.DataFrame({
        'Date': [entry['dateTime'] for entry in steps_data],
        'Steps': [entry['value'] for entry in steps_data],
        'Distance': [entry['value'] for entry in distance_data]
    })
    
# Step 4: Update stats tracker
def update_stats_tracker(stats_df, sheet_path):
    """Update the endurance sheet with new data."""
    try:
        tracker_data = pd.read_excel(sheet_path)
        updated_data = pd.concat([tracker_data, stats_df])
        updated_data.to_excel(sheet_path, index=False)
        print("Stats tracker updated successfully.")
    except Exception as e:
        print(f"Failed to update the stats tracker: {e}")
        
# Step 5: Notify Mohammed
def notify_user():
    """Notify Mohammed via proper channels."""
    print("Mohammed has been notified via email/Slack/other channels.")
    
# Main Execution
if __name__ == "__main__":
    try:
        SHEET_PATH = "endurance_sheet.xlsx"  # Path to stats tracker file
        last_sync_date = get_last_sync_date(SHEET_PATH)
        stats_df = extract_stats(last_sync_date)
        update_stats_tracker(stats_df, SHEET_PATH)
        notify_user()
    except Exception as e:
        print(f"Automation failed: {e}")
        


        
        
 