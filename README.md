# GENerate ACL for Excluded Subnet In Supernet : GENAESIS

**[Still under development]**

Generate an ACL with all subnets composing a Supernet except those specified.  
This is very useful on plateforms that doesn't support `deny` entries (nxos on PBRs for example..)

## Installation

After `git clone`, entering the directory, creating a `venv` and activating it, a simple    
`python -m pip install -r requirements.txt` should do the trick.

## Quick Usage

Edit the file `subnets_to_exclude.yaml` with the subnets you want to exclude as a yaml list.

Then, using the defaults:

`python exclude_subnets.py`

## Options that could be of some use

`python exclude_subnets.py -h`

```
usage: exclude_subnets.py [-h] [-f SUBNETS_FILE] [-s SUPERNET] [-n ACL_NAME] [-p PLATFORM]

Generates exhaustive access-list entries to match all except a few subnets

optional arguments:
  -h, --help            show this help message and exit
  -f SUBNETS_FILE, --subnets_file SUBNETS_FILE
                        File containing a list of subnets to exclude default file: subnets_to_exclude.yaml
  -s SUPERNET, --supernet SUPERNET
                        supernet including the subnets to exclude default supernet: 0.0.0.0/0
  -n ACL_NAME, --acl_name ACL_NAME
                        Name of the ACL default name : SAMPLE_ACL_NAME
  -p PLATFORM, --platform PLATFORM
                        OS/platform for which the ACL should be generated default platform: nxos
```
