#!/bin/bash
#
# Compile Arena ACM Paper
# Usage: ./compile_paper.sh [clean]
#

set -e

PAPER="arena_acm_paper"

# Add TeX Live to PATH
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"

# Clean if requested
if [ "$1" == "clean" ]; then
    echo "🧹 Cleaning auxiliary files..."
    rm -f ${PAPER}.aux ${PAPER}.bbl ${PAPER}.blg ${PAPER}.log ${PAPER}.out ${PAPER}.toc ${PAPER}.fdb_latexmk ${PAPER}.fls ${PAPER}.synctex.gz
    echo "✅ Clean complete"
    exit 0
fi

echo "📄 Compiling Arena ACM Paper..."
echo ""

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "❌ Error: pdflatex not found"
    echo "Please install a LaTeX distribution:"
    echo "  - macOS: brew install --cask mactex"
    echo "  - Ubuntu: sudo apt-get install texlive-full"
    echo "  - Windows: Download MiKTeX from https://miktex.org/"
    exit 1
fi

# Compile sequence
echo "1️⃣ First pass (pdflatex)..."
pdflatex -interaction=nonstopmode ${PAPER}.tex > /dev/null 2>&1
# Don't exit on warnings - check if PDF was created
if [ ! -f "${PAPER}.pdf" ]; then
    echo "❌ First pass failed. Check ${PAPER}.log for errors"
    exit 1
fi

echo "2️⃣ Processing bibliography (bibtex)..."
bibtex ${PAPER} > /dev/null 2>&1 || {
    echo "⚠️  BibTeX warning (may be normal if no citations)"
}

echo "3️⃣ Second pass (pdflatex)..."
pdflatex -interaction=nonstopmode ${PAPER}.tex > /dev/null 2>&1

echo "4️⃣ Third pass (pdflatex)..."
pdflatex -interaction=nonstopmode ${PAPER}.tex > /dev/null 2>&1

echo ""
echo "✅ Compilation successful!"
echo "📄 Output: ${PAPER}.pdf"
echo ""

# Show file size
if [ -f "${PAPER}.pdf" ]; then
    SIZE=$(du -h "${PAPER}.pdf" | cut -f1)
    echo "📊 File size: ${SIZE}"

    # Count pages (requires pdfinfo)
    if command -v pdfinfo &> /dev/null; then
        PAGES=$(pdfinfo "${PAPER}.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}')
        if [ ! -z "$PAGES" ]; then
            echo "📖 Pages: ${PAGES}"
        fi
    fi
fi

echo ""
echo "💡 To clean auxiliary files: ./compile_paper.sh clean"
echo "💡 To open PDF: open ${PAPER}.pdf"
