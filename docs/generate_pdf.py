"""
Génère les PDF des livrables à partir des fichiers Markdown.
Usage : python docs/generate_pdf.py
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

DOCS_DIR = Path(__file__).parent

CSS_STYLE = CSS(string="""
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    @page {
        margin: 2.5cm 2cm;
        @bottom-right {
            content: "Page " counter(page) " / " counter(pages);
            font-size: 9pt;
            color: #888;
        }
        @bottom-left {
            content: "Your Car Your Way — Confidentiel";
            font-size: 9pt;
            color: #888;
        }
    }

    body {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #222;
    }

    h1 {
        color: #1a3c5e;
        font-size: 22pt;
        border-bottom: 3px solid #1a3c5e;
        padding-bottom: 8px;
        margin-top: 0;
    }

    h2 {
        color: #1a3c5e;
        font-size: 16pt;
        border-bottom: 1px solid #ccc;
        padding-bottom: 4px;
        margin-top: 2em;
    }

    h3 {
        color: #2c5f8a;
        font-size: 13pt;
        margin-top: 1.5em;
    }

    h4 {
        color: #444;
        font-size: 11pt;
        margin-top: 1em;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        font-size: 10pt;
    }

    th {
        background-color: #1a3c5e;
        color: white;
        padding: 8px 10px;
        text-align: left;
    }

    td {
        padding: 7px 10px;
        border-bottom: 1px solid #ddd;
    }

    tr:nth-child(even) td {
        background-color: #f5f8fc;
    }

    code, pre {
        font-family: "Courier New", monospace;
        font-size: 9pt;
        background: #f4f4f4;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    pre {
        padding: 12px;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    code {
        padding: 1px 4px;
    }

    blockquote {
        border-left: 4px solid #1a3c5e;
        margin-left: 0;
        padding-left: 16px;
        color: #555;
        font-style: italic;
    }

    a {
        color: #1a3c5e;
    }

    ul, ol {
        padding-left: 1.5em;
    }

    li {
        margin: 4px 0;
    }

    hr {
        border: none;
        border-top: 1px solid #ccc;
        margin: 2em 0;
    }

    p strong {
        color: #1a3c5e;
    }
""")


def md_to_pdf(md_path: Path, pdf_path: Path):
    print(f"Conversion : {md_path.name} → {pdf_path.name}")
    text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "nl2br"],
    )
    full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"></head>
<body>{html_body}</body>
</html>"""
    HTML(string=full_html, base_url=str(DOCS_DIR)).write_pdf(
        pdf_path, stylesheets=[CSS_STYLE]
    )
    print(f"  ✓ Généré : {pdf_path}")


if __name__ == "__main__":
    md_to_pdf(
        DOCS_DIR / "cahier_des_charges.md",
        DOCS_DIR / "cahier_des_charges.pdf",
    )
    md_to_pdf(
        DOCS_DIR / "proposition_architecture.md",
        DOCS_DIR / "proposition_architecture.pdf",
    )
    print("\nTous les PDF ont été générés dans le dossier docs/.")
