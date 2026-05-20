import json
import requests
import sys
from datetime import datetime, timedelta

def fetch_contributions(username):
    url = f"https://api.github.com/users/{username}/contributions"
    today = datetime.now()
    start_date = today - timedelta(days=364)
    params = {'since': start_date.strftime('%Y-%m-%d'), 'until': today.strftime('%Y-%m-%d')}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching contributions: {response.status_code}")
        sys.exit(1)
    return response.json()

def generate_snake_svg(data, output_path, color_mode='normal'):
    days = data['contributions']
    grid = [['#ebedf0'] * 7 for _ in range(365 // 7 + 1)]
    
    for day in days:
        date = datetime.strptime(day['date'], '%Y-%m-%d')
        count = day['count']
        week = (date - datetime(2025, 1, 1)).days // 7
        if week < len(grid):
            col = date.weekday()
            if count > 0:
                if count >= 9:
                    grid[week][col] = '#58a6ff' if color_mode == 'normal' else '#00f5d4'
                elif count >= 5:
                    grid[week][col] = '#9be9a8' if color_mode == 'normal' else '#00f5d4'
                elif count >= 3:
                    grid[week][col] = '#40c463' if color_mode == 'normal' else '#00f5d4'
                elif count >= 1:
                    grid[week][col] = '#30a14e' if color_mode == 'normal' else '#00f5d4'

    svg = '<?xml version="1.0" encoding="UTF-8"?>\n'
    svg += '<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 770 505" fill="none">\n'
    svg += f'  <rect width="770" height="505" fill="#{color_mode if color_mode == "neon" else "0d1117"}"/>\n'
    
    for week in range(len(grid)):
        for col in range(7):
            x = col * 16 + week * 16 + 10
            y = week * 16 + 10
            svg += f'  <rect x="{x}" y="{y}" width="15" height="15" rx="2" fill="{grid[week][col]}"/>\n'
    
    svg += '</svg>'
    
    with open(output_path, 'w') as f:
        f.write(svg)
    print(f"Snake generated: {output_path}")

if __name__ == '__main__':
    username = 'Serpentum'
    data = fetch_contributions(username)
    generate_snake_svg(data, 'output/github-snake.svg', 'normal')
    generate_snake_svg(data, 'output/github-snake-neon.svg', 'neon')
