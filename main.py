#!/usr/bin/python

from flask import Flask, request
import os, sys, logging, json

import slice_lifecycle_mgr.nst_manager as nst_manager
import slice_lifecycle_mgr.nsi_manager as nsi_manager



app = Flask(__name__)

# ----- NETSLICE TEMPLATE Actions -----
@app.route('/api/nst/v1/descriptors', methods=['POST'])
def postNST():
    receivedNSTd = request.json
    new_NST = nst_manager.createNST(receivedNSTd)
    jsonNST = json.dumps(new_NST, indent=4, sort_keys=True)
    
    return (jsonNST),201

@app.route('/api/nst/v1/descriptors', methods=['GET'])
def getAllNST():
    allNST = nst_manager.getAllNst()
    jsonNSTList = json.dumps(allNST, indent=4, sort_keys=True)
    logging.info('Returning all NST')
    
    return (jsonNSTList),200

@app.route('/api/nst/v1/descriptors/<nstId>', methods=['GET'])
def getNST(nstId):
    returnedNST = nst_manager.getNST(nstId)
    jsonNST = json.dumps(returnedNST, indent=4, sort_keys=True)
    logging.info('Returning the desired NST')
    
    return jsonNST,200

@app.route('/api/nst/v1/descriptors/<nstId>', methods=['DELETE'])
def deleteNST(nstId):
    deleted_NSTid = nst_manager.deleteNST(nstId)
    
    return ('The NST was deleted successfully.'),204


## ----- NETSLICE INSTANCE Actions -----
#@app.route('/api/nsi', methods=['POST'])
#def createNSI():

#  return 'Creating a new NSI!'

@app.route('/api/nsilcm/v1/nsi', methods=['GET'])
def getALLNSI():
  allNSI = nsi_manager.getAllNsi()
  jsonNSIList = json.dumps(allNSI, indent=4, sort_keys=True)
  logging.info('Returning all existing NSIs (instantiated/terminated/etc.)')
  
  return (jsonNSIList),200

@app.route('/api/nsilcm/v1/nsi/<nsiId>', methods=['GET'])
def getNSI(nsiId):
  logging.info('Returning the desired NSI')
  returnedNSI = nsi_manager.getNSI(nsiId)
  jsonNSI = json.dumps(returnedNSI, indent=4, sort_keys=True)
    
  return (jsonNSI),200

#@app.route('/nsi/<int:nsiId>', methods=['DELETE'])
#def deleteNSI(nsiId):
#  #db.nsi_list.del[nsiId]

#  return 'Deletes the specific NSI'

#@app.route('/api/nsilcm/v1/nsi/<nsiId>/instantiate', methods=['POST']) #TODO: decide if we use two-steps creation or not
@app.route('/api/nsilcm/v1/nsi/instantiate', methods=['POST'])
def postNSIinstantiation():
  receivedNSI = request.json
  new_NSI = nsi_manager.createNSI(receivedNSI)
  instantiatedNSI = nsi_manager.instantiateNSI(new_NSI)
  jsonNSI = json.dumps(instantiatedNSI, indent=4, sort_keys=True)
  
  return (jsonNSI),201

@app.route('/api/nsilcm/v1/nsi/<nsiId>/terminate', methods=['POST'])
def postNSItermination(nsiId):
  terminationRx = request.json
  terminateNSI = nsi_manager.terminateNSI(nsiId, terminationRx)
  jsonNSI = json.dumps(terminateNSI, indent=4, sort_keys=True)
  
  return (jsonNSI),201



#MAIN FUNCTION OF THE SERVER
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5998)
