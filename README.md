# Various Scripts & Jupyter Notebooks

## Introduction

This repository presents:

* Python scripts using the ncclient library (0.5.2) to talk to NETCONF-enabled devices.
* Jupyter (IPython) Notebooks in the directory [```notebooks```](notebooks).


## Python Dependencies

The package dependencies for the scripts and the jupyter notebooks are listed in ```requirements.txt```, which may be used to install the dependencies thus (note the upgrade to pip; must be running **```pip >= 8.1.2```** to successfully install some dependencies):

```
EINARNN-M-80AT:ncc einarnn$ virtualenv v
New python executable in v/bin/python2.7
Also creating executable in v/bin/python
Installing setuptools, pip, wheel...done.
EINARNN-M-80AT:ncc einarnn$ . v/bin/activate
(v)EINARNN-M-80AT:ncc einarnn$ pip install --upgrade pip
Requirement already up-to-date: pip in ./v/lib/python2.7/site-packages
(v)EINARNN-M-80AT:ncc einarnn$ pip install -r requirements.txt
```

This example shows using the virtualenv tool to isolate packages from your global python install. This is recommended. Note that the versiojn of pip installed in the test environment was up to date, and so it did not need upgraded.


## Python Scripts

The Python scripts have been radically rationalized and there are now just a few key scripts, with the remainder moved to the [```archived```](archived) directory. The main scripts are:

* [```ncc.py```](ncc.py) -- A kind of Swiss Army Knife script with many options to get-config, get, edit-config, pass in parameters for substitution, etc. Can be easily extended by users to have more edit-config templates or more named filter templates. Available content can be seen using the ```--list-templates``` and ```--list-filters``` parameters.

* [```ncc-filtered-get.py```](ncc-filtered-get.py) -- Very simple script that takes a subtree filter and does a get.

* [```ncc-get-all-schema.py```](ncc-get-all-schema.py) -- Script that attempts to download all the supported schema that the box has and tries to compile them, determine missing includes or imports, etc.

* [```ncc-get-schema.py```](ncc-get-schema.py) -- Script to get a single names schema and dup it to ```STDOUT```.

* [```ncc-simple-poller.py```](ncc-simple-poller.py) -- Script that polls a device on a specified cadence for a specified subtree or XPath filter.

* [```rc-xr.py```](rc-xr.py) -- Embryonic RESTCONF sample script using the Python ```requests``` library.


A couple of the scripts used to have other names, so, for backwards compatibility, the following symlinks currently exist:


* ```ncc-oc-bgp.py``` --> ```ncc.py```

* ```ncc-get-all-schema-new.py``` --> ```ncc-get-all-schema.py```


### Running The Scripts

The scripts mostly have a fairly common set of options for help, hostname, port, username and password. For example, the [ncc.py](ncc.py) script can be invoked with ```--help```:

```
01:46 $ python ncc.py --help
usage: ncc.py [-h] [--host HOST] [-u USERNAME] [-p PASSWORD] [--port PORT]
              [--timeout TIMEOUT] [-v] [--default-op DEFAULT_OP]
              [--params PARAMS] [--params-file PARAMS_FILE]
              [-f FILTER | --named-filter NAMED_FILTER | -x XPATH]
              [--list-templates | --list-filters | -g | --get-oper | --do-edits DO_EDITS [DO_EDITS ...]]

Select your NETCONF operation and parameters:

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           The IP address for the device to connect to (default
                        localhost)
  -u USERNAME, --username USERNAME
                        Username to use for SSH authentication (default
                        'cisco')
  -p PASSWORD, --password PASSWORD
                        Password to use for SSH authentication (default
                        'cisco')
  --port PORT           Specify this if you want a non-default port (default
                        830)
  --timeout TIMEOUT     NETCONF operation timeout in seconds (default 60)
  -v, --verbose         Exceedingly verbose logging to the console
  --default-op DEFAULT_OP
                        The NETCONF default operation to use (default 'merge')
  --params PARAMS       JSON-encoded string of parameters dictionaryfor
                        templates
  --params-file PARAMS_FILE
                        JSON-encoded file of parameters dictionary for
                        templates
  -f FILTER, --filter FILTER
                        NETCONF subtree filter
  --named-filter NAMED_FILTER
                        Named NETCONF subtree filter
  -x XPATH, --xpath XPATH
                        NETCONF XPath filter
  --list-templates      List out named templates embedded in script
  --list-filters        List out named filters embedded in script
  -g, --get-running     Get the running config
  --get-oper            Get oper data
  --do-edits DO_EDITS [DO_EDITS ...]
                        Execute a sequence of named templates with an optional
                        default operation and a single commit
```

Named subtree filters are stored in [snippets/filters](snippets/filters) and named templates are stored in [snippets/editconfigs](snippets/editconfigs). The naming convention is fairly obvious; templates files end in ```.tmpl```, but when referred to via CLI arguments the extension is ommitted.

The snippets for both edit config messages and named filters now support a JSON format for specifying parameters either on the command line of in a provided file. For example, we may have the filter snippet in file ```intf-brief.tmpl```:

```
<interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
  <interface-briefs>
    <interface-brief>
      <interface-name>{{INTF_NAME}}</interface-name>
    </interface-brief>
</interfaces>
```

Then, run against IOS-XR:

```
$ python ncc.py --host=192.239.42.222 --get-oper --named-filter intf-brief --params '{"INTF_NAME":"GigabitEthernet0/0/0/0"}'
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
   <interface-briefs>
    <interface-brief>
     <interface-name>GigabitEthernet0/0/0/0</interface-name>
     <interface>GigabitEthernet0/0/0/0</interface>
     <type>IFT_GETHERNET</type>
     <state>im-state-admin-down</state>
     <actual-state>im-state-admin-down</actual-state>
     <line-state>im-state-admin-down</line-state>
     <actual-line-state>im-state-admin-down</actual-line-state>
     <encapsulation>ether</encapsulation>
     <encapsulation-type-string>ARPA</encapsulation-type-string>
     <mtu>1514</mtu>
     <sub-interface-mtu-overhead>0</sub-interface-mtu-overhead>
     <l2-transport>false</l2-transport>
     <bandwidth>1000000</bandwidth>
    </interface-brief>
   </interface-briefs>
  </interfaces>
 </data>
```

Or:

```
$ echo '{"INTF_NAME":"GigabitEthernet0/0/0/0"}' > test_params.json
$ python ncc.py --host=192.239.42.222 --get-oper --named-filter intf-brief --params-file test_params.json
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
   <interface-briefs>
    <interface-brief>
     <interface-name>GigabitEthernet0/0/0/0</interface-name>
     <interface>GigabitEthernet0/0/0/0</interface>
     <type>IFT_GETHERNET</type>
     <state>im-state-admin-down</state>
     <actual-state>im-state-admin-down</actual-state>
     <line-state>im-state-admin-down</line-state>
     <actual-line-state>im-state-admin-down</actual-line-state>
     <encapsulation>ether</encapsulation>
     <encapsulation-type-string>ARPA</encapsulation-type-string>
     <mtu>1514</mtu>
     <sub-interface-mtu-overhead>0</sub-interface-mtu-overhead>
     <l2-transport>false</l2-transport>
     <bandwidth>1000000</bandwidth>
    </interface-brief>
   </interface-briefs>
  </interfaces>
 </data>

```

## Running The Jupyter Notebooks

The jupyter notebook server should be run inside the same Python virtualenv as you created above for running the Python scripts. The notebook server is run up thus:

```
EINARNN-M-D10Q:ncc einarnn$ pwd
/opt/git-repos/ncc
EINARNN-M-D10Q:ncc einarnn$ . v/bin/activate
(v) EINARNN-M-D10Q:ncc einarnn$ jupyter notebook
[I 16:39:38.230 NotebookApp] The port 8888 is already in use, trying another port.
[I 16:39:38.240 NotebookApp] Serving notebooks from local directory: /opt/git-repos/ncc
[I 16:39:38.240 NotebookApp] 0 active kernels
[I 16:39:38.240 NotebookApp] The Jupyter Notebook is running at: http://localhost:8889/
[I 16:39:38.240 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```

When the notebook server is running, it will also open up a web page with your default web browser, pointing to the jupyter notebook server. Just pick one of the notebooks in the [notebooks](notebooks) directory (```*.ipynb```) and away you go!!
