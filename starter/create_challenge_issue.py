import requests
import json
import datetime
import sys


if len(sys.argv) == 1:
    print("no system arguments")
    exit()

GH_TOKEN = sys.argv[1]
OWNER = sys.argv[2]
OWN_REPOSITORY_NAME = sys.argv[3]

GH_API_BASED_URL = "https://api.github.com"
GH_API_BASED_HEADERS = {
    "Authorization": "Bearer {}".format(GH_TOKEN),
    "X-GitHub-Api-Version": "2022-11-28",
    "Accept": "application/vnd.github+json"
}

SOLVED_AD_API_URL = "https://solved.ac/api/v3/problem/show"


def read_latest_solved_commit_info():
    read_commit_endpoint = GH_API_BASED_URL + "/repos/{}/{}/commits".format(OWNER, OWN_REPOSITORY_NAME)

    parameters = {"per_page": 1, "page": 1}
    response = requests.get(
        read_commit_endpoint,
        headers=GH_API_BASED_HEADERS,
        params=parameters
    ).json()

    return {
        "commit_message": response[0]["commit"]["message"],
        "commit_url": response[0]["html_url"]
    }


def get_problem_info(problem_id):
    levels = {
        0: "U",
        1: "B5", 2: "B4", 3: "B3", 4: "B2", 5: "B1",
        6: "S5", 7: "S4", 8: "S3", 9: "S2", 10: "S1",
        11: "G5", 12: "G4", 13: "G3", 14: "G2", 15: "G1",
        16: "P1", 17: "P2", 18: "P3", 19: "P2", 20: "P1",
    }

    parameters = {"problemId": problem_id}

    response = requests.get(
        SOLVED_AD_API_URL,
        params=parameters
    ).json()

    return {
        "problem_id": response["problemId"],
        "problem_name": response["titleKo"],
        "problem_level": levels[response["level"]],
        "problem_tag": response["tags"][0]["key"],
    }


def create_issue_template(problem_info, solution_code):
    date = datetime.datetime.now().date()
    formatted_date = date.strftime("%Y.%m.%d")

    issue_title_format = "[solve] {} - @{}"
    issue_title = issue_title_format.format(formatted_date, OWNER)

    issue_body_format = (
        "## {}  \n"
        "- **author** : @{}  \n"
        "- **platform** : baekjoon online judge  \n"
        "- **problem info**  \n"
        "  - **number** : {}  \n"
        "  - **link** : [https://www.acmicpc.net/problem/{}](https://www.acmicpc.net/problem/{})  \n"
        "  - **name** : {}  \n"
        "  - **rank** : `{}`  \n"
        "  - **category** : `{}`  \n"
        "- [**browse code**]({})  \n"
    )
    issue_body = issue_body_format.format(
        formatted_date,
        OWNER,
        problem_info["problem_id"],
        problem_info["problem_id"], problem_info["problem_id"],
        problem_info["problem_name"],
        problem_info["problem_level"],
        problem_info["problem_tag"],
        solution_code
    )

    return {
        "title": issue_title,
        "body": issue_body
    }


def create_new_issue(issue_template):
    create_issue_endpoint = "https://api.github.com/repos/unsolved-ac/challenge/issues"

    body = {
        "title": issue_template["title"],
        "body": issue_template["body"],
        "labels": ["solved"]
    }

    response = requests.post(
        create_issue_endpoint,
        headers=GH_API_BASED_HEADERS,
        data=json.dumps(body)
    ).json()

    return response["html_url"]


def main():
    latest_commit_info = read_latest_solved_commit_info()
    latest_commit_message = latest_commit_info["commit_message"]
    solution_code = latest_commit_info["commit_url"]

    if not latest_commit_message.startswith("solve"):
        print("this commit is not solved commit")
        return

    solved_problem_number = latest_commit_message.split()[2]

    problem_info = get_problem_info(solved_problem_number)

    issue_template = create_issue_template(problem_info, solution_code)
    issue_url = create_new_issue(issue_template)
    print(issue_url)


main()
