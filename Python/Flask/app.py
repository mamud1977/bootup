from github import Github
from flask import Flask, request
from github import GithubException
from configparser import ConfigParser

config = ConfigParser()
config.read('config.txt')
git_token = config["dev"]["git_token"]
g = Github(git_token)

app = Flask(__name__)

@app.get("/org/<string:orgname>")   
def get_org_by_name(orgname):
    
    try:
        org_name = orgname
        org = g.get_organization(org_name)

        # List organization members
        members = org.get_members()
        members_list = []
        for member in members:
            members_list.append(member.login)

        # Get organization repositories
        repos = org.get_repos()

        original_repos = []
        forked_repos = []

        # Iterate through each repository
        repository_list =[]
        for repo in repos:

            if repo.fork:
                original_repos = False
                forked_repos = True
            else:
                original_repos = True
                forked_repos = False
            
            # Print the number of watchers
            watchers_count = repo.watchers_count

            # Get the list of languages
            languages = repo.get_languages()
            languages_list =[]
            for language in languages:
                languages_list.append(language)

            repository = {
                "RepositoryName": repo.name,
                "original_repos": original_repos,
                "forked_repos": forked_repos,
                "watchers_count": watchers_count,
                "languages_list": languages_list
            }
        
            repository_list.append(repository)
        
        GithubOrganization = {
                "OrganizationName": org.name,
                "OrganizationID": org.id,
                "Description": org.description,
                "PublicRepos": org.public_repos,
                "PrivateRepos": org.total_private_repos,
                "Members": members_list,
                "Repositories": repository_list
            }

        return GithubOrganization
    except GithubException as e:
        return {"status": f"Error accessing GitHub API: {e.status} - {e.data['message']}"}
    except Exception as e:
        return {f"An unexpected error occurred: {e}"}   
    

# Inprogress
@app.post("/org/<string:repo_owner>/fork")  
def create_forked_repo(repo_owner):
    
    try:
        request_data = request.get_json()
        repo_owner = request_data["repo_owner"]
        repo_name = request_data["repo_name"]
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        
        github_user = g.get_user()
        
        #myfork = github_user.create_fork(repo)

        
        #repo = g.get_repo(f"{repo_owner}/{repo_name}")
        
        return {
            "repo_owner": repo_owner, 
            "repo_name": repo_name}
        


        # Replace with your desired username for the forked repository

        # fork = repo.create_fork(user)

        # Optional: Verify that the fork was created successfully
      
    # return 'Store not found', 404
        
    except Exception as e:
        return {f"Exception: {e}"}
    