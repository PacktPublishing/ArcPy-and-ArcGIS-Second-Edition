import urllib
import urllib2
import httplib
import json
import contextlib


def submit_request(request):
    """ Returns the response from an HTTP request in json format."""
    with contextlib.closing(urllib2.urlopen(request)) as response:
        job_info = json.load(response)
        return job_info

def return_token(service_url, username, password):
    """ Returns an authentication token for use in ArcGIS Online."""

    # Set the username and password parameters before
    #  getting the token.
    #
    params = {"username": username,
              "password": password,
              "referer": "https://www.arcgis.com",
              "f": "json"}
    #build url for the generate token
    service_url = "{}/generateToken".format(service_url)
    #this is variable to be passed to the "submit_request" function
    request = urllib2.Request(service_url, urllib.urlencode(params))
    print "REQUEST IS ", request
    token_response = submit_request(request)
    print "TOKEN RESPONSE ", token_response
    #if condition to test if token is returned
    if "token" in token_response:
        print("Getting token...")
        token = token_response.get("token")
        return token
    else:
        # Test the request on HTTPS if error returned
        # Request for token must be made through HTTPS.
        if "error" in token_response:
            error_mess = token_response.get("error", {}).get("message")
            if "This request needs to be made over https." in error_mess:
                token_url = token_url.replace("http://", "https://")
                token = get_token(service_url, username, password)
                return token
            else:
                raise Exception("AGOL error: {} ".format(error_mess))
