#!/usr/bin/python

import os, sys, requests, json, logging, uuid, time
import database.database as db

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("slicemngr:repo")
LOG.setLevel(logging.INFO)


#################################### Sonata SP information #####################################
def get_base_url():
    #ip_address=db.settings.get('SLICE_MGR','SONATA_SP_IP')
    #base_url = 'http://'+ip_address+':32001/api/v2'
    
    ip_address=db.settings.get('SLICE_MGR','SONATA_GTK')
    base_url = 'http://'+ip_address+':5300'
    
    return base_url

def use_sonata():    
    return db.settings.get('SLICE_MGR','USE_SONATA')

########################################## /requests ##########################################
#POST /requests to INSTANTIATE Network Service instance
def net_serv_instantiate(service_uuid):
    LOG.info("MAPPER: Preparing the request to instantiate NetServices")
    # prepares the parameters for the POST request
    url = get_base_url() + '/requests'
    headers = '{"Content-Type":"application/json"}'
    data = '{"service_uuid":"' + service_uuid + '", "ingresses":[], "egresses":[]}'

    #SONATA SP or EMULATED Connection 
    if use_sonata() == "True":
      #sends the request to the Sonata Gatekeeper API
      response = requests.post(url, headers=headers, data=data)
      jsonresponse = json.loads(response.text)
      
      return jsonresponse
    else:
      print ("SONATA EMULATED INSTANTIATION NSI --> URL: " +url+ ",HEADERS: " +str(headers)+ ",DATA: " +str(data))
      #Generates a RANDOM (uuid4) UUID for this emulated NSI
      uuident = uuid.uuid4()
      jsonresponse = json.loads('{"id":"'+str(uuident)+'"}')
      return jsonresponse

#POST /requests to TERMINATE Network Service instance
def net_serv_terminate(servInstance_uuid):
    LOG.info("MAPPER: Preparing the request to terminate NetServices")
    # prepares the parameters for the POST request
    url = get_base_url() + "/requests"
    headers = '{"Content-Type":"application/json"}'
    data = '{"service_instance_uuid":'+ servInstance_uuid + ', "request_type":"TERMINATE"}'

    #SONATA SP or EMULATED Connection 
    if use_sonata() == "True":
      # sends the request to the Sonata Gatekeeper API
      response = requests.post(url, headers=headers, data=data)
      jsonresponse = json.loads(response.text)

      return jsonresponse
    
    else:
      jsonresponse = "SONATA EMULATED TERMINATE NSI --> URL: " +url+ ",HEADERS: " +str(headers)+ ",DATA: " +str(data)
      print (jsonresponse)
      return jsonresponse

#GET /requests to pull the information of all Network Services INSTANCES
def getAllNetServInstances():
    LOG.info("MAPPER: Preparing the request to get all the NetServicesInstances")
    # prepares the parameters for the POST request
    url = get_base_url() + "/requests"
    headers = '{"Content-Type":"application/json"}'

    #SONATA SP or EMULATED Connection 
    if use_sonata() == "True":
      #sends the request to the Sonata Gatekeeper API
      response = requests.get(url, headers=headers)
      jsonresponse = json.loads(response.text)

      return jsonresponse
    
    else:
      jsonresponse = "SONATA EMULATED GET ALL NSI --> URL: " +url+ ",HEADERS: " +str(headers)
      LOG.info(jsonresponse)
      return jsonresponse

#GET /requests/<request_uuid> to pull the information of a single Network Service INSTANCE
def getRequestedNetServInstance(request_uuid):
    LOG.info("MAPPER: Preparing the request to get desired NetServicesInstance")
    # prepares the parameters for the POST request
    url = get_base_url() + "/requests/" + str(request_uuid)
    headers = '{"Content-Type":"application/json"}'

    #SONATA SP or EMULATED Connection 
    if use_sonata() == "True":
      # sends the request to the Sonata Gatekeeper API
      response = requests.get(url, headers=headers)
      jsonresponse = json.loads(response.text)

      return jsonresponse
    
    else:
      print ("SONATA EMULATED GET NSI --> URL: " +url+ ",HEADERS: " +str(headers))
      uuident = uuid.uuid4()
      jsonresponse = json.loads('{"began_at": "2017-09-15","callback": "http://localhost:5400/serv-instan-time","created_at": "2017-09-15","id": "de0d4c7e-9450-4c3f-8add-5f9531303c65","request_type": "CREATE","service_instance_uuid": "'+str(uuident)+'","service_uuid": "233cb9b2-5575-4ddd-8bd6-6c32396afe02","status": "READY","updated_at": "2017-09-15"}')
      return jsonresponse 
      
   
########################################## /services ##########################################
#GET /services to pull all Network Services information
def getListNetServices():
    LOG.info("MAPPER: Preparing the request to get the NetServices Information")
    #cleans the current nsInfo_list to have the information updated
    del db.nsInfo_list[:]
    
    # prepares the parameters for the POST request
    url = get_base_url() + "/services"
    headers = '{"Content-Type":"application/json"}'

    #SONATA SP or EMULATED Connection 
    if use_sonata() == "True":
      # sends the request to the Sonata Gatekeeper API
      response = requests.get(url, headers=headers)
      services_array = json.loads(response.text)
    
      for service_item in services_array:
        #Each element of the list is a dictionary   
        dict_ns = {}
        dict_ns["name"] = service_item['nsd']['name']
        dict_ns["uuid"] = service_item['uuid']
        dict_ns["decription"] = service_item['nsd']['description']
        dict_ns["version"] = service_item['nsd']['version']
        dict_ns["vendor"] = service_item['nsd']['vendor']
        dict_ns["md5"] = service_item['md5']
        dict_ns["author"] = service_item['nsd']['author']
        dict_ns["created"] = service_item['created_at']
        dict_ns["status"] = service_item['status']
        dict_ns["updated"] = service_item['updated_at']
  
        #adds the dictionary element into the list
        db.nsInfo_list.append(dict_ns)
              
      return db.nsInfo_list
      
    else:
      print ("SONATA EMULATED GET SERVICES --> URL: " +url+ ",HEADERS: " + str(headers))
