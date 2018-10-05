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
    {"full_name": "wget", "name": "wget", "package_type": "brew", "state" : "present" },
    {"full_name": "iTerm2 (3.2.1)", "name": "iterm2", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Google Chrome", "name": "google-chrome", "package_type": "brewcask", "state" : "present" },
    {"full_name": "1Password 7", "name": "1Password 7", "package_type": "mas", "mas_id": "1333542190", "state" : "present" },
    {"full_name": "Airmail 3 (3.6.41)", "name": "Airmail 3", "package_type": "mas", "mas_id": "918858936", "state" : "present" },
    {"full_name": "FullContact", "name": "FullContact", "package_type": "mas", "mas_id": "1094748271", "state" : "present" },
    {"full_name": "fantatical 2", "name": "fantastical", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Simplenote (1.3.7)", "name": "simplenote", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Sublime Text", "name": "sublime-text", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Vox", "name": "vox", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Backup and Sync from Google", "name": "google-backup-and-sync", "package_type": "brewcask", "state" : "present" },
    {"full_name": "DaisyDisk", "name": "daisydisk", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Notes for Google Keep", "name": "Notes for Google Keep", "package_type": "mas", "mas_id": "981433563", "state" : "present" },
    {"full_name": "MacDown", "name": "macdown", "package_type": "brewcask", "state" : "present" },
    {"full_name": "monosnap", "name": "monosnap", "package_type": "mas", "mas_id": "540348655", "state" : "present" },           
    {"full_name": "Photo Meta Edit", "name": "Photo Meta Edit", "package_type": "mas", "mas_id": "553760117", "state" : "present" },
    {"full_name": "Gemini 2", "name": "gemini", "package_type": "brewcask", "state" : "present" },
    {"full_name": "Sourcetree (2.7.6)", "name": "sourcetree", "package_type": "brewcask", "state" : "present"},
    {"full_name": "Intellij IDEA (2018.2.4)", "name": "intellij-idea", "package_type": "brewcask", "state" : "present"},
    {"full_name": "RubyMine (2018.2.3)", "name": "rubymine", "package_type": "brewcask", "state" : "present"},
    {"full_name": "PyCharm (2018.2.4)", "name": "pycharm", "package_type": "brewcask", "state" : "present"},
    {"full_name": "Vagrant (2.1.5)", "name": "vagrant", "package_type": "brewcask", "state" : "present"},
    {"full_name": "Virtualbox (5.2.18)", "name": "virtualbox", "package_type": "brewcask", "state" : "present"},
    {"full_name": "Airmail 3 (3.6.41)", "name": "airmail", "package_type": "brewcasklocal", "state" : "present" },
    {"full_name": "FullContact (18.07.3)", "name": "fullcontact", "package_type": "brewcasklocal", "state" : "present" },
    {"full_name": "Notes for Google Keep", "name": "notesforgooglekeep", "package_type": "brewcasklocal", "state" : "present" },
    {"full_name": "Monosnap (3.5.1)", "name": "monosnap", "package_type": "brewcasklocal", "state" : "present" },
    {"full_name": "dBPowerAmp (16.3.1)", "name": "dbpoweramp", "package_type": "brewcasklocal", "state" : "present" },
    {"full_name": "Photo Meta Edit", "name": "photometaedit", "package_type": "brewcasklocal" , "state" : "present" },
    {"full_name": "Picktorial (3.0.6)", "name": "picktorial", "package_type": "brewcasklocal" , "state" : "present" }
]
""".strip()

if __name__ == "__main__":
  package_data = json.loads(PACKAGES_DATA)
  print(package_data)

