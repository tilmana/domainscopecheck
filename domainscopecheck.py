import socket

domains = []
scope = []
validScope = {}
invalidDomains = []

domainFile = open("domains", "r")
scopeFile = open("scope", "r")

for d in domainFile.readlines():
    d = d.strip("\n")
    domains.append(d)

for s in scopeFile.readlines():
    s = s.strip("\n")
    scope.append(s)

for domain in domains:
    try:
        ip = socket.gethostbyname(domain)
        if ip in scope:
            validScope[domain] = ip
    except Exception as e:
        invalidDomains.append(domain)

for k, v in validScope.items():
    print(k, ":", v)

print("=====Invalid Domains=====")
for domain in invalidDomains:
    print(domain)
