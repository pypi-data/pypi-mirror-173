import sys

# this is a hack to allow this script to run even when shieldpython is not installed
sys.path.append("../shieldpython")
#print(sys.path)
import ShieldCloudAPI as shield
import json


apikey = ""  # please enter your Shield API key here
fqdn = "intrusion.com"

if len(sys.argv) > 1:
    fqdn = sys.argv[1]

print("Query for: {}".format(fqdn))
session = shield.init(
    apikey,  # a key for accessing the API that you can get from developers.intrusion.com
    shield.shieldmethod.SHIELD_CLOUD_API_V1,  # a method for accessing the information
)
result = shield.query_dns(
    session,  # the session initialised above
    fqdn,  # the domain name you wish to query
    # optional "querytype" value here, such as AAAA for an IPv6 hostname query
)

# print the resulting structure in a human readable format
print(json.dumps(result, indent=2))
