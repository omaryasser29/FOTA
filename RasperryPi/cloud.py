import requests
from supabase import create_client, Client


"""------------------------------------------ Global Variables -------------------------------------------"""

#__________________ URL for uploading the file (Supabase upload URL)

# URL for the file 
FileURL = "https://wngqbymqpbrcpgtuqetr.supabase.co/storage/v1/object/sign/FOTA_DATA/User_App.bin?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJGT1RBX0RBVEEvVXNlcl9BcHAuYmluIiwiaWF0IjoxNzM0MjA2NjAyLCJleHAiOjE3NjU3NDI2MDJ9.h8ujQF30kVEZJjZVXbX15kaPLr6zi1cYOLVWzoU57zc&t=2024-12-14T20%3A03%3A22.478Z"

# API KEY
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InduZ3FieW1xcGJyY3BndHVxZXRyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNDIwMDM3MiwiZXhwIjoyMDQ5Nzc2MzcyfQ.9hTOd76a0rjjiZOZy8Hb6GKP0JXWCz6qyx4lQtoFgFU"

# Headers for the request
headers = { "Authorization": API_KEY}

# URL for Database
SUPABASE_URL = "https://wngqbymqpbrcpgtuqetr.supabase.co"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, API_KEY)


"""--------------------------------------------- Functions --------------------------------------------"""
#__________________ Function to upload the file

def download_file():
    print("Starting file download...")

    try:
        # Send GET request
        response = requests.get(FileURL)

        print("HTTP Response Code:", response.status_code)

        if response.status_code == 200:
            # Open file for writing (using LittleFS or other filesystem)
            try:
                with open("code.bin", 'wb') as file:
                    # Write the response content to the file
                    file.write(response.content)
                    print("File downloaded")
            except OSError as e:
                print("Failed to open file for writing:", e)
                return False
        else:
            print(f"Error in HTTP request: {response.status_code}")
            return False

    except Exception as e:
        print("Exception occurred during download:", e)
        return False

    return True

# Remove the Bin File From Cloud 
def remove_file_from_cloud():
    try:
        # Perform file deletion
        response = supabase.storage.from_("FOTA_DATA").remove("User_App.bin")

        # Check response
        if response:
            print("Filesuccessfully deleted from Supabase.")
            return True
        else:
            print(f"Failed to delete file.")
            return False

    except Exception as e:
        print(f"Error during file deletion: {e}")
        return False
    
# Check the value in the Supabase database
def check_value():

    # Create the URL with API key as a query parameter
    api_url = f"{SUPABASE_URL}/rest/v1/FOTA?select=value&apikey={API_KEY}"
    
    # Make a GET request to fetch data
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        # If the request is successful, parse the response
        response_data = response.json()
        
        # Extract the 'value' field
        value = response_data[0]["value"]
        return value
    else:
        print(f"Failed to fetch data, error code: {response.status_code}")
        return 400

# Update the value in the Supabase database
def update_value_to_zero():
    # Fetch the first (and only) row
    response = supabase.table("FOTA").select("value").limit(1).execute()
    
    # Correct way to access data
    data = response.data

    if not data:
        print("No rows found to update.")
        return False

    # Perform the update operation on the first row
    update_response = (
        supabase.table("FOTA")
        .update({"value": 0})
        .neq("value", 0)  # Ensures only rows where value != 0 are updated
        .execute()
    )

    # Correct way to access update data
    updated_data = update_response.data

    if updated_data:
        print("Value updated to 0 successfully:", updated_data)
        return True
    else:
        print("Update failed:", update_response)
        return False
    
