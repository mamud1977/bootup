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
