from pathlib import Path
from autorecon.plugins.subdom import SubdomPlugin

class Enumerator:
    def __init__(self, target: str, outdir: Path, cfg: dict):
        self.target = target
        self.outdir = outdir
        self.cfg    = cfg

    def run(self, data: dict):
        # Ejecutamos plugins que correspondan
        if "domain" in data:
            plug = SubdomPlugin()
            res = plug.run(self.target, 0, self.cfg.subdomain.model_dump())
            data.update(res)   # agrega {"subdomains": [...]}