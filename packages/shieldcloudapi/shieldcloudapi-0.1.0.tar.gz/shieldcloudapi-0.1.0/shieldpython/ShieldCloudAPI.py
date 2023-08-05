# Python Module for accessing Shield Cloud API
import json

# special import so that we can hack the connection method to bootstrap it
from urllib3.util import connection

_orig_create_connection = connection.create_connection

# main requests library that will call urllib3
import requests

# dns libraries could be imported conditionally during init
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query

import os
import copy

# the following commented out code belongs in the shieldmethod class

# methods that are called before DNS resolution (effectively replacing it) are in this list:
# PRE_RESOLVE_METHODS = [SHIELD_CLOUD_API_V1, SHIELD_DNS_API_JSON, GOOGLE_DOH]

# methods that are called after DNS resolution are in this list:
# POST_RESOLVE_METHODS = [
#    SHIELD_RECURSOR_DNS,
#    GOOGLE_DNS,
# ]

# methods that are not in either list will fail
# methods that are in both lists will probably only work at the PRE_RESOLVE stage

# bootstrap hostnames to allow query of HTTPS endpoints to provide DNS information (when DNS is obviously not available)
# please use the add_bootstrap_host funcion to add new entries during initialisation of your script
bootstrap_fqdn = {
    "developer.intrusion.com": "34.98.66.35",  # Shield Cloud API endpoint
    "dns.google": "8.8.8.8",  # Google DNS
    "zegicnvgd2.execute-api.us-west-2.amazonaws.com": "52.32.153.91",  # Shield DNS API endpoint (alpha)
}


# Shield methods to be implemented as an enum here:
from enum import Enum


class shieldmethod(Enum):
    SHIELD_CLOUD_API_V1 = 1  # Apigee Interface with V1 URLs
    SHIELD_DNS_API = 20  # DOH with dns-message method, via AWS API with an API key
    SHIELD_DNS_API_JSON = (
        21  # DOH using dns-query method, use this to get extended information easily
    )
    SHIELD_RECURSOR_DNS = 53  # query with UDP, fallback to UDP
    CLOUDFLARE_DNS = 1111  # testing
    GOOGLE_DNS = 8888  # testing mode using 8.8.8.8 DNS
    GOOGLE_DOH = 8889  # testing mode using JSON GET to 8.8.8.8

    # default function
    @classmethod
    def default(cls):
        return cls.SHIELD_CLOUD_API_V1


def bootstrap_create_connection(address, *args, **kwargs):
    # this function provides a connection to developer.intrusion.com, the IP address cannot be resolved at boot time because we are the DNS
    # ideally, we might give a global variable here that is bootstrap resolved during init
    # but for now just use a hard coded IP

    # if you try to use the "connection" function elsewhere in your own program, it may instead use this one which will create problems

    # one day this will be replaced by a DNS Adapter function so that

    # print("DEBUG: using bootstrap_create_connection")

    host, port = address
    hostip = "34.98.66.35"
    return _orig_create_connection((hostip, port), *args, **kwargs)


# global function to replace connection routine used by "requests" with our bootstrapped routine
connection.create_connection = bootstrap_create_connection


# helper function to load an API key from a local file if it is not available as part of init
# helpful because the developer (me) can re-use their key instead of accidently importing it to github
def apikeyfile(hintname="", hintpath=""):

    filenames = ["shield_apikey","apikey", "apikey.txt"]
    if hintname:
        filenames.insert(0, hintname)

    paths = [os.getcwd(), os.path.expanduser("~")]
    if hintpath:
        paths.insert(0, hintpath)

    # nested loops to look for candidates
    for f in filenames:
        for p in paths:
            file = "{}/{}".format(p, f)

            # debug info
            #print("Looking for apikey in: {}".format(file))

            if os.path.exists(file):
                # read until we get a line that is not:
                #   whitespace
                #   beginning with #
                #   shorter than 32 characters (the API key length is 49)

                h = open(file, "r")
                lines = h.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#") and len(line) > 31:
                        return line

    # if we get to here then there is no apikey
    return False


# init function to load authentication credentials
# also determines the method used to retreive information (Shield Cloud API, Shield DNS API, Shield Recursor DNS)
# returns some kind of session, allowing multiple API hosts (ie: prod, stage) to be used simultaneously
#
# NOTE TO DEVELOPERS - documentation is at developers.intrusion.com, API calls go to developer.intrusion.com. subtle.


def init(
    apikey,
    method=shieldmethod.SHIELD_CLOUD_API_V1,
    apihost="developer.intrusion.com",
    timeout=5,
    loadbalance="none",
    debug=0,
):

    # api key
    # method
    # apihost
    # timeout - seconds, under normal conditions we might set this to 30, but in a firewall application we need a quick response!
    # loadbalance - placeholder to decide how we multiple api hosts are handled
    # debug - return a debugging response that includes full HTTP headers of request/response

    session = {}

    # print("SC Variable type")
    # print(type(method))

    # allow the session to be setup using different variables for "method"
    # if type(method) is enum:
    #   session["method"] = method
    #
    if type(method) is str:
        # test to see if str is actually an integer

        session["method"] = shieldmethod[method]
        # test for valid method, otherwise warn

    elif type(method) is int:
        session["method"] = shieldmethod(method)

    else:
        session["method"] = shieldmethod.default()

    #print("SC method configured: {}".format(shieldmethod(session["method"])))

    # this is a catch all, if a valid method is not set, set it to default
    if type(session["method"]) == "NoneType" or not isinstance(
        session["method"], shieldmethod
    ):
        # print("DEFAULT method")
        session["method"] = shieldmethod.default()

    # replace the incoming "method" with whatever got configured
    method = session["method"]

    # debug throwaway
    # print(type(session["method"]))
    # print("session method:")
    # print(session["method"])
    # print("requested method:")
    # print(method)
    # print("apikey:")
    # print(apikey)
    # print()

    session[
        "loadbalance"
    ] = loadbalance  # validation of this parameter can be done below

    if method == shieldmethod.SHIELD_CLOUD_API_V1:
        # validate api key, maybe some kind of regex is appropriate

        # try and find it in a local file
        if not apikey:
            apikey = apikeyfile()

        if not apikey:
            raise ValueError("init: invalid apikey")

        # validate apihost - in a future version intrusion might introduce load balancing functionality here
        if not apihost:
            raise ValueError("init: empty api host, cannot proceed")

        session["apihost"] = apihost
        session["apikey"] = apikey
        session["urlprefix"] = "https://" + apihost
        session["headers"] = {"Content-type": "application/json", "x-apikey": apikey}

        # might need to bump up the default timeout for APIGEE

        return session

    elif method == shieldmethod.SHIELD_RECURSOR_DNS:

        dns_hosts = []  # list of IPv4 and IPv6 addresses
        dns_default = ["198.58.73.13"]

        # add default IP if blank
        if 1:
            dns_hosts = dns_default
        # change default "developer.intrusion.com" to default IP

        # bootstrap resolve hostname, ie: bind-dev.rr.shield-cloud.com

        # setup a scoreboard to test that DNS is working before we try and use it

        session["dnshosts"] = dns_hosts
        return session

    elif (
        method == shieldmethod.SHIELD_DNS_API_JSON or method == shieldmethod.GOOGLE_DOH
    ):
        # only validate API key for SHIELD_DNS_API_JSON
        if method == shieldmethod.SHIELD_DNS_API_JSON:
            # IP address is ok
            if not apihost:
                raise ValueError("DNS JSON - apihost not configured")

            # https://zegicnvgd2.execute-api.us-west-2.amazonaws.com/dns-query

            session["apihost"] = apihost
            session["apikey"] = apikey
            session["urlprefix"] = "https://" + apihost
            session["headers"] = {
                "Content-type": "application/json",
                "x-apikey": apikey,
            }

            # no-op for formatting
            pass
            # expand hostname to IP addresses
            session["url"] = "https://"
            # ipv6 address we should check

        elif method == shieldmethod.GOOGLE_DOH:
            dns_hosts = ["8.8.8.8"]

        else:
            raise ValueError("Unsupported Method for DoH query:", method)

        session["dnshosts"] = dns_hosts
        return session


# doh_simple functions from https://github.com/rthalley/dnspython/blob/master/examples/doh-json.py
def make_rr(simple, rdata):
    csimple = copy.copy(simple)
    csimple["data"] = rdata.to_text()
    return csimple


def flatten_rrset(rrs):
    simple = {
        "name": str(rrs.name),
        "type": rrs.rdtype,
    }
    if len(rrs) > 0:
        simple["TTL"] = rrs.ttl
        return [make_rr(simple, rdata) for rdata in rrs]
    else:
        return [simple]


def to_doh_simple(message):
    simple = {"Status": message.rcode()}
    for f in dns.flags.Flag:
        if f != dns.flags.Flag.AA and f != dns.flags.Flag.QR:
            # DoH JSON doesn't need AA and omits it.  DoH JSON is only
            # used in replies so the QR flag is implied.
            simple[f.name] = (message.flags & f) != 0
    for i, s in enumerate(message.sections):
        k = dns.message.MessageSection.to_text(i).title()
        simple[k] = []
        for rrs in s:
            simple[k].extend(flatten_rrset(rrs))
    # we don't encode the ecs_client_subnet field

    # johns EDNS options code - non standard
    # Google says EDNS is not supported
    # https://developers.google.com/speed/public-dns/docs/doh/json
    # IETF document does not mention it
    # https://datatracker.ietf.org/doc/html/draft-bortzmeyer-dns-json

    modifiedresponse = False
    if message.options:
        edns = []

        for o in message.options:
            infocode = int(o.otype)
            edecode = edecodes[infocode] if edecodes[infocode] else "unknown"
            edns.append(
                {
                    # INFO-CODE and EXTRA-TEXT are defined in RFC 8914
                    "infocode": infocode,
                    "edecode:": edecodes[infocode],
                    "extratext": o.text,
                }
            )
            if infocode > 0:
                modifiedresponse = True

        simple["EDNS"] = edns
        if modifiedresponse:
            simple["ModifiedDNSResponse"] = True

    return simple


# apigee raw API call to resolve domain
def domainresolution_v1(session, domain, querytype):
    # validate session or fail

    # this function will only work for method SHIELD_API_V1

    jdict = {"domain": domain, "querytype": querytype}
    url = session["urlprefix"] + "/domainresolution/v1/"
    #print("URL: " + url)
    #print(session["headers"])
    # response = requests.post(url, json=jdict, headers=session["headers"])
    response = requests.get(url, params=jdict, headers=session["headers"])

    # if debug, grab the headers and request/response here
    # print(response)

    # assume response is json, should probably test for that first
    data = json.loads(response.text)

    # collect some infomation from the requests object and return it as data for better error handling
    data["api"] = {
        "status_code": response.status_code,
        "elapsed": response.elapsed.total_seconds(),
    }

    return data


# call domainresolution_v1 above, and mediate the result into a "standard" JSON DNS response
def domainresolution_v1_mediated(session, domain, querytype):
    result = domainresolution_v1(session, domain, querytype)
    r = {}
    # 0 is an affirmative response, there are other codees for errors
    r["Status"] = 0

    # type should be the numeric code
    r["Question"] = {"name": domain, "type": dns.rdatatype.from_text(querytype)}
    r["Answer"] = result["response"]["answer"]
    r["Authority"] = []
    r["Additional"] = {}

    return r


def domainenrich_v1(session, domain, querytype):
    # validate session or fail

    jdict = {"domain": domain, "querytype": querytype}
    url = session["urlprefix"] + "/domainenrich/v1/"
    #print("URL: " + url)
    #print(session["headers"])
    response = requests.post(url, json=jdict, headers=session["headers"])
    # if debug, grab the headers and request/response here
    # print(response)

    # assume response is json, should probably test for that first
    data = response.text

    return data


def doh_json(session, domain, querytype):
    # validate session of fail

    # session method should be SHIELD_DNS_API_JSON or GOOGLE_DOH
    url = session["url"]

    return false


def query_recursor(session, domain, querytype="ANY"):
    # this is the standard DNS query

    # validate session

    # just take the first DNS host, add in load balancing code later
    dns_server = session["dnshosts"][0]

    # add the edns tag here, so that Shield Recursor DNS gives an extended response
    q = dns.message.make_query(domain, querytype, use_edns=0)

    # validate that it made a query?
    # print("DEBUG 1")
    # print(q.to_text())

    # print("DNS: " + dns_server)

    # run the query
    # implement timeout here later
    (r, tcp) = dns.query.udp_with_fallback(q, dns_server)

    # use doh_simple code from lambda to turn the wirecode response into a python object
    # print("DEBUG 2")
    # print(r.to_text())

    p = to_doh_simple(r)

    if session["method"] == shieldmethod.SHIELD_RECURSOR_DNS:
        # check for extra guff here to add into the response
        pass
    else:
        # its vanilla DNS
        pass

    # ultimately, lambda_handler.py will probably load this module, wouldn't that be cool
    # that way, customers can run their own lambda handler that points at our infrasructure recursively

    return p


# top function for querying of all methods with a mediated result
def query_dns(session, domain, querytype="A"):

    # shield API does not handle types other than A or AAAA, so we probably need to handle that

    # debug line
    #print(session)

    if session["method"] == shieldmethod.SHIELD_CLOUD_API_V1:
        # result = domainresolution_v1(session, domain, querytype)
        result = domainresolution_v1_mediated(session, domain, querytype)

    elif session["method"] == shieldmethod.SHIELD_RECURSOR_DNS:
        result = query_recursor(session, domain, querytype)

    # need to test for failure here in case session["method"] is not valid

    return result


def query(session, domain, querytype="ANY"):
    # basic host request
    # return block or allow
    # return list of blocked IP addresses
    # return list of allowed IP addresses

    return false
