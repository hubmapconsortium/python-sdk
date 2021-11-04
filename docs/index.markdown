<!--
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
layout: home
-->
![hubmap logo](hubmap-type-white250.png)
# HuBMAP SDK

---

### Table of contents
1. [SDK Overview](#1-sdk-overview)
   1. [Getting Started](#11-getting-started)
   2. [Requirements](#12-requirements)
2. [Entity SDK](#2-entity-sdk)
3. Search SDK

---
### 1. SDK Overview


This document covers the HuBMAP SDK that provides an interface to the functions that can be accessed through the HuBMAP API's. These API's include Entity-Api, Search-Api, UUID-Api, and Ingest-API. Each API has its own client library contained within the hubmap_sdk package. Details for using the individual sdk's are provided in their respective section below.  

#### 1.1 Getting Started
The HuBMAP SDK takes the form of a python client library. This library (hubmap_sdk) can be installed via pip with the command
```bash
pip install hubmap-sdk 
```

#### 1.2 Requirements
hubmap_sdk has the following requirements:
```bash
certifi==2021.10.8
chardet==4.0.0
idna==2.10
requests==2.25.1
urllib3==1.26.7
```



---
### 2. Entity SDK
#### 2.1 Entity SDK Overview
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

#### 2.2 Entity Sdk Methods 

The following entity sdk methods each correspond with an endpoint inside the entity api. 

##### Get Status
<table>
<tr><td>Description</td><td>Get status will print the current build, version, and neo4j connection status of the Entity Api.</td></tr>
<tr><td>Arguments</td><td>None</td></tr>
<tr><td>Outputs</td><td>This method will print the version, build, and neo4j connection status to the terminal. It will be formatted as "version: '{version}', build: '{build}', neo4j_connection: '{neo4j_connection}'". Additionally, the complete response from entity api will be returned as a dictionary.</td></tr>
<tr><td>Example</td><td>
Input:

```python
status_object = entitysdk_instance.get_status()
```
Output:

```
'version: '{version}' , build: '{build}', neo4j_connecton: '{neo4j_connection}'
```
</td></tr>

<tr><td>Error Handling</td><td>Most methods will raise an exception if either Entity Api returns an error code (http status code 300 or greater) or if the connection fails altogether. Because of the nature of the get status method, if either of these occur, an exception will not be raised, rather the exception or error message from Entity Api will be printed to the terminal and returned rather than the status message</td></tr>
<tr><td>Authorizations</td><td>This method requires no token</td></tr>
</table>


##### Get Ancestor Organs 
<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for a sample or dataset and will return a list of organs that are ancestors to the given sample or Dataset.</td></tr>
<tr><td rowspan="2">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td> Type: String</td></tr>
<tr><td>Output</td><td colspan="2">The output of this method is a list containing objects of the class Sample. These sample objects are the organs that are ancestors to the given sample or dataset</td></tr>
<tr><td>Example</td><td colspan="2">Input:

```python
hubmap_id = "HBM123.ABCD.456"
organs_list = entitysdk_instance.get_ancestor_organs(hubmap_id)
print(f"The output is of type {type(organs_list)}")
print(f"The elements in the list are of the type {type(organs_list[0])}")
```
Output:

```
organs_list is of type <class 'list'>
The elements in the list are of the type <class 'hubmap_sdk.entitysdk.Sample'>
```


</td></tr>

<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get ancestor organs method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raised also.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of the HuBMAP-Read group, only organs that are public will be returned.</td></tr>
</table>

##### Get Entity by ID
<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for an entity and returns an instance of the class corresponding to the given id.</td></tr>
<tr><td rowspan="2">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr>
<tr><td>Output</td><td colspan="2">This method outputs an instance of one of the entity classes. This class will correspond with the class of the entity given by the identification</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
new_sample = entitysdk_instance.get_entity_by_id(hubmap_id)
print(f"new_sample is of the type {new_sample}")
```
Output:

```
new_sample is of the type <class 'hubmap_sdk.entitysdk.Sample'>
```

</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get entity by id method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>
</table>

##### Get Entity Provenance 

<table>
<tr><td>Description</td><td colspan="2">Takes in an id (HuBMAP ID or UUID) and returns a dictionary with the provenance tree above the given ID. Optionally accepts an integer "depth" which will limit the size of the returned tree.</td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">Depth</td><td>Optional: Yes</td></tr><tr><td>Type: Integer</td></tr>
<tr><td>Output</td><td colspan="2">This method outputs a dictionary containing the complete provenance tree above the given id. </td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
tree_depth = 4
hubmap_id = "HBM123.ABCD.456"
provenance = entitysdk_instance.get_entity_provenance(hubmap_id, tree_depth)
print(f"The type of the returned provenance is {type(provenance)}")
```

Output

```
The type of the returned provenance is <class 'dict'>
```

<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get entity provenance method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>
</table>

##### Get Entity Types

<table>
<tr><td>Description</td><td>This method returns a list of all available entity types as defined in the schema yaml https://raw.githubusercontent.com/hubmapconsortium/entity-api/test-release/entity-api-spec.yaml</td></tr>
<tr><td>Arguments</td><td>None</td></tr>
<tr><td>Outputs</td><td>This method outputs a list. The list contains each entity type defined in the schema. Each is represented as a string</td></tr>
<tr><td>Example</td><td>
Input:

```python
list_of_entity_types = entitysdk_instance.get_entity_types()
print(f"The type for list_of_entity_types is {type(list_of_entity_types)}")
print(f"The type for items in the list is {type(list_of_entity_types[0])}")
```

Output:

```
The type for list_of_entity_types is <class 'list'>
The type for items in the list is <class 'str'>
```


</td></tr>
<tr><td>Error Handling</td><td>If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get entity types method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td>No token is required for this method. If a token is provided and it is invalid, an exception will be raised.</td></tr>
</table>

##### Get Entities by Type

<table>
<tr><td>Description</td><td colspan="2">Takes as input an entity type and returns a list of all entities within that given type. Optionally, rather than Returning all of the information about the entities, it is possible to filter such that only a certain property is returned for each. This is given by the value "property_key". For example, when retrieving a list of all donors, if it is desired to only have the uuid of each donor included in the list, set property_key = "uuid". Acceptable values for entity type are the entities defined in the schema yaml https://raw.githubusercontent.com/hubmapconsortium/entity-api/test-release/entity-api-spec.yaml</td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">entity_type</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">property_key</td><td>Optional: Yes</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a list. This list contains objects of the class given by entity_type</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
entity_type = "uploads"
propertykey = "uuid"
list_of_uploads = entitysdk_instance.get_entities_by_type(entity_type, propertykey)
print(f"The type for list_of_entity_types is {type(list_of_uploads)}")
print(f"The type for items in the list is {type(list_of_uploads[0])}")
```

Output:

```
The type for list_of_entity_types is <class 'list'>
The type for items in the list is <class 'Upload'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get entities by type method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>


##### Get Collection

<table>
<tr><td>Description</td><td colspan="2">Takes as input identification (HuBMAP id or UUID) for a collection and returns an instance of the collection class corresponding to the identification given</td></tr>
<tr><td rowspan="2">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs an instance of the collection class.</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
new_collection = entitysdk_instance.get_collection(hubmap_id)
print(f"The type for new_collection is {type(new_collection)}")
```

Output:

```
The type for new_collection is <class 'Collection'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get collection method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>

##### Get Collections 
<table>
<tr><td>Description</td><td>Returns a list of all public collections. If a valid token is given that is part of the HuBMAP-Read group, both published and unpublished collections will be returned</td></tr>
<tr><td>Arguments</td><td>None</td></tr>
<tr><td>Outputs</td><td>This method outputs a list. The list contains objects of the class Collections.</td></tr>
<tr><td>Example</td><td>
Input:

```python
collections_list = entitysdk_instance.get_collections()
print(f"The type for collections_list is {type(collections_list)}")
print(f"The type for items in the list is {type(collections_list[0])}")
```

Output:

```
The type for collections_list is <class 'list'>
The type for items in the list is <class 'Collection'>
```


</td></tr>
<tr><td>Error Handling</td><td>If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get collections method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td>No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>

##### Create Multiple Samples
<table>
<tr><td>Description</td><td colspan="2">Creates multiple samples from the same source. Accepts a dictionary containing the information of the new entity and an integer designating how many samples to create. Returns a list of the newly created sample objects. 'direct_ancestor_uuid' is a required field in the dictionary. An example of a valid call would be: create_multiple_samples(5, data) where data is the dictionary containing the information about the new entities. A token is required.</td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">count</td><td>Optional: No</td></tr><tr><td>Type: Integer</td></tr><tr><td rowspan="2">data</td><td>Optional: No</td></tr><tr><td>Type: Dictionary</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a list. This list contains objects of the class Sample</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
count = 5
data = {"specimen_type": "blood", "protocol_url": "https://dx.doi.org/99.9999/protocols.io.abcdefg", "direct_ancestor_uuid": "99999999999999999999999999999999"}
list_of_samples = entitysdk_instance.create_multiple_samples(count, data)
print(f"The type for list_of_entity_types is {type(list_of_samples)}")
print(f"The type for items in the list is {type(list_of_samples[0])}")
```

Output:

```
The type for list_of_samples is <class 'list'>
The type for items in the list is <class 'Sample'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The create multiple samples method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">A token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or one is provided but is not in the HuBMAP-Read group, an exception will be raised.</td></tr>

</table>

##### Create Entity
<table>
<tr><td>Description</td><td colspan="2">Creates a new entity of a specified type. Takes as input a dictionary containing the details of the new entity and entity type.</td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">entity_type</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">data</td><td>Optional: No</td></tr><tr><td>Type: Dictionary</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs an instance of a class given by entity_type.</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
entity_type: "sample"
data = {"specimen_type": "blood", "protocol_url": "https://dx.doi.org/99.9999/protocols.io.abcdefg", "direct_ancestor_uuid": "99999999999999999999999999999999"}
new_sample = entitysdk_instance.create_entity(entity_type, data)
print(f"The type for new_sample is {type(new_sample)}")
```

Output:

```
The type for new_sample is <class 'Sample'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The create entity method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">A token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or one is provided but is not in the HuBMAP-Read group, an exception will be raised.</td></tr>

</table>


##### Update Entity 

<table>
<tr><td>Description</td><td colspan="2">Updates an existing entity. Takes as input an id (HuBMAP id or UUID) to an existing entity anda dictionary containing the properties either to add to or replace in the given entity. Returns an instance of the class corresponding with the given entity to reflect the new changes</td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">data</td><td>Optional: No</td></tr><tr><td>Type: Dictionary</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs an instance of a class corresponding to the class of the entity given by its id.</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
data = {"specimen_type": "blood", "protocol_url": "https://dx.doi.org/99.9999/protocols.io.abcdefg", "direct_ancestor_uuid": "99999999999999999999999999999999"}
updated_sample = entitysdk_instance.update_entity(hubmap_id, data)
print(f"The type for updated_sample is {type(updated_sample)}")
```

Output:

```
The type for updated_sample is <class 'Sample'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The update entity method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">A token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or one is provided but is not in the HuBMAP-Read group, an exception will be raised.</td></tr>

</table>

##### Get Ancestors

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for an entity and returns all of that entity's ancestors as a list. Allows filtering of specific properties by an optional argument "property_type". For example, for each entry in the returned list, rather than returning all of the properties, you could return only the UUID's by setting property_key='uuid' </td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">property_key</td><td>Optional: Yes</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a list of dictionaries. Each dictionary contains the information of an ancestor of the given id. If property key is set, the dictionaries will only have the property given by property_key</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
property_key = "uuid"
list_of_ancestors = entitysdk_instance.get_ancestors(hubmap_id, property_key)
print(f"The type for list_of_ancestors is {type(list_of_ancestors)}")
print(f"The type for each item in the list is {type(list_of_ancestors)}")
```

Output:

```
The type for list_of_ancestors is <class 'list'>
The type for each item in the list is <class 'dict'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get ancestors entity method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>

##### Get Descendants

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for an entity and returns all of that entity's descendants as a list. Allows filtering of specific properties by an optional argument "property_type". For example, for each entry in the returned list, rather than returning all of the properties, you could return only the UUID's by setting property_key='uuid' </td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">property_key</td><td>Optional: Yes</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a list of dictionaries. Each dictionary contains the information of a descendant of the given id. If property key is set, the dictionaries will only have the property given by property_key</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
property_key = "uuid"
list_of_descendants = entitysdk_instance.get_descendants(hubmap_id, property_key)
print(f"The type for list_of_descendants is {type(list_of_descendants)}")
print(f"The type for each item in the list is {type(list_of_descendants)}")
```

Output:

```
The type for list_of_descendants is <class 'list'>
The type for each item in the list is <class 'dict'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get descendants entity method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>

##### Get Parents

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for an entity and returns all of that entity's parents as a list. Allows filtering of specific properties by an optional argument "property_type". For example, for each entry in the returned list, rather than returning all of the properties, you could return only the UUID's by setting property_key='uuid' </td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">property_key</td><td>Optional: Yes</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a list of dictionaries. Each dictionary contains the information of a parent of the given id. If property key is set, the dictionaries will only have the property given by property_key</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
property_key = "uuid"
list_of_parents = entitysdk_instance.get_parents(hubmap_id, property_key)
print(f"The type for list_of_parents is {type(list_of_parents)}")
print(f"The type for each item in the list is {type(list_of_parents)}")
```

Output:

```
The type for list_of_parents is <class 'list'>
The type for each item in the list is <class 'dict'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get parents entity method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>

##### Get Children

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for an entity and returns all of that entity's children as a list. Allows filtering of specific properties by an optional argument "property_type". For example, for each entry in the returned list, rather than returning all of the properties, you could return only the UUID's by setting property_key='uuid' </td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">property_key</td><td>Optional: Yes</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a list of dictionaries. Each dictionary contains the information of a child of the given id. If property key is set, the dictionaries will only have the property given by property_key</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
property_key = "uuid"
list_of_children = entitysdk_instance.get_children(hubmap_id, property_key)
print(f"The type for list_of_children is {type(list_of_children)}")
print(f"The type for each item in the list is {type(list_of_children)}")
```

Output:

```
The type for list_of_children is <class 'list'>
The type for each item in the list is <class 'dict'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get children entity method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>

##### Get Previous Revisions

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for an entity and returns all of that entity's previous revisions as a list. Allows filtering of specific properties by an optional argument "property_type". For example, for each entry in the returned list, rather than returning all of the properties, you could return only the UUID's by setting property_key='uuid' </td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">property_key</td><td>Optional: Yes</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a list of dictionaries. Each dictionary contains the information of a previous revision of the given id. If property key is set, the dictionaries will only have the property given by property_key</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
property_key = "uuid"
list_of_previous_revisions = entitysdk_instance.get_previous_revisions(hubmap_id, property_key)
print(f"The type for list_of_previous_revisions is {type(list_of_previous_revisions)}")
print(f"The type for each item in the list is {type(list_of_previous_revisions)}")
```

Output:

```
The type for list_of_previous_revisions is <class 'list'>
The type for each item in the list is <class 'dict'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get previous revisions entity method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>

##### Get Next Revisions

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for an entity and returns all of that entity's next revisions as a list. Allows filtering of specific properties by an optional argument "property_type". For example, for each entry in the returned list, rather than returning all of the properties, you could return only the UUID's by setting property_key='uuid' </td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">property_key</td><td>Optional: Yes</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2" colspan="2">This method outputs a list of dictionaries. Each dictionary contains the information of a next revision of the given id. If property key is set, the dictionaries will only have the property given by property_key</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
property_key = "uuid"
list_of_next_revisions = entitysdk_instance.get_next_revisions(hubmap_id, property_key)
print(f"The type for list_of_next_revisions is {type(list_of_next_revisions)}")
print(f"The type for each item in the list is {type(list_of_next_revisions)}")
```

Output:

```
The type for list_of_next_revisions is <class 'list'>
The type for each item in the list is <class 'dict'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get next revisions entity method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned</td></tr>

</table>

##### Add Datasets To Collection

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for a collection and a list of dataset uuid's and connects each datset to the collection. The collection is then returned </td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">list_of_datasets</td><td>Optional: No</td></tr><tr><td>Type: List</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs an instance of the class Collection corresponding to the given id</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
list_of_datasets = ["11111111111111111111111111111111", "22222222222222222222222222222222", "33333333333333333333333333333333"]
new_collection = entitysdk_instance.add_datasets_to_collection(hubmap_id, list_of_datasets)
print(f"The type for new_collection is {type(new_collection)}")
```

Output:

```
The type for new_collection is <class 'Collection'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The add datasets to collection method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only entities that are public will be returned and both the collection and each of the datasets must be public, otherwise an exception will be raised </td></tr>

</table>

##### Get Globus Url

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for an entity and returns that entity's globus url </td></tr>
<tr><td rowspan="2">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td> Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a string containing the globus url</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
globus_url = entitysdk_instance.get_globus_url(hubmap_id)
print(f"The type for globus_url is {type(globus_url)}")
```

Output:

```
The type for globus_url is <class 'str'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get globus url method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only urls for entities that are public will be returned</td></tr>

</table>

##### Get Dataset Latest Revision

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for a dataset and returns an instance of the class dataset corresponding with the latest revision of the dataset given by the id </td></tr>
<tr><td rowspan="2">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td> Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs an instance of the class Dataset. This Dataset object corresponds with the latest revision of the dataset of the given id</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
latest_revision = entitysdk_instance.get_dataset_latest_revision(hubmap_id)
print(f"The type for latest_revision is {type(latest_revision)}")
```

Output:

```
The type for latest_revision is <class 'Dataset'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get dataset latest revision method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only urls for entities that are public will be returned</td></tr>

</table>

##### Get Dataset Revision Number

<table>
<tr><td>Description</td><td colspan="2">Takes an id (HuBMAP id or UUID) for a dataset and returns the revision number of that dataset as an integer</td></tr>
<tr><td rowspan="2">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td> Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs an integer for the revision number of a given dataset</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
revision_number = entitysdk_instance.get_dataset_revision_number(hubmap_id)
print(f"The type for revision_number is {type(revision_number)}")
```

Output:

```
The type for revision_number is <class 'int'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get dataset revision number method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only urls for entities that are public will be returned</td></tr>

</table>

##### Retract Dataset

<table>
<tr><td>Description</td><td colspan="2">Retracts a published dataset. Takes as input an id (HuBMAP id or UUID) for a dataset and a string retraction_reason Changes the field sub_status to "retracted" and sets "retraction_reason" to the string retraction_reason for the given dataset. The updated dataset is returned</td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">retraction_reason</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs an instance of the class Dataset corresponding to the retracted dataset</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
retraction_reason = "this dataset has been deprecated"
retracted_dataset = entitysdk_instance.retract_dataset(hubmap_id, retraction_reason)
print(f"The type for retracted_dataset is {type(retracted_dataset)}")
```

Output:

```
The type for retracted_dataset is <class 'Dataset'>
```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get globus url method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only urls for entities that are public will be returned</td></tr>

</table>

##### Get Revisions List

<table>
<tr><td>Description</td><td colspan="2">Takes as input an id (HuBMAP id or UUID) for a dataset and returns the list of all next or previous revisions of that dataset. It doesn't matter where in the list of revisions the given dataset is. For example, if the given dataset is the first revision of 5, or the 5th revision of 5, the output will be the same. Accepts an optional argument "include_dataset". By default this is false. If left unchanged, only the revision number and uuid will be included for each revision. If include_dataset is set to true, the full dataset will also be returned for each</td></tr>
<tr><td rowspan="4">Arguments</td><td rowspan="2">identification</td><td>Optional: No</td></tr><tr><td>Type: String</td></tr><tr><td rowspan="2">include_dataset</td><td>Optional: Yes</td></tr><tr><td>Type: Bool</td></tr>
<tr><td>Outputs</td><td colspan="2">This method outputs a list of dictionaries. Each dictionary contains the revision number integer, and the uuid of the dataset as a string. If include_dataset is set to true, then the complete dataset for each will be included as a dictionary as well</td></tr>
<tr><td>Example</td><td colspan="2">
Input:

```python
hubmap_id = "HBM123.ABCD.456"
include_dataset=True
list_of_revisions = entitysdk_instance.get_revisions_list(hubmap_id, include_dataset)
print(f"The type for list_of_revisions is {type(list_of_revisions)}")
print(f"The type for item in list_of_revisions is {type(list_of_revisions[0])}")
```

Output:

```
The type for list_of_revisions is <class 'Dataset'>
The type for item in list_of_revisions is <class 'dict'>

```


</td></tr>
<tr><td>Error Handling</td><td colspan="2">If the response code from Entity Api is greater than 300, an exception will be raised. The exception message will be the response from the Entity API. The get revisions list method will return this response from the API, so if this exception is handled individually, this information can be used. If the request to the Entity Api fails, an exception will be raise as well.</td></tr>
<tr><td>Authorization</td><td colspan="2">No token is required for this method. If a token is provided and it is invalid, an exception will be raised. If a token is not provided, or if a valid token is provided and the token is not part of HuBMAP-Read group, only information for entities that are public will be returned</td></tr>

</table>

