# this script will show the output of the domainresolution API

import sys

# this is a hack to allow this script to run even when shieldpython is not installed
sys.path.append("../shieldpython")
print(sys.path)
import ShieldCloudAPI as shield
import json


apikey = ""  # please enter your Shield API key here
fqdn = "intrusion.com"

if len(sys.argv) > 1:
    fqdn = sys.argv[1]


session = shield.init(apikey, shield.shieldmethod.SHIELD_CLOUD_API_V1)
result = shield.domainenrich_v1(session, "google.com", "A")

# print the resulting structure in a human readable format
print(json.dumps(result, indent=2))
