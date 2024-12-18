import subprocess
import os
import sys
import requests

def check_proxy(proxy):
    """
    Check if the proxy is working by making a simple HTTP request.
    Args:
        proxy (str): The proxy in the format 'ip:port'.
    Returns:
        bool: True if the proxy is working, False otherwise.
    """
    test_url = "http://www.google.com"  # You can use any URL to test the proxy
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)  # Timeout after 5 seconds
        return response.status_code == 200  # Proxy is valid if we get a successful response
    except requests.RequestException:
        return False  # If any exception occurs, consider the proxy invalid

def open_url_with_proxies(url, proxies, browser_count):
    """
    Opens the given URL in the specified number of Chrome browsers with different profiles and proxies.
    
    Args:
        url (str): The URL to open.
        proxies (list): List of proxies to use for each browser instance.
        browser_count (int): The number of Chrome browsers to open with the URL.
    """
    # Path to the Chrome executable
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update with the correct path

    # Ensure the path exists
    if not os.path.exists(chrome_path):
        print(f"Error: Chrome executable not found at {chrome_path}")
        sys.exit(1)

    # Base directory for Chrome user data
    base_user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\CustomProfiles")

    # Create the base directory if it doesn't exist
    if not os.path.exists(base_user_data_dir):
        os.makedirs(base_user_data_dir)

    for i in range(browser_count):
        # Generate a unique profile directory for each instance
        profile_dir = os.path.join(base_user_data_dir, f"Profile_{i}")

        # Create a new proxy server for each browser instance
        proxy = proxies[i % len(proxies)]  # Ensure that proxies list is cycled if more browsers are requested than proxies

        # Launch Chrome with the specified profile and proxy
        print(f"Opening URL in Chrome instance {i+1} with Proxy {proxy} and Profile {i+1}")
        subprocess.Popen([chrome_path, 
                          f"--user-data-dir={base_user_data_dir}", 
                          f"--profile-directory=Profile_{i}", 
                          f"--proxy-server=http://{proxy}", 
                          "--new-window", 
                          url])

def read_proxies_from_file(file_path):
    """
    Read proxies from a file, one per line.
    Args:
        file_path (str): The path to the proxy file.
    Returns:
        list: A list of proxies from the file.
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

if __name__ == "__main__":
    try:
        url = input("Enter the URL to open: ")
        num_browsers = int(input("Enter the number of browsers to open: "))
        proxy_file = 'proxy.txt'  # Path to your proxy.txt file

        # Read proxies from the file
        proxies = read_proxies_from_file(proxy_file)

        # Filter out invalid proxies
        valid_proxies = [proxy for proxy in proxies if check_proxy(proxy)]
        if not valid_proxies:
            print("No valid proxies found. Exiting.")
            sys.exit(1)

        if num_browsers <= 0:
            print("Please enter a positive number.")
        else:
            # If there are fewer valid proxies than the number of browsers, cycle through the valid proxies
            open_url_with_proxies(url, valid_proxies, num_browsers)

    except ValueError:
        print("Invalid input. Please enter a valid number.")
