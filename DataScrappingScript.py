import pandas as pd 
import requests
import time
import csv

token="YOUR_API_KEY"
headers={'Authorization':f"token {token}"}
BASE_URL = "https://api.github.com"
location='seattle'
min_followers=200
query=f"location%3A{location}%20followers%3A%3E{min_followers}"

def get_user_data():
    total_data = []
    page = 1

    while True:
        # GitHub search query for users in Seattle with 200+ followers
        url = f"{BASE_URL}/search/users?q={query}&per_page=30&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 403:  # Rate limit exceeded
            reset_time = int(response.headers.get("X-RateLimit-Reset"))
            wait_time = max(reset_time - int(time.time()), 0)
            print(f"Rate limit hit. Waiting for {wait_time} seconds...")
            time.sleep(wait_time + 10)  # Wait for the reset plus a buffer
            continue

        data = response.json()
        if "items" in data:
            total_data.extend(data["items"])
        else:
            print("Error:", data)
            break

        if len(data["items"]) < 30:
            break  # Break when there are no more results

        page += 1
        time.sleep(1)  # To avoid hitting the rate limit

    return total_data

def get_user_details(username):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_user_repositories(username,):
    url = f'https://api.github.com/users/{username}/repos?per_page=500'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Write users.csv
def write_users_csv(users):
    with open('user.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        for user in users:
            writer.writerow([
                user['login'],
                user.get('name', ''),
                user['company'].strip().lstrip('@').upper() if user.get('company') else '',
                user.get('location', ''),
                user.get('email', ''),
                user.get('hireable', False),  
                user.get('bio', ''),
                user['public_repos'],
                user['followers'],
                user['following'],
                user['created_at']
            ])

def write_repositories_csv(repositories):
    with open('repositories.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])
        for repo in repositories:
            writer.writerow([
                repo['owner']['login'],
                repo['full_name'],
                repo['created_at'],
                repo['stargazers_count'],
                repo['watchers_count'],
                repo.get('language', ''),  
                repo.get('has_projects', False),  
                repo.get('has_wiki', False), 
                repo['license']['key'] if repo.get('license') else ''  
            ])

def main():
    try:
        users = get_user_data()
        
        detailed_users = [get_user_details(user['login']) for user in users]
        
        repositories = [repo for user in detailed_users for repo in get_user_repositories(user['login'])]
        
        write_users_csv(detailed_users)
        write_repositories_csv(repositories)
        
        print("Data scraped successfully and written to users.csv and repositories.csv")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
