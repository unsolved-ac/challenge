import requests
import json
import sys


if len(sys.argv) == 1:
    print("no system arguments")
    exit()

GH_TOKEN = sys.argv[1]
GH_API_BASED_URL = "https://api.github.com"
GH_API_BASED_HEADERS = {
    "Authorization": "Bearer {}".format(GH_TOKEN),
    "X-GitHub-Api-Version": "2022-11-28",
    "Accept": "application/vnd.github+json"
}


def get_opened_issues_number():
    get_issues_endpoint = GH_API_BASED_URL + "/repos/unsolved-ac/challenge/issues"
    parameter = {
        "state": "open"
    }
    response = requests.get(get_issues_endpoint, headers=GH_API_BASED_HEADERS, params=parameter).json()
    return [issue["number"] for issue in response]


def close_opened_issues(issue_numbers):
    for issue_number in issue_numbers:
        update_issue_endpoint = GH_API_BASED_URL + "/repos/unsolved-ac/challenge/issues/{}".format(issue_number)
        body = {
            "state": "close"
        }
        requests.patch(
            update_issue_endpoint,
            headers=GH_API_BASED_HEADERS,
            data=json.dumps(body)
        ).json()


def main():
    opened_issues_number = get_opened_issues_number()
    close_opened_issues(opened_issues_number)
    print("success")


main()

