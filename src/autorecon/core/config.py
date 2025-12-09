from pathlib import Path
import yaml
from pydantic import BaseModel, Field

DEFAULT_CFG = Path(__file__).with_suffix("").parent.parent / "config" / "default.yaml"

class ScannerConf(BaseModel):
    fast_ports: str = "top 1000"
    full_ports: str = "1-65535"
    timing: str = "-T4"

class SubdomainConf(BaseModel):
    enabled: bool = True
    brute: bool = False
    wordlist: str = "builtin"
    tools: list[str] = Field(default_factory=lambda: ["subfinder", "dnsx", "ffuf"])
    wildcard_filter: bool = True
    rescan_new_ips: str = "ask"

class PluginsConf(BaseModel):
    http: bool = True
    ftp: bool = True
    smb: bool = True
    ssh: bool = True
    dns: bool = True
    subdom: bool = True

class Config(BaseModel):
    scanner: ScannerConf = Field(default_factory=ScannerConf)
    subdomain: SubdomainConf = Field(default_factory=SubdomainConf)
    plugins: PluginsConf = Field(default_factory=PluginsConf)

def load_config(extra: Path | None = None) -> Config:
    """Carga default.yaml (del paquete) y opcionalmente user-config."""
    with DEFAULT_CFG.open() as f:
        data = yaml.safe_load(f)
    if extra and extra.exists():
        with extra.open() as f:
            data |= yaml.safe_load(f)
    return Config(**data)