from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


# submit name and age
@app.route("/submitGitName", methods=["POST"])
def submitGitName():
    input_name = request.form.get("gitname")

    # sent the request to the github
    response = requests.get(f"https://api.github.com/users/{input_name}/repos")

    if response.status_code == 200:
        repos = response.json()
        repo_info = []

        for repo in repos:
            repo_name = repo["fullname"]
            repo_update = repo["updated_at"]
            star_count = repo["stargazers_count"]

            languages_response = requests.get(f"https://api.github.com/repos/{repo_name}/languages")             
            # Check if the languages request is successful
            if languages_response.status_code == 200:                 
                languages = languages_response.json()  # Parse JSON data into a dictionary of languages
                # Get the names of the languages used                
                language_names = list(languages.keys()) 
                
            else: 
                language_names = [] # Empty list if unable to fetch languages

            collaborators_response = requests.get(f"https://api.github.com/repos/{repo_name}/collaborators")             
            # Check if the collaborators request is successful
            if collaborators_response.status_code == 200:                 
                collaborators = collaborators_response.json()  # Parse JSON data into a list of collaborators
                # Extract collaborator names                
                collaborator_names = [collaborator["login"] for collaborator in collaborators] 
                
            else: 
                collaborator_names = [] # Empty list if unable to fetch collaborators

            # get commit list
            commits_response = requests.get(f"https://api.github.com/repos/{repo_name}/commits")             
            # Check if the commits request is successful
            if commits_response.status_code == 200:                 
                commits = commits_response.json()  # Parse JSON data into a list of commits
                # Get the latest commit hash
                if commits:  
                    latest_commit = commits[0]                  
                    latest_commit_hash = latest_commit["sha"]  # Get the SHA of the latest commit
                    latest_commit_message = latest_commit["commit"]["message"] # Get the message
                    latest_commit_author = latest_commit["commit"]["author"]["name"]
                else:
                    latest_commit_hash = None # No commits found
                    latest_commit_message = None
                    latest_commit_author = None

            else:
                latest_commit_hash = None
                latest_commit_message = None 
                latest_commit_author = None
            
            repo_info.append(
                {"name": repo_name, "updated_at": repo_update,  
                "collaborators": collaborator_names, "latest_commit_hash": latest_commit_hash, 
                "latest_commit_message": latest_commit_message, "latest_commit_author": latest_commit_author}, 
                "language": languages, "stars": star_count)
 


    return render_template("helloGit.html", gitname=input_name, repositories = repo_info)


# submit name and age
@app.route("/submitNameAge", methods=["POST"])
def submitNameAge():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


def process_query(q):
    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"

    else:
        return "Unknown"


# get the dinosaurs
@app.route("/query", methods=["GET"])
def query():
    q = request.args.get("q")
    response = process_query(q)

    return response