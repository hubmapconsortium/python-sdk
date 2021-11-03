<!--
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
layout: home
-->
![hubmap logo](hubmap-type-white250.png)
#HuBMAP SDK

---

###Table of contents
1. [SDK Overview](#1-sdk-overview)
   1. Getting Started
   2. Requirements 
2. [Entity SDK](#2-entity-sdk)
3. Search SDK

---
###1. SDK Overview
This document covers the HuBMAP SDK that provides an interface to the functions that can be accessed through the HuBMAP API's. These API's include Entity-Api, Search-Api, UUID-Api, and Ingest-API. Each API has its own client library contained within the hubmap_sdk package. Details for using the individual sdk's are provided in their respective section below.  

####1.1 Getting Started
The HuBMAP SDK takes the form of a python client library. This library (hubmap_sdk) can be installed via pip with the command
```bash
pip install hubmap-sdk 
```

####1.2 Requirements
hubmap_sdk has the following requirements:
```bash
certifi==2021.10.8
chardet==4.0.0
idna==2.10
requests==2.25.1
urllib3==1.26.7
```



---
###2. Entity SDK
####2.1 Entity SDK Overview
The entity sdk may be used to access any functionality from the Entity API. In order to use the entity sdk, you will 
need to either import the hubmap_sdk package with 

```python
import hubmap_sdk
```

or you may directly import the entity sdk class with 

```python
from hubmap_sdk.entitysdk import EntitySdk
```

In order to use any of the entity sdk methods, create an instance of the entity sdk class. This class accepts 2 
arguments, both of which are optional. The first is "token". Token is a Globus Nexus token. If there is no such token, 
only public accessible methods will be reachable. Which methods require special access will be indicated below. 

Depending on which user groups the provided nexus token belongs in, some or all functionality in certain methods will 
remain inaccessible. These too will be detailed in each method's outline below. Validation of nexus tokens is performed 
when the entity api is called. If, for example, a method that requires a nexus token is used but there is no token
given, the entity api will return an error detailing the problem. This will also happen if a token is provided that is 
invalid, or if the token given is valid but is not part of the necessary user group to access part or all of a method.

If no token is given, it is assumed that there is no token. 

The next argument is service_url. The Entity Api has several servers: Dev, Test, Stage, and Production. It is also 
possible to run the entity api locally. service_url is where the chosen instance of Entity Api is selected. If none is
provided, the production server will be used automatically. Be certain there are no typos in the service url. The urls 
for the different servers are as follows: 

* Dev: https://entity-api.hubmapconsortium.org/
* Test: https://entity-api.test.hubmapconsortium.org/
* Stage: https://entity-api.stage.hubmapconsortium.org/
* Production: https://entity-api.hubmapconsortium.org/

If using a local instance of Entity Api, by default the port used is 5002. Therefore "localhost:5002" would be used for
service_url. 

Once this entity sdk instance is created, it will be used for each method. Creating an entity sdk instance will look 
like the following:

```python
from hubmap_sdk import EntitySdk

#In this example, the token and service url are being retrieved from a configuration file.
url = app.config['DEV_URL']
nexus_token = app.config['GLOBUS_TOKEN'] 


entity_instance = EntitySdk(nexus_token, url)
```

Each of the major entity types recognized by the Entity Api is modeled with its own class in the hubmap sdk.
These include:
* Donor
* Dataset
* Sample
* Collection
* Upload

Several methods in the entity api will return an instance of these classes; particularly methods that retrieve entities 
or create entities. The Entity Api itself simply returns dictionaries with the properties of these entities, and the 
hubmap_sdk creates these class instances to allow developers to have a workable object to use. For example, if the 
method "get_endpoint_by_id" is used (this endpoint is detailed below) and the id supplied is for a donor entity, rather
than return a dictionary with the properties of that donor, an object of the class donor is returned.

####2.2 Entity Sdk Methods 

The following entity sdk methods each correspond with an endpoint inside the entity api. 

#####Get Status
<table>
<tr><td>Description</td><td>Get status will print the current build, version, and neo4j connection status of the Entity Api.</td></tr>
<tr><td>Arguments</td><td>None</td></tr>
<tr><td>Outputs</td><td>This method will print the version, build, and neo4j connection status to the terminal. It will be formatted as "version: '{version}', build: '{build}', neo4j_connection: '{neo4j_connection}'". Additionally, the complete response from entity api will be returned as a dictionary.</td></tr>
<tr><td>Example</td><td>
input:

```python
status_object = entitysdk_instance.get_status()
```
output:

status_object

terminal output:
```
'version: '{version}' , build: '{build}', neo4j_connecton: '{neo4j_connection}'
```
</td></tr>

<tr><td>Error Handling</td><td>Most methods will raise an exception if either Entity Api returns an error code (http status code 300 or greater) or if the connection fails altogether. Because of the nature of the get status method, if either of these occur, an exception will not be raised, rather the exception or error message from Entity Api will be printed to the terminal and returned rather than the status message</td></tr>
<tr><td>Authorizations</td><td>This method requires no token</td></tr>
</table>


#####Get Ancestor Organs 
<table>
<tr><td>Description</td><td>Takes an id (HuBMAP id or UUID) for a sample or dataset and will return a list of organs that are ancestors to the given sample or Dataset.</td></tr>

<tr><td>Arguments</td><td><table><tr><td>identification</td><td><table><tr><td>Optional: No</td></tr><tr><td>Type: String</td></tr></table></td></table></tr>

<tr><td>Output</td><td>The output of this method is a list containing objects of the class Sample. These sample objects are the organs that are ancestors to the given sample or dataset</td></tr>
<tr><td>Example</td><td>input:

```python
organs_list = entitysdk_instance.get_ancestor_organs(hubmap_id)
```
output:

a list with objects of the type "Sample"

</td></tr>

<tr><td>Error Handling</td><td>If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get ancestor organs method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raised also.</td></tr>
<tr><td>Authorization</td><td>No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of the HuBMAP-Read group, only organs that are public will be returned.</td></tr>
</table>

#####Get Entity by ID
<table>
<tr><td>Description</td><td>Takes an id (HuBMAP id or UUID) for an entity and returns an instance of the class corresponding to the given id.</td></tr>
<tr><td>Arguments</td><td><table><tr><td>identification</td><td><table><tr><td>Optional: No</td></tr><tr><td>Type: String</td></tr></table></td></table></tr>
<tr><td>Outputs</td><td>This method outputs an instance of one of the entity classes. This class will correspond with the class of the entity given by the identification</td></tr>
<tr><td>Example</td><td>
input:

```python
sample1 = entitysdk_instance.get_entity_by_id() 
```
output:


</td></tr>
</table>

