import sys
import os
# this is a hack so the module can be imported even if it isn't installed yet
sys.path.append("../shieldpython")
import ShieldCloudAPI as shield
import json

# enter your API key in this line, or leave it blank for the software to look in ~/apikey for it
apikey = "" 

methods = [ 
    "SHIELD_CLOUD_API_V1",
    #"SHIELD_DNS_API",
    #"SHIELD_DNS_API_JSON",
    "SHIELD_RECURSOR_DNS",
    #"GOOGLE_DNS",
    #"CLOUDFLARE_DNS"
    ]

session = {}
session["SHIELD_CLOUD_API_V1"] = shield.init("","SHIELD_CLOUD_API_V1","developer.intrusion.com")
#print(session["SHIELD_CLOUD_API_V1"])

session["SHIELD_RECURSOR_DNS"] = shield.init("","SHIELD_RECURSOR_DNS")


qname = "google.com"
qtype = "A"

for method in methods:
    numeric_method = shield.shieldmethod[method]
    print(method + ":\t" + str(numeric_method))
    result = shield.query_dns(session[method],qname,qtype)
    print(json.dumps(result,indent=2))




