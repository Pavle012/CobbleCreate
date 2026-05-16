#!/usr/bin/env python3
"""
Mod update checker for Modrinth modpacks
Checks current versions vs latest versions on Modrinth
"""

import json
import requests
from pathlib import Path

def get_modrinth_project(project_id):
    """Get project info from Modrinth API"""
    try:
        response = requests.get(
            f"https://api.modrinth.com/v2/project/{project_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return None

def parse_version(mod_path):
    """Extract mod name and version from file path"""
    filename = Path(mod_path).name
    # Try to extract version from filename
    parts = filename.split('-')
    return filename, parts

def check_updates():
    """Check for mod updates"""
    
    # Load the index
    with open('modrinth.index.json', 'r') as f:
        index = json.load(f)
    
    print(f"\n📦 Checking updates for {index['name']} v{index['versionId']}")
    print("=" * 80)
    
    mods = index.get('files', [])
    print(f"Total mods: {len(mods)}\n")
    
    updates_available = 0
    
    for mod in mods:
        path = mod.get('path', '')
        if 'mods/' not in path:
            continue
            
        filename = Path(path).name
        
        # Extract mod ID from download URL
        downloads = mod.get('downloads', [])
        if not downloads:
            continue
        
        url = downloads[0]
        # Parse Modrinth URL to get project ID
        if 'modrinth.com/data/' in url:
            try:
                parts = url.split('/data/')[1].split('/')[0]
                project_id = parts
                
                project = get_modrinth_project(project_id)
                if project:
                    current_version = filename
                    latest_version = project.get('title', 'Unknown')
                    
                    print(f"✓ {project['name']}")
                    print(f"  Current: {filename}")
                    print(f"  Latest:  {project.get('title', 'N/A')}")
                    print()
                    
            except Exception as e:
                print(f"⚠ {filename} - Could not check: {str(e)[:50]}")
    
    print("=" * 80)
    print(f"Use 'packwiz update --all' to update all mods")

if __name__ == "__main__":
    check_updates()
