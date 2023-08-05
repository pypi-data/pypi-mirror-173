# this script queries the Shield Cloud API for a hostname that is known to be blocked
import sys

print(sys.path)
# this is a hack to allow this script to run even when shieldpython is not installed
sys.path.append("../shieldpython")
print(sys.path)
import ShieldCloudAPI as shield
import json


apikey = ""  # please enter your Shield API key here
fqdn = "intrusion.com"


session = shield.init(apikey, "SHIELD_CLOUD_API_V1")
result = shield.domainresolution_v1(session, "playboy.com", "A")

print(json.dumps(result, indent=2))
