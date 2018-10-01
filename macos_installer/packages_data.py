#!/usr/bin/env python3

import json

TEST_PACKAGES_DATA="""
[
    {"full_name": "Atom Editor 1.31.1", "name": "atom", "package_type": "brewcask", "state" : "present" },
    {"full_name": "lzip 1.2.0", "name": "lzip", "package_type": "brew", "state" : "absent" },
    {"full_name": "Keep It (1.5.2)", "name": "Keep It", "package_type": "mas", "mas_id": "1272768911" , "state" : "absent" }     
]
""".strip()

FAILING_PACKAGES_DATA="""
    {"full_name": "HMA Pro VPN", "name": "hma-pro-vpn", "package_type": "brewcask", "state" : "present",
     "secondary": "open '/usr/local/Caskroom/hma-pro-vpn/3.2.11.2/Install HMA! Pro VPN.app'"}
""".strip()

PACKAGES_DATA="""
[
    {"full_name": "iTerm2 (3.2.1)", "name": "iterm2", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Google Chrome", "name": "google-chrome", "package_type": "brewcask", "state" : "present" },
    {"full_name": "1Password 7", "name": "1Password 7", "package_type": "mas", "mas_id": "1333542190", "state" : "present" },
    {"full_name": "Airmail 3 (3.6.41)", "name": "Airmail 3", "package_type": "mas", "mas_id": "918858936", "state" : "present" },
    {"full_name": "Contacts for Google", "name": "Contacts for Google", "package_type": "mas", "mas_id": "1127748291", "state" : "present" },
    {"full_name": "GCal for Google Calendar", "name": "GCal for Google Calendar", "package_type": "mas", "mas_id": "1107163858", "state" : "present" },
    {"full_name": "Simplenote (1.3.7)", "name": "Simplenote", "package_type": "mas", "mas_id": "692867256", "state" : "present" },
    {"full_name": "Sublime Text", "name": "sublime-text", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Vox", "name": "vox", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Backup and Sync from Google", "name": "google-backup-and-sync", "package_type": "brewcask", "state" : "present" },
    {"full_name": "DaisyDisk", "name": "DaisyDisk", "package_type": "mas", "mas_id": "411643860", "state" : "present" },
    {"full_name": "Notes for Google Keep", "name": "Notes for Google Keep", "package_type": "mas", "mas_id": "981433563", "state" : "present" },
    {"full_name": "MacDown", "name": "macdown", "package_type": "brewcask", "state" : "present" },
    {"full_name": "monosnap", "name": "monosnap", "package_type": "mas", "mas_id": "540348655", "state" : "present" },           
    {"full_name": "Photo Meta Edit", "name": "Photo Meta Edit", "package_type": "mas", "mas_id": "553760117", "state" : "present" },
    {"full_name": "Gemini 2", "name": "gemini", "package_type": "brewcask", "state" : "present" }    
]
""".strip()

if __name__ == "__main__":
  package_data = json.loads(PACKAGES_DATA)
  print(package_data)

