import subprocess
import json
from pathlib import Path
from typing import Dict, Any
import nmap
from pydantic import BaseModel

class Scanner:
    def __init__(self, target: str, outdir: Path, cfg: BaseModel):
        self.target = target
        self.outdir = outdir
        self.cfg = cfg.dict() if isinstance(cfg, BaseModel) else cfg

    def run_fast(self) -> Dict[str, Any]:
        """Escaneo rápido top 1000 TCP."""
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=self.target, arguments=f"-sSCV -Pn {self.cfg['timing']} --top-ports 1000  -")
            return self._parse_nmap(nm)
        except nmap.PortScannerError as e:
            raise ValueError(f"Nmap error: {e}")
        except Exception as e:
            raise RuntimeError(f"Escaneo rápido falló: {e}")

    def run_full(self) -> Dict[str, Any]:
        """Escaneo completo TCP + scripts por defecto."""
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=self.target, arguments=f"-sS -sV -Pn {self.cfg['timing']} -p- -oX -")
            return self._parse_nmap(nm)
        except nmap.PortScannerError as e:
            raise ValueError(f"Nmap error: {e}")
        except Exception as e:
            raise RuntimeError(f"Escaneo completo falló: {e}")

    def _parse_nmap(self, nm) -> Dict[str, Any]:
        result = {"target": self.target, "open": {}, "down_hosts": []}
        for host in nm.all_hosts():
            if nm[host].state() == "down":
                result["down_hosts"].append(host)
                continue
            
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                open_ports = {
                    str(p): {
                        "state": nm[host][proto][p]["state"],
                        "name": nm[host][proto][p].get("name", ""),
                        "product": nm[host][proto][p].get("product", ""),
                        "version": nm[host][proto][p].get("version", ""),
                    }
                    for p in ports if nm[host][proto][p]["state"] == "open"
                }
                if open_ports:
                    result["open"][proto] = open_ports
        
        return result

    def save(self, data: Dict[str, Any], suffix: str = "scan") -> Path:
        self.outdir.mkdir(parents=True, exist_ok=True)
        out = self.outdir / f"{suffix}.json"
        try:
            out.write_text(json.dumps(data, indent=2))
            return out
        except Exception as e:
            raise IOError(f"No se pudo guardar en {out}: {e}")