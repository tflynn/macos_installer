#!/usr/bin/env python3

import json

PACKAGES_DATA="""
[
    {"full_name": "Atom Editor 1.31.1", "name": "atom", "package_type": "brewcask", "state" : "present" },
    {"full_name": "lzip 1.2.0", "name": "lzip", "package_type": "brew", "state" : "absent" },
    {"full_name": "Keep It (1.5.2)", "name": "Keep It", "package_type": "mas", "mas_id": "1272768911" , "state" : "absent" }     
]
""".strip()

if __name__ == "__main__":
  package_data = json.loads(PACKAGES_DATA)
  print(package_data)

