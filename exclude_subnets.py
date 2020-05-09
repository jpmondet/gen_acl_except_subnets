#! /usr/bin/env python3

from os import access, R_OK
from sys import exit
from argparse import ArgumentParser
from ipaddress import ip_network
from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML



def extract_subnets_from_file(subnets_file):
    with open(subnets_file) as fsub:
        yaml = YAML(typ='safe')
        subnets_str = yaml.load(fsub)

    subnets = [] 
    for sub_str in subnets_str:
        subnets.append(ip_network(sub_str))

    return subnets

def get_sublist_from_excluded_subnet(subnet, supernet):
    return list(supernet.address_exclude(subnet))

def find_subnets_to_be_included(subnets, supernet):
    supnet = ip_network(supernet)

    subs_list = get_sublist_from_excluded_subnet(subnets[0], supnet)

    for sub in subnets[1:]:

        subs_to_check = subs_list.copy()
        subs_to_replace = []
        subs_to_add = []

        for sub_to_check in subs_to_check:
            try:
                subs_to_append = get_sublist_from_excluded_subnet(sub, sub_to_check)
            except ValueError:
                continue
            subs_to_replace.append(sub_to_check) 
            subs_to_add.extend(subs_to_append)

        for sub_to_replace in subs_to_replace:
            subs_list.pop(subs_list.index(sub_to_replace))
        subs_list.extend(subs_to_add)

    return subs_list

def generate_access_list(subnets):
    j2_env = Environment(
        loader=FileSystemLoader(".")#, trim_blocks=True, autoescape=True
    )
    template = j2_env.get_template("acl.j2")
    
    print(template.render(subnets=enumerate(subnets)))

    
def to_string_list(subnets):
    sub_list = []
    for sub in subnets:
        sub_list.append(str(sub))

    return sorted(sub_list, key=lambda k:int(k.split('.')[0]))



def main():
    parser = ArgumentParser(description='Generates exhaustive access-list entries to match all except a few subnets')
    parser.add_argument(
        "-fsub",
        "--subnets_file",
        type=str,
        help="File containing a list of subnets to exclude",
        default='subnets_to_exclude.yaml',
    )
    parser.add_argument(
        "-sup",
        "--supernet",
        type=str,
        help="supernet including the subnets to exclude",
        default='0.0.0.0/0',
    )

    args = parser.parse_args()

    if not access(args.subnets_file, R_OK):
        print(f"Error accessing file {args.fsub}")
        exit(1)

    excl_subs_list = extract_subnets_from_file(args.subnets_file)

    subs_to_incl = find_subnets_to_be_included(excl_subs_list, args.supernet)
    subs_str_to_incl = to_string_list(subs_to_incl)

    generate_access_list(subs_str_to_incl)

if __name__ == "__main__":
    main()
