#!/bin/bash
set -euo pipefail

PROJECT_DIR="/home/gris/.hermes/workspace/ACTIVE/protein-lab"
PREPRINT_DIR="$PROJECT_DIR/investigacion-fibromialgia"
MANUSCRIPT="$PREPRINT_DIR/preprint_dopaminergic_convergence_FM.md"
OUTPUT_DIR="$PROJECT_DIR/artifacts/manuscript/v2.14"
BUILD_DIR="$OUTPUT_DIR/build"
PDF_NAME="FM_transcriptomic_reframing_v2.14.pdf"

mkdir -p "$OUTPUT_DIR" "$BUILD_DIR"

echo "=== Generating PDF v2.14 (pandoc HTML + weasyprint) ==="
echo "Source: $MANUSCRIPT"
echo "Output: $OUTPUT_DIR/$PDF_NAME"
echo ""

# Step 1: Convert Markdown to HTML
echo "[1/3] Converting Markdown to HTML..."
pandoc "$MANUSCRIPT" \
    --from markdown+tex_math_dollars+yaml_metadata_block+pipe_tables+multiline_tables+table_captions+smart \
    --to html5 \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --standalone \
    -o "$BUILD_DIR/manuscript.html"

# Step 2: Create CSS
echo "[2/3] Creating CSS..."
cat > "$BUILD_DIR/style.css" << 'CSS'
@page {
    size: A4;
    margin: 2.5cm 2cm 2cm 2cm;
    @top-center {
        content: "Peripheral Transcriptomic Reframing of Fibromyalgia";
        font-size: 9pt;
        color: #666;
    }
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        color: #666;
    }
}
body {
    font-family: "Georgia", "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #222;
    max-width: 100%;
}
h1 {
    font-size: 16pt;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
}
h2 {
    font-size: 14pt;
    font-weight: bold;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
}
h3 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 0.3em;
}
p {
    margin-bottom: 0.8em;
    text-align: justify;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 10pt;
}
th {
    background-color: #f0f0f0;
    border: 1px solid #999;
    padding: 8px 6px;
    font-weight: bold;
    text-align: left;
}
td {
    border: 1px solid #ccc;
    padding: 6px;
}
tr:nth-child(even) {
    background-color: #f9f9f9;
}
a {
    color: #0066cc;
    text-decoration: none;
}
pre {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 3px;
    padding: 10px;
    font-size: 9pt;
    overflow-x: auto;
    white-space: pre-wrap;
}
code {
    font-family: "Courier New", monospace;
    font-size: 9pt;
    background-color: #f5f5f5;
    padding: 2px 4px;
}
blockquote {
    border-left: 4px solid #0066cc;
    padding-left: 1em;
    margin: 1em 0;
    color: #555;
    font-style: italic;
}
ul, ol {
    margin-bottom: 0.8em;
}
li {
    margin-bottom: 0.3em;
}
.caption {
    font-size: 9pt;
    color: #555;
    text-align: center;
    margin-top: 0.5em;
    margin-bottom: 1em;
}
CSS

# Step 3: Generate PDF with weasyprint
echo "[3/3] Generating PDF with weasyprint..."
WEASYPRINT_DEBIAN=1 /tmp/venv-weasy/bin/weasyprint \
    --base-url "$BUILD_DIR" \
    --stylesheet "$BUILD_DIR/style.css" \
    "$BUILD_DIR/manuscript.html" \
    "$OUTPUT_DIR/$PDF_NAME"

if [ -f "$OUTPUT_DIR/$PDF_NAME" ]; then
    PDF_SIZE=$(stat -c%s "$OUTPUT_DIR/$PDF_NAME")
    PDF_SIZE_KB=$((PDF_SIZE / 1024))
    echo "  ✅ PDF generated: $PDF_SIZE_KB KB"
    echo "📄 PDF: $OUTPUT_DIR/$PDF_NAME"
    ls -lh "$OUTPUT_DIR/$PDF_NAME"
else
    echo "  ❌ PDF generation failed"
    exit 1
fi