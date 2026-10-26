"""Assemble report/0*_*.md + 1*_*.md into one Markdown/HTML document and print a PDF preview.

Usage: .venv/bin/python report/build.py
Outputs: report/build/report.md, report/build/report.html, report/build/report.pdf, report/build/figures/
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import markdown

R = Path(__file__).resolve().parent
OUT = R / "build"
FIG_SRC = R.parent / "src" / "results" / "main" / "figures"
FIGS = {  # report numbering -> analysis output
    "fig4_environment.png": "figure1_positive_control.png",
    "fig1_interaction.png": "figure2_family_interaction.png",
    "fig2_auroc_by_view.png": "figure3_auroc_by_view.png",
    "fig3_mitigation.png": "figureC1_mitigation.png",
}
FOOTNOTE = ("Research conducted at the [AI Collusion Research Sprint]"
            "(https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25), October 2026")
CSS = """
@page { size: A4; margin: 2.2cm 2.3cm; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt; line-height: 1.38; color: #111; }
h1 { font-size: 17pt; text-align: center; margin-bottom: 4pt; }
h2 { font-size: 13pt; margin: 14pt 0 4pt; }
h3 { font-size: 11pt; margin: 10pt 0 3pt; }
p, li { text-align: justify; }
img { display: block; margin: 6pt auto 2pt; max-width: 100%; }
img[alt="Figure 2"] { max-width: 58%; }
img[alt="Figure 3"] { max-width: 88%; }
img[alt="Figure 1"] { max-width: 60%; }
img[alt="Figure C1"] { max-width: 70%; }
table { border-collapse: collapse; margin: 6pt auto; font-size: 9pt; }
th, td { border: 1px solid #999; padding: 2pt 5pt; }
th { background: #eee; }
pre { font-size: 7.5pt; white-space: pre-wrap; background: #f6f6f6; padding: 6pt; }
code { font-size: 9pt; }
.authors { text-align: center; }
.footnote { font-size: 8.5pt; border-top: 1px solid #aaa; margin-top: 12pt; padding-top: 3pt; }
.pagebreak { page-break-before: always; }
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "figures").mkdir(exist_ok=True)
    for src, dst in FIGS.items():
        shutil.copy(FIG_SRC / src, OUT / "figures" / dst)
    parts = []
    for p in sorted(R.glob("[01][0-9]_*.md")):
        t = p.read_text()
        t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        for src, dst in FIGS.items():
            t = t.replace(f"../src/results/main/figures/{src}", f"figures/{dst}")
        if p.name.startswith("08_"):  # main body ends before References
            t = '<div class="pagebreak"></div>\n\n' + t
        parts.append(t.strip())
    md = "\n\n".join(parts)
    md = md.replace("**Authors:**", '<p class="authors">', 1)
    md = re.sub(r'(<p class="authors">)(.*?)\n', r"\1\2</p>\n", md, count=1)
    md = md.replace("\n## Abstract", f'\n<p class="footnote">¹ {markdown.markdown(FOOTNOTE)[3:-4]}</p>\n\n## Abstract', 1)
    md = re.sub(r"^(# .+)$", r"\1¹", md, count=1, flags=re.M)
    (OUT / "report.md").write_text(md)
    html = markdown.markdown(md, extensions=["tables", "fenced_code", "md_in_html"])
    (OUT / "report.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><title>Report</title>"
                                     f"<style>{CSS}</style></head><body>{html}</body></html>")
    browser = next((b for b in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"] if Path(b).exists()), None)
    if browser:
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={OUT / 'report.pdf'}", (OUT / "report.html").as_uri()],
                       check=False, capture_output=True, timeout=120)
    print("built", OUT)


if __name__ == "__main__":
    main()
