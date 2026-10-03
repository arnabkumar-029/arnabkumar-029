import os
import requests
from datetime import datetime, timedelta

USERNAME = "arnabkumar-029"
TOKEN = os.environ["GITHUB_TOKEN"]

API_URL = "https://api.github.com/graphql"

query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            weekday
            contributionCount
            color
          }
        }
      }
    }
  }
}
"""

today = datetime.utcnow().date()
start = today - timedelta(days=364)

variables = {
    "login": USERNAME,
    "from": f"{start}T00:00:00Z",
    "to": f"{today}T23:59:59Z"
}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(
    API_URL,
    json={
        "query": query,
        "variables": variables
    },
    headers=headers
)

response.raise_for_status()

data = response.json()

if "errors" in data:
    raise Exception(data["errors"])

calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

weeks = calendar["weeks"]

# GitHub-style colors
EMPTY = "#161b22"

# SVG dimensions
CELL = 12
GAP = 4
STEP = CELL + GAP

LEFT = 35
TOP = 35

WIDTH = LEFT + (len(weeks) * STEP) + 10
HEIGHT = TOP + (7 * STEP) + 10

svg = []

svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{WIDTH}" height="{HEIGHT}" '
    f'viewBox="0 0 {WIDTH} {HEIGHT}">'
)

# Dark background
svg.append(
    f'<rect width="100%" height="100%" fill="#0d1117" rx="6"/>'
)

# Month labels
months_seen = set()

for week_index, week in enumerate(weeks):

    for day in week["contributionDays"]:

        date = datetime.strptime(
            day["date"],
            "%Y-%m-%d"
        ).date()

        if date.day <= 7:

            month_key = (date.year, date.month)

            if month_key not in months_seen:

                months_seen.add(month_key)

                x = LEFT + week_index * STEP

                month_name = date.strftime("%b")

                svg.append(
                    f'<text x="{x}" y="18" '
                    f'font-family="Arial, sans-serif" '
                    f'font-size="11" fill="#8b949e">'
                    f'{month_name}</text>'
                )

# Day labels
day_labels = {
    1: "Mon",
    3: "Wed",
    5: "Fri"
}

for weekday, label in day_labels.items():

    y = TOP + (weekday - 1) * STEP + 10

    svg.append(
        f'<text x="0" y="{y}" '
        f'font-family="Arial, sans-serif" '
        f'font-size="10" fill="#8b949e">'
        f'{label}</text>'
    )

# Contribution squares
for week_index, week in enumerate(weeks):

    for day in week["contributionDays"]:

        weekday = day["weekday"]
        count = day["contributionCount"]
        date = day["date"]
        color = day["color"]

        x = LEFT + week_index * STEP
        y = TOP + (weekday - 1) * STEP

        if count == 0:
            color = EMPTY

        tooltip = (
            f"{count} contribution"
            f"{'' if count == 1 else 's'} on "
            f"{datetime.strptime(date, '%Y-%m-%d').strftime('%B %-d, %Y')}"
        )

        # Windows-compatible date formatting
        tooltip = (
            f"{count} contribution"
            f"{'' if count == 1 else 's'} on "
            f"{datetime.strptime(date, '%Y-%m-%d').strftime('%B')} "
            f"{int(date[8:10])}, {date[:4]}"
        )

        svg.append(
            f'<rect x="{x}" y="{y}" '
            f'width="{CELL}" height="{CELL}" '
            f'rx="2" fill="{color}">'
            f'<title>{tooltip}</title>'
            f'</rect>'
        )

svg.append("</svg>")

with open("contribution-graph.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print("Contribution graph generated successfully.")
