import requests
from phantasyRestClient.config import conf_dict
from phantasyRestClient.req.mp import MachinePortalResources
from phantasyRestClient.req.ca import CAResources

session = requests.Session()
session.verify = False
# mp resources
MachinePortalResources.SESSION = session
MachinePortalResources.URL = conf_dict['bind']
# ca resources
CAResources.SESSION = session
CAResources.URL = conf_dict['bind']
