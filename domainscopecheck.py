import socket
import argparse
import ipaddress

domainsList = []
scope = []
validScope = {}
invalidDomains = []

parser = argparse.ArgumentParser(description="Checks if domain(s) in a file are in scope based on IP(s) from another file")

parser.add_argument('-c,', '-csv', '--csv', help='Defines whether files are separated by commas versus newlines', action="store_true")
parser.add_argument('-o,', '-output', '--output', help='File to write output to')
parser.add_argument('-d,', '--domains', '--domain', help='Domain file to read from', required=True)
parser.add_argument('-s,', '--scope', '--ips', '--ip', help='IP/Scope file to read from', required=True)

args = parser.parse_args()

domainFile = open(args.domains, "r")
scopeFile = open(args.scope, "r")

if args.csv:
    domain = domainFile.readline()
    domains = domain.replace(" ", "").strip("\n").split(",")
    for domain in domains:
        domainsList.append(domain)
else:
    for domain in domainFile.readlines():
        domain = domain.strip("\n")
        domainsList.append(domain)

if args.csv:
    ipLine = scopeFile.readline()
    ips = ipLine.replace(" ", "").strip("\n").split(",")
    for value in ips:
        if "/" in value:
            for ipValue in [str(ip) for ip in ipaddress.IPv4Network(value)]:
                scope.append(ipValue)
        else:
            scope.append(value)
else:
    for ipLine in scopeFile.readlines():
        ips = ipLine.strip("\n")
        if "/" in ips:
            for ipValue in [str(ip) for ip in ipaddress.IPv4Network(ips)]:
                scope.append(ipValue)
        else:
            scope.append(ips)

for domain in domainsList:
    try:
        ip = socket.gethostbyname(domain)
        if ip in scope:
            validScope[domain] = ip
    except Exception as e:
        invalidDomains.append(domain)

if args.output:
    outputFile = open(args.output, "w")

print("=====Valid Scope=====")
for k, v in validScope.items():
    print(k, ":", v)
    if args.output:
        outputFile.write(k, ":", v)

print("=====Invalid Domains=====")
for domain in invalidDomains:
    print(domain)
    if args.output:
        outputFile.write(domain)

if args.output:
    outputFile.close()
