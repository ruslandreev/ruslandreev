import os
import requests

ORG_NAME = "datekt" 
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def get_org_stats(org):
    org_url = f"https://github.com{org}"
    org_res = requests.get(org_url, headers=headers)
    
    if org_res.status_code != 200:
        print(f"Ошибка получения данных организации: {org_res.status_code}")
        return 0, 0, 0, "Ошибка API"
        
    org_data = org_res.json()
    followers = org_data.get("followers", 0)
    
    repos_url = f"https://github.com{org}/repos?per_page=100"
    repos_res = requests.get(repos_url, headers=headers)
    
    if repos_res.status_code != 200:
        print(f"Ошибка получения репозиториев: {repos_res.status_code}")
        return 0, 0, followers, "Ошибка API"
        
    repos = repos_res.json()
    
    total_repos = len(repos)
    total_stars = 0
    last_updated_repo = "Нет репозиториев"
    latest_time = ""

    for repo in repos:
        total_stars += repo.get("stargazers_count", 0)
        
        updated_at = repo.get("updated_at", "")
        if updated_at > latest_time:
            latest_time = updated_at
            last_updated_repo = repo.get("name", "")

    return total_repos, total_stars, followers, last_updated_repo

repos_count, stars_count, followers_count, last_repo = get_org_stats(ORG_NAME)

svg_template = f"""<svg width="450" height="200" viewBox="0 0 450 200" fill="none" xmlns="http://w3.org">
  <style>
    .title {{ font: bold 16px 'Segoe UI', Ubuntu, Sans-Serif; fill: #58a6ff; }}
    .text {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #c9d1d9; }}
    .value {{ font: bold 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #f0883e; }}
    .border {{ stroke: #30363d; stroke-width: 1.5; }}
    .bg {{ fill: #0d1117; rx: 10; }}
  </style>
  <rect width="450" height="200" class="bg border"/>
  
  <text x="25" y="35" class="title">Статистика организации @{ORG_NAME}</text>
  
  <text x="25" y="75" class="text">Публичные репозитории:</text>
  <text x="220" y="75" class="value">{repos_count}</text>
  
  <text x="25" y="105" class="text">Всего звёзд (Stars):</text>
  <text x="220" y="105" class="value">⭐ {stars_count}</text>
  
  <text x="25" y="135" class="text">Подписчики (Followers):</text>
  <text x="220" y="135" class="value">👤 {followers_count}</text>
  
  <text x="25" y="165" class="text">Последний измененный:</text>
  <text x="220" y="165" class="value" fill="#58a6ff">📦 {last_repo}</text>
</svg>
"""

with open("org_stats.svg", "w", encoding="utf-8") as f:
    f.write(svg_template)

print("Файл org_stats.svg успешно обновлен!")