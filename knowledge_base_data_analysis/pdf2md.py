#!/usr/bin/env python3
"""
Instrument Datasheet & Programming Guide to Markdown Converter
==============================================================

Optimized for Keysight/test instrument datasheets.
Extracts: SCPI command tables, specifications, examples, block diagrams.

Usage:
    python extract_instrument_pdf.py <datasheet.pdf> [output.md]
    python extract_instrument_pdf.py keysight_psu.pdf --scpi-only
    python extract_instrument_pdf.py --batch *.pdf
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed. Install with: pip install pdfplumber")
    sys.exit(1)


@dataclass
class ExtractConfig:
    """Configuration for PDF extraction."""
    scpi_only: bool = False          # Extract only SCPI commands
    include_images: bool = False      # Try to preserve image captions
    min_table_cols: int = 2           # Minimum columns to consider a table
    max_heading_len: int = 150        # Max length to consider a heading
    debug: bool = False


def is_scpi_command_row(text: str) -> bool:
    """Detect if row contains SCPI command (starts with : or common root)."""
    s = text.strip()
    if not s:
        return False
    # SCPI commands usually start with : or root like VOLT, CURR, MEAS, CONF, etc.
    return (s.startswith(':') or 
            re.match(r'^(VOLT|CURR|MEAS|CONF|OUTP|TRIG|INIT|SENS|SOUR|READ|FETC|CAL|SYST|STAT|INST|LIST|WAV|TIME|FREQ)\b', s.upper()))


def format_scpi_table(table: List[List[str]]) -> str:
    """Format SCPI command table with special highlighting."""
    if not table or len(table) < 1:
        return ""
    
    def clean_cell(cell):
        if cell is None:
            return ""
        s = str(cell).strip()
        s = ' '.join(s.split())
        return s
    
    # Check header
    first_row = [clean_cell(c) for c in table[0]]
    if not any(first_row):
        return ""
    
    # Detect if this is a SCPI command table
    is_scpi_table = any(is_scpi_command_row(cell) for cell in first_row)
    
    md_lines = []
    
    # Header
    if is_scpi_table:
        md_lines.append("| SCPI Command | Description | Parameters |")
        md_lines.append("|---|---|---|")
    else:
        md_lines.append("| " + " | ".join(first_row) + " |")
        md_lines.append("|" + "|".join(["---"] * len(first_row)) + "|")
    
    # Data rows
    for row in table[1:]:
        clean_row = [clean_cell(c) for c in row]
        if is_scpi_table and len(clean_row) >= 1:
            # Format SCPI row: command | description | notes
            cmd = clean_row[0] if clean_row[0] else ""
            desc = clean_row[1] if len(clean_row) > 1 else ""
            notes = clean_row[2] if len(clean_row) > 2 else ""
            if cmd.startswith(':') or is_scpi_command_row(cmd):
                md_lines.append(f"| `{cmd}` | {desc} | {notes} |")
            else:
                md_lines.append("| " + " | ".join(clean_row) + " |")
        else:
            md_lines.append("| " + " | ".join(clean_row) + " |")
    
    return "\n".join(md_lines)


def format_table(table: List[List[str]]) -> str:
    """Format generic table as markdown."""
    if not table or len(table) < 1:
        return ""
    
    def clean_cell(cell):
        if cell is None:
            return ""
        s = str(cell).strip()
        s = ' '.join(s.split())
        # Escape pipes in cell content
        s = s.replace('|', '\\|')
        return s
    
    first_row = [clean_cell(c) for c in table[0]]
    if not any(first_row):
        return ""
    
    md_lines = []
    md_lines.append("| " + " | ".join(first_row) + " |")
    md_lines.append("|" + "|".join(["---"] * len(table[0])) + "|")
    
    for row in table[1:]:
        clean_row = [clean_cell(c) for c in row]
        md_lines.append("| " + " | ".join(clean_row) + " |")
    
    return "\n".join(md_lines)


def detect_heading(text: str, config: ExtractConfig) -> Optional[str]:
    """Detect and format heading. Returns markdown heading or None."""
    stripped = text.strip()
    
    if not stripped or len(stripped) > config.max_heading_len:
        return None
    
    # Very short + all caps (section title)
    if len(stripped) < 100 and stripped.isupper() and len(stripped) > 3:
        return f"### {stripped}"
    
    # Numbered section (e.g. "3.2.1 SCPI Commands")
    if re.match(r'^\d+[\.\s]', stripped):
        return f"### {stripped}"
    
    # Common datasheet section keywords
    keywords = [
        'specification', 'feature', 'parameter', 'description', 
        'performance', 'rating', 'interface', 'command', 'example',
        'connection', 'calibration', 'measurement', 'application',
        'scpi', 'programming', 'table', 'definition', 'syntax',
        'format', 'response', 'error', 'status', 'register'
    ]
    
    lower_text = stripped.lower()
    if any(lower_text.startswith(kw) for kw in keywords):
        return f"### {stripped}"
    
    # Standalone uppercase line (likely a section)
    if stripped.isupper() and len(stripped) > 5:
        return f"### {stripped}"
    
    return None


def extract_code_blocks(text: str) -> Tuple[str, List[str]]:
    """Extract probable code examples and return cleaned text + examples."""
    lines = text.split('\n')
    examples = []
    cleaned = []
    in_code = False
    code_buffer = []
    
    for line in lines:
        # Detect code-like content (indented, contains symbols, etc.)
        if (line.startswith(('    ', '\t')) or 
            re.search(r'[:=\[\]{}<>]', line) or
            line.strip().startswith(('*IDN?', ':', 'VOLT', 'CURR'))):
            if not in_code:
                in_code = True
                code_buffer = []
            code_buffer.append(line)
        else:
            if in_code and code_buffer:
                examples.append('\n'.join(code_buffer))
                code_buffer = []
                in_code = False
            cleaned.append(line)
    
    if code_buffer:
        examples.append('\n'.join(code_buffer))
    
    return '\n'.join(cleaned), examples


def process_page(text: str, page_num: int, config: ExtractConfig) -> str:
    """Process page text with structure detection."""
    if not text:
        return ""
    
    if config.scpi_only:
        # Filter to only SCPI-related lines
        lines = [l for l in text.split('\n') if is_scpi_command_row(l) or 'SCPI' in l.upper()]
        text = '\n'.join(lines)
    
    lines = text.split('\n')
    output = []
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            output.append("")
            continue
        
        # Detect and format headings
        heading = detect_heading(stripped, config)
        if heading:
            output.append(f"\n{heading}\n")
        else:
            output.append(stripped)
    
    result = '\n'.join(output)
    
    # Clean up excessive blank lines
    result = re.sub(r'\n\n\n+', '\n\n', result)
    
    return result


def extract_datasheet(pdf_path: Path, output_path: Path, config: ExtractConfig = None, verbose: bool = True):
    """Extract instrument datasheet/programming guide to markdown."""
    
    if config is None:
        config = ExtractConfig()
    
    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}")
        return False
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header with metadata
            f.write(f"# {pdf_path.stem}\n\n")
            f.write(f"**Source PDF:** `{pdf_path.name}`\n\n")
            f.write(f"**Extracted:** {Path(output_path).stat().st_mtime}\n\n")
            f.write("---\n\n")
            
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages, 1):
                    if verbose:
                        print(f"  Page {page_num}/{total_pages}...", end='', flush=True)
                    
                    # Section marker
                    f.write(f"## Page {page_num}\n\n")
                    
                    # Extract and process text
                    text = page.extract_text()
                    if text:
                        processed = process_page(text, page_num, config)
                        f.write(processed)
                        f.write("\n\n")
                    
                    # Extract tables (including SCPI command tables)
                    tables = page.extract_tables()
                    if tables:
                        f.write("### Tables on this Page\n\n")
                        for table_idx, table in enumerate(tables, 1):
                            # Decide which formatter to use
                            if any(is_scpi_command_row(cell[0]) if cell else False for cell in table[:3]):
                                formatted = format_scpi_table(table)
                            else:
                                formatted = format_table(table)
                            
                            if formatted:
                                f.write(formatted)
                                f.write("\n\n")
                    
                    if verbose:
                        print(" ✓")
        
        if verbose:
            file_size = output_path.stat().st_size / 1024
            print(f"\n✓ Extraction complete!")
            print(f"  Source:  {pdf_path}")
            print(f"  Output:  {output_path}")
            print(f"  Size:    {file_size:.1f} KB")
            print(f"  Pages:   {total_pages}")
        
        return True
    
    except Exception as e:
        print(f"\nERROR: {e}")
        if config.debug:
            import traceback
            traceback.print_exc()
        return False


def main():
    """Main entry point with argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Extract instrument datasheets/programming guides to Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_instrument_pdf.py datasheet.pdf
  python extract_instrument_pdf.py datasheet.pdf output.md
  python extract_instrument_pdf.py keysight_psu.pdf --scpi-only
  python extract_instrument_pdf.py --batch keysight*.pdf
        """
    )
    
    parser.add_argument('pdf', nargs='?', help='Input PDF file (or pattern with --batch)')
    parser.add_argument('-o', '--output', help='Output markdown file (default: input.md)')
    parser.add_argument('--scpi-only', action='store_true', help='Extract only SCPI commands')
    parser.add_argument('--batch', action='store_true', help='Process multiple files matching pattern')
    parser.add_argument('--debug', action='store_true', help='Show traceback on errors')
    
    args = parser.parse_args()
    
    if not args.pdf:
        parser.print_help()
        sys.exit(1)
    
    config = ExtractConfig(
        scpi_only=args.scpi_only,
        debug=args.debug
    )
    
    if args.batch:
        # Batch process
        from glob import glob
        pdf_files = glob(args.pdf)
        if not pdf_files:
            print(f"ERROR: No files matching pattern: {args.pdf}")
            sys.exit(1)
        
        print(f"Processing {len(pdf_files)} files...")
        for pdf_file in pdf_files:
            pdf_path = Path(pdf_file)
            output_path = pdf_path.with_suffix('.md')
            print(f"\n{pdf_path.name}")
            extract_datasheet(pdf_path, output_path, config, verbose=True)
    else:
        # Single file
        pdf_path = Path(args.pdf)
        
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = pdf_path.with_suffix('.md')
        
        extract_datasheet(pdf_path, output_path, config, verbose=True)


if __name__ == '__main__':
    main()
