from github import Github

# Replace 'YOUR_TOKEN' with your actual personal access token
token = <>
g = Github(token)


    
# or using username and password
# g = Github("mamud1977", "zeenat02$")

print(g)

user = g.get_user()

print(user)

repos = user.get_repos()

for repo in repos:
    print(repo.name)