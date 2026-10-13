import urllib.request, tarfile, io, hashlib, glob, sys, json

root = sys.argv[1]
files = glob.glob(root + "/lib/**/*.sol", recursive=True)
res = {f: "UNVERIFIED" for f in files}
pkgs = [
    ("@openzeppelin/contracts-upgradeable", "contracts-upgradeable", "/lib/openzeppelin-contracts-upgradeable/contracts/"),
    ("@openzeppelin/contracts", "contracts", "/lib/openzeppelin-contracts/contracts/"),
]
for pkg, short, prefix in pkgs:
    enc = pkg.replace("@", "%40").replace("/", "%2F")
    for ver in ["4.9.6", "4.9.5", "4.9.4", "4.9.3"]:
        url = "https://registry.npmjs.org/%s/-/%s-%s.tgz" % (enc, short, ver)
        try:
            data = urllib.request.urlopen(url, timeout=30).read()
        except Exception as e:
            print("fetch-fail", url, e)
            continue
        t = tarfile.open(fileobj=io.BytesIO(data))
        up = {}
        for m in t.getmembers():
            if m.isfile() and m.name.endswith(".sol"):
                up[m.name[len("package/"):]] = t.extractfile(m).read()
        for f in files:
            p = root + prefix
            if not f.startswith(p) or res[f].startswith("IDENTICAL"):
                continue
            rel = f[len(p):]
            if rel in up:
                a = hashlib.sha256(open(f, "rb").read()).hexdigest()
                b = hashlib.sha256(up[rel]).hexdigest()
                if a == b:
                    res[f] = "IDENTICAL@" + ver
                elif res[f] == "UNVERIFIED":
                    res[f] = "DIFFERENT(vs " + ver + ")"
for f, v in sorted(res.items()):
    print(v, f[len(root):])
