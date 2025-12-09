import subprocess
from pathlib import Path
from typing import Dict, List

from autorecon.plugins.base import PluginABC

class SubdomPlugin(PluginABC):
    def accept(self, service: str, port: int) -> bool:
        # Se activa solo si el usuario pasó --domain
        return service == "domain"

    def run(self, target: str, port: int, config: dict) -> Dict[str, List[str]]:
        """Devuelve lista de subdominios descubiertos."""
        tools   = config.get("tools", ["subfinder", "dnsx"])
        brute   = config.get("brute", False)
        wordlist= config.get("wordlist", "builtin")
        outdir  = Path("output") / target
        outdir.mkdir(exist_ok=True, parents=True)

        domain = target   # en este caso target es el dominio
        subs: set[str] = set()

        # 1. subfinder (pasivo)
        if "subfinder" in tools:
            try:
                r = subprocess.run(["subfinder", "-d", domain, "-silent"],
                                   capture_output=True, text=True, timeout=60)
                if r.returncode == 0:
                    subs.update(r.stdout.splitlines())
            except Exception:
                pass

        # 2. dnsx (resolución + wildcard filter)
        if "dnsx" in tools and subs:
            try:
                r = subprocess.run(["dnsx", "-l", "-", "-silent", "-wd", domain],
                                   input="\n".join(subs), text=True, capture_output=True, timeout=60)
                if r.returncode == 0:
                    subs = set(r.stdout.splitlines())
            except Exception:
                pass

        # 3. ffuf (brute) – solo si se activa
        if brute and "ffuf" in tools:
            wl = wordlist if wordlist != "builtin" else "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
            try:
                r = subprocess.run([
                    "ffuf", "-u", f"https://FUZZ.{domain}", "-w", wl,
                    "-mc", "200,204,301,302,307,401,403", "-s", "-t", "50"
                ], capture_output=True, text=True, timeout=120)
                if r.returncode == 0:
                    for line in r.stdout.splitlines():
                        if "FUZZ" in line:
                            subs.add(line.split()[1] + "." + domain)
            except Exception:
                pass

        # guardamos lista cruda
        outfile = outdir / "subdomains.txt"
        outfile.write_text("\n".join(sorted(subs)))
        return {"subdomains": sorted(subs)}