#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Script calls API URL with the Specified Arguments and returns output
in JSON format. 

Requires Python 3.6 

call_api.py -u http://url [OPTIONS]
        
        OPTIONS
        
        --prid = PRID
        --sn = stack_name
        --ae = app_env
        --ac = aws_account
        --auth = Base 64 encoded UserName and Password String
        

"""
import sys
import getopt
import requests

def get_params(argv):
    usage = """call_api.py -u http://url [OPTIONS]
        
        OPTIONS
        
        --prid = PRID
        --sn = stack_name
        --ae = app_env
        --ac = aws_account
        --auth = Base 64 encoded UserName and Password String
        """

    auth=""
    host_url = ""
    prid = None
    stack_name = None
    app_env = None
    aws_account = None
    
    if ( len(argv) < 1 ):
        print(usage)
        sys.exit(2)
    

    try:
        opts, args = getopt.getopt(argv,"hu:", [ "prid=", "sn=", 
                                               "ae=", "ac=", 
                                               "auth" ])
        
        for opt, arg in opts:
            if opt == "-h":
                print (usage)
                sys.exit(0)
            if opt == "-u":
                host_url = arg 
            elif opt == "--prid":
                prid = prid
            elif opt == "--sn":
                stack_name = arg
            elif opt == "--ae":
                app_env = arg
            elif opt == "--ac":
                aws_account = arg
            elif opt == "--auth":
                auth = arg
            else:
                pass
                
  
        return ( host_url, prid, stack_name, app_env, aws_account, auth )
            
            
    except getopt.GetoptError:
        sys.exit(2)
    

def call_aws_api(host_url, prid, stack_name, 
                 app_env, aws_account, auth):
    
    api_url = f'{host_url}/v1/{prid}/application/{stack_name}/details'
    api_params = {'exact' : 'false' , 'awsAccount' : aws_account }
    api_headers = {'Accept' : 'accept:application/json', 'authorization': f'Basic: {auth}'}

    try:

        response = requests.get(api_url, params = api_params, 
                                headers = api_headers, timeout=(2,1))
        response.raise_for_status()
        json_output = response.json()
        
    except requests.exceptions.MissingSchema:
        print("Invalid URL")
        sys.exit(3)
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        sys.exit(4)
    except requests.exceptions.HTTPError: 
        print("HTTP Error")
        sys.exit(5)
    except requests.exceptions.ReadTimeout:
        print("Server failed to respond.. Reply timeout")
        sys.exit(4)
    except requests.exceptions.ConnectTimeout:
        print("Connection request to server failed.. Request timeout")
        sys.exit(4)
    except ValueError:
        print("Received Invalid JSON output")
        sys.exit(6)
        
    return json_output


if __name__ == "__main__":
    host_url, prid, stack_name, app_env, aws_account, auth = get_params(sys.argv[1:])
    json_out = call_aws_api(host_url, prid, stack_name, app_env, aws_account, auth)
    print(json_out)
