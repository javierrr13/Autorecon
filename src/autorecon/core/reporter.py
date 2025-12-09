import json
from pathlib import Path
from jinja2 import Template

class Reporter:
    def __init__(self, outdir: Path, template_path: Path | None = None):
        self.outdir   = outdir
        self.json_file= outdir / "scan.json"
        self.md_file  = outdir / "report.md"
        self.tpl_path = template_path or Path(__file__).with_suffix("").parent.parent / "templates" / "report.j2"

    def load(self) -> dict:
        return json.loads(self.json_file.read_text())

    def render(self, data: dict) -> str:
        tpl = Template(self.tpl_path.read_text())
        return tpl.render(**data)

    def save(self, text: str) -> Path:
        self.md_file.write_text(text)
        return self.md_file

    def run(self) -> Path:
        data = self.load()
        md   = self.render(data)
        return self.save(md)