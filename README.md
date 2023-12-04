# `is_hostname()` for python

Much to my surprise, or perhaps simply failure to search properly,
there is no RFC compliant python tool for that syntactically validates hostnames.
Note that not all valid domain names are valid hostnames.

To validated domain names, I recommend dnspython, and to validate Urls, I recommend pydantic. But neither offers direct validation of hostnames.

## "Host" v "hostname"

A host for many internet protocols can be given in the form of a domain name, an IPv4 address, or an IPv6 address. I will use the term "hostname" to require to the domain name form.
A hostname must be a valid domain name, but not all valid domain names are hostnames.
