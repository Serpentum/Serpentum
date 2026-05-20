import json
import os
import requests
import sys
from datetime import datetime, timedelta

def fetch_contributions(username):
    query = """
    {
      user(login: "%s") {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """ % username
    
    headers = {}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
        headers['Content-Type'] = 'application/json'
    
    response = requests.post('https://api.github.com/graphql', headers=headers, json={'query': query})
    if response.status_code != 200:
        print(f"GraphQL Error: {response.status_code} - {response.text}")
        sys.exit(1)
    
    result = response.json()
    if 'data' not in result:
        print(f"GraphQL Error: {result}")
        sys.exit(1)
    
    cal = result['data']['user']['contributionsCollection']['contributionCalendar']
    contributions = []
    for week in cal['weeks']:
        for day in week['contributionDays']:
            contributions.append({
                'date': day['date'],
                'count': day['contributionCount']
            })
    
    return contributions

def generate_snake(data, output_path, color_mode='normal'):
    color_map = {
        0: '#ebedf0',
        1: '#9be9a8',
        2: '#40c463',
        3: '#30a14e',
        4: '#256b39'
    }
    
    if color_mode == 'neon':
        color_map = {
            0: '#0d1117',
            1: '#00f5d4',
            2: '#00f5d4',
            3: '#00f5d4',
            4: '#00f5d4'
        }
    
    cell_size = 16
    gap = 3
    offset_x = 10
    offset_y = 10
    cols = 7
    rows = 53
    
    svg_width = cols * (cell_size + gap) + offset_x * 2
    svg_height = rows * (cell_size + gap) + offset_y * 2
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="{color_map[0]}">
'''
    
    for i, day in enumerate(data):
        week = i // cols
        col = i % cols
        if week >= rows:
            break
        x = offset_x + col * (cell_size + gap)
        y = offset_y + week * (cell_size + gap)
        count = day['count']
        color = color_map[min(count, 4)]
        svg += f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="{2}" fill="{color}"/>\n'
    
    svg += '</svg>'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {output_path}")

if __name__ == '__main__':
    contributions = fetch_contributions('Serpentum')
    generate_snake(contributions, 'output/snake.svg', 'normal')
    generate_snake(contributions, 'output/snake-neon.svg', 'neon')
