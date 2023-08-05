from spinsrv import spinpy as sp
from spinsrv import spin

kc = sp.KeyServerHTTPClient()
resp = kc.which(
    spin.KeyWhichRequest(
        public="proteins",
        private="proteins",
    )
)
print(resp)
kc.temp(
    spin.KeyTempRequest(
        public="proteins",
        private="proteins",
        duration=60000000000,
    )
)

dc = sp.DirServerHTTPClient()
dc.lookup("proteins", "proteins", "proteins", "/")
dc.list("proteins", "proteins", "proteins", "/")
dc.tree("proteins", "proteins", "proteins", "/", 1)

assert kc.url != ""
