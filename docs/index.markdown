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
