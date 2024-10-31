# GithubUserDataAnalysis
Scrapping user data using github api under a particular condition like locations and followers count
## How Scrapping Done ?

- **Data Collection:** The data was collected by querying the GitHub API for users in the given location:Seattle with over 200 followers. In ordered to not exceed the rate limit of github api we used time module to wait for 1 second and called the api . We also used 30 datas per page to carefully handle the rate limit.
- **Extracting User Data** Once the initial data is collected next we called another function to fetch the required user data that is mentioned in the details by forwarding username which is obtained from `data collection` to the `get_user_detail()`
-  **Extracting User Repository Data** The nested list comprehension starts by iterating over each user in the `detailed_users` list. For each user, it calls the function `get_user_repositories(user["login"])` to retrieve that user’s list of repositories. It then iterates over each repository in this list, adding each repository to the final `repositories` list. This process continues until all repositories from all users have been collected in one comprehensive list.
-  ** Writing CSV Files ** we iterrate over the both user data and repository data list and then by using `csv.writerow()` we write the data

---
## Intresting Fact
Analysis revealed a positive correlation between the length of a user’s bio and their follower count, suggesting that detailed bios might attract more followers.

## Recommendation for Developers: 
To increase engagement, developers should consider adding descriptive, relevant content to their GitHub bios to enhance visibility and follower growth.



