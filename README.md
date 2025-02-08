Password Brute-Force Tool - Project By RahulHackz
=================================================

Overview
--------

This tool demonstrates a basic brute-force attack implementation for educational purposes. It combines web scraping and HTTP request handling to automate login attempts against web forms.

### Key Features

*   Automatic form field detection ✅
*   Multiple header rotation ✅
*   Success condition detection ✅
*   Wordlist-based password guessing ✅

Dependencies
------------

    import os
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

*   **requests:** HTTP requests handling
*   **BeautifulSoup:** HTML parsing and DOM navigation
*   **urljoin:** URL resolution for form actions
*   **os:** File system operations for wordlist handling

Code Structure
--------------

### 1\. Configuration Constants

    USERNAME_FIELDS = ['username', 'email', ...]
    PASSWORD_FIELDS = ['password', 'pass', ...]
    SUBMIT_FIELDS = ['submit', 'login', ...]
    SUCCESS_INDICATORS = ['dashboard', 'account', ...]
    HEADERS_LIST = [...]

These lists contain patterns for identifying form elements and success conditions.

### 2\. Core Functions

#### detect\_login\_fields(url)

Identifies login form components through HTML analysis:

*   Form action URL detection
*   Input field identification using name/id attributes
*   Submit button detection

#### try\_requests(url, payload, headers\_list, method)

Handles HTTP requests with different headers and methods to bypass basic security measures.

#### brute\_force\_login(...)

Manages the brute-force process:

*   Wordlist handling
*   Payload construction
*   Success condition checking

Detailed Code Explanation
-------------------------

### Form Detection Logic

    form = soup.find('form')
    form_action = urljoin(url, form_action)

Uses BeautifulSoup's DOM parsing to find form elements and resolve relative URLs.

### Field Identification

    for input_tag in soup.find_all(['input', 'button']):
        input_name = input_tag.get('name', '').lower()
        # Field matching logic...

Prioritizes name attributes but falls back to id attributes for better compatibility.

### Header Rotation System

    HEADERS_LIST = [
        {'User-Agent': 'Chrome/114...'},
        {'User-Agent': 'Mac OS X...'}
    ]

Mimics different browsers to avoid basic User-Agent based blocking.

### Success Detection

    any(indicator in response.text.lower()...)
    response.history and any(...)

Checks both response content and redirect history for success indicators.

Tool Workflow
-------------

1.  URL input and validation
2.  Automatic form field detection
    *   HTML parsing with BeautifulSoup
    *   Pattern matching for field identification
3.  Manual field fallback
4.  Wordlist processing
5.  Brute-force execution
    *   Payload generation
    *   Header rotation
    *   Response analysis

Security Considerations
-----------------------

**Important:** This tool should only be used on authorized systems. Unauthorized use is illegal.  

#### You can use [https://rahulhackz.in/loginpage](https://rahulhackz.in/loginpage) to attack

Ethical Considerations
----------------------

*   Always obtain proper authorization
*   Use only on test systems you own
*   Follow the cybersecurity laws
*   Responsible disclosure principles

Testing & Debugging
-------------------

### Test Cases

*   Simple HTML forms
*   Multiple form pages
*   JavaScript-rendered forms (won't work)

### Debugging Tips

    # Uncomment these below lines in code for debugging:
    # print(f"\nResponse Status Code: {response.status_code}")
    # print(f"Response Text: {response.text}")

Conclusion
----------

This tool demonstrates basic brute-force attack principles while highlighting important security concepts. It serves as an educational resource for understanding:

*   Web form structure
*   HTTP request handling
*   Basic web security mechanisms

### Contact Information

If you face any issues you can contact me from:

*   Email: hi.rahulhackz@gmail.com
*   WhatsApp: [+917995041926](https://wa.me/917995041926)
*   Instagram: @rahulhackz @yourslovinglyrahul
*   Dont forget to subscribe to my youtube channel!  
    👉 [https://youtube.com/rahulhackz](https://youtube.com/rahulhackz) 👈
