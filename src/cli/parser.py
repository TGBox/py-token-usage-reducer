"""Command-line interface definition and command dispatching."""

import argparse
import sys
from pathlib import Path

from src.core.text_utils import format_token_savings
from src.core.tokenizer import count_tokens
from src.docs.manual import TOOL_DOCS, get_tool_documentation
from src.modules.converter import convert_to_markdown
from src.modules.data_reducer import reduce_data_file
from src.modules.dep_tracer import trace_dependencies
from src.modules.diff_packager import package_git_diff
from src.modules.log_compressor import compress_log_file, compress_logs
from src.modules.reporter import generate_project_report
from src.modules.skeletonizer import skeletonize_file


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser with rich help text."""
    parser = argparse.ArgumentParser(
        prog="py-token-usage-reducer",
        description="Werkzeuge zur lokalen Token-Reduktion beim Arbeiten mit KI-Coding-Agenten.",
        epilog="Nutze 'py-token-usage-reducer guide [BEFEHL]' für detaillierte Anleitungen und Praxisbeispiele.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--gui", action="store_true", help="Startet die PySide6 Desktop-Benutzeroberfläche."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Ausführliche Konsolenausgabe aktivieren."
    )

    subparsers = parser.add_subparsers(
        dest="subcommand", title="Verfügbare Werkzeuge", metavar="<BEFEHL>"
    )

    # 1. convert
    p_convert = subparsers.add_parser("convert", help=TOOL_DOCS["convert"].summary)
    p_convert.add_argument("file", help="Pfad zur Quelldatei (PDF, DOCX, HTML, IPYNB)")
    p_convert.add_argument("-o", "--output", help="Ausgabepfad für das generierte Markdown")
    p_convert.add_argument(
        "--include-outputs", action="store_true", help="Code-Ausgaben bei Notebooks beibehalten"
    )

    # 2. report
    p_report = subparsers.add_parser("report", help=TOOL_DOCS["report"].summary)
    p_report.add_argument("dir", nargs="?", default=".", help="Projektverzeichnis (Standard: .)")
    p_report.add_argument("-o", "--output", help="Ausgabepfad für den Markdown-Report")
    p_report.add_argument(
        "-s", "--skeletons", action="store_true", help="API-Skelette wichtiger Module einbetten"
    )
    p_report.add_argument(
        "--max-skeletons",
        type=int,
        default=5,
        help="Maximale Anzahl eingebetteter Skelette (Standard: 5)",
    )

    # 3. skeleton
    p_skel = subparsers.add_parser("skeleton", help=TOOL_DOCS["skeleton"].summary)
    p_skel.add_argument("file", help="Pfad zur Python-Datei (.py)")
    p_skel.add_argument("-o", "--output", help="Ausgabepfad")
    p_skel.add_argument("--no-docstrings", action="store_true", help="Entfernt auch Docstrings")

    # 4. schema
    p_schema = subparsers.add_parser("schema", help=TOOL_DOCS["schema"].summary)
    p_schema.add_argument("file", help="Pfad zur Datei (JSON, CSV, SQL)")
    p_schema.add_argument("-o", "--output", help="Ausgabepfad")
    p_schema.add_argument(
        "-s", "--samples", type=int, default=3, help="Anzahl Beispielzeilen (Standard: 3)"
    )

    # 5. compress-log
    p_log = subparsers.add_parser("compress-log", help=TOOL_DOCS["compress-log"].summary)
    p_log.add_argument(
        "file", nargs="?", help="Pfad zur Log- oder Traceback-Datei (ohne Angabe: stdin)"
    )
    p_log.add_argument("-o", "--output", help="Ausgabepfad")

    # 6. trace-deps
    p_deps = subparsers.add_parser("trace-deps", help=TOOL_DOCS["trace-deps"].summary)
    p_deps.add_argument("entry", help="Pfad zur Einstiegsdatei (.py)")
    p_deps.add_argument("--root", help="Projekt-Wurzelverzeichnis")
    p_deps.add_argument("--depth", type=int, default=3, help="Maximale Import-Tiefe (Standard: 3)")
    p_deps.add_argument("-o", "--output", help="Ausgabepfad für gebündeltes Kontext-Markdown")

    # 7. diff-pack
    p_diff = subparsers.add_parser("diff-pack", help=TOOL_DOCS["diff-pack"].summary)
    p_diff.add_argument(
        "dir", nargs="?", default=".", help="Git-Repository-Verzeichnis (Standard: .)"
    )
    p_diff.add_argument("--staged", action="store_true", help="Verwendet 'git diff --staged'")
    p_diff.add_argument(
        "--no-skeletons", action="store_true", help="Keine Schnittstellen-Skelette anhängen"
    )
    p_diff.add_argument("-o", "--output", help="Ausgabepfad")

    # 8. guide
    p_guide = subparsers.add_parser(
        "guide", help="Ausführliche Hilfe, Wann-nutzen-Anleitungen und Beispiele anzeigen"
    )
    p_guide.add_argument(
        "tool",
        nargs="?",
        help="Name des Werkzeugs (z. B. convert, report, skeleton) oder leer für Vollhandbuch",
    )

    return parser


def run_cli(args: list[str] | None = None) -> int:
    """Parse command-line arguments and run requested command. Returns status code (0 for success)."""
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    parser = build_parser()
    parsed = parser.parse_args(args)

    # If no subcommand given or --gui explicitly requested, signal to launch GUI
    if parsed.gui or not parsed.subcommand:
        return 100  # Exit code 100 indicates 'launch GUI'

    subcmd = parsed.subcommand

    try:
        if subcmd == "guide":
            print(get_tool_documentation(parsed.tool))
            return 0

        result_text = ""
        stats_info = ""

        if subcmd == "convert":
            res = convert_to_markdown(parsed.file, include_outputs=parsed.include_outputs)
            result_text = res["markdown"]
            stats_info = f"Tokens: {res['estimated_raw_tokens']:,} -> {res['reduced_tokens']:,} (Ersparnis: {res['tokens_saved']:,} Tokens)"

        elif subcmd == "report":
            res = generate_project_report(
                parsed.dir,
                include_skeletons=parsed.skeletons,
                max_skeleton_files=parsed.max_skeletons,
            )
            result_text = res["markdown"]
            stats_info = f"Projekt analysiert: {res['total_files']} Dateien, {res['total_tokens']:,} Tokens (~${res['estimated_cost_usd']:.4f})"

        elif subcmd == "skeleton":
            res = skeletonize_file(parsed.file, keep_docstrings=not parsed.no_docstrings)
            result_text = res["skeleton"]
            stats_info = f"Tokens: {res['original_tokens']:,} -> {res['reduced_tokens']:,} (-{res['percentage_saved']}%)"

        elif subcmd == "schema":
            res = reduce_data_file(parsed.file, max_samples=parsed.samples)
            result_text = res["reduced_markdown"]
            stats_info = f"Tokens: {res['original_tokens']:,} -> {res['reduced_tokens']:,} (-{res['percentage_saved']}%)"

        elif subcmd == "compress-log":
            if parsed.file:
                res = compress_log_file(parsed.file)
            else:
                raw = sys.stdin.read()
                compressed = compress_logs(raw)
                res = {
                    "compressed_log": compressed,
                    **format_token_savings(count_tokens(raw), count_tokens(compressed)),
                }
            result_text = res["compressed_log"]
            stats_info = f"Tokens: {res['original_tokens']:,} -> {res['reduced_tokens']:,} (-{res['percentage_saved']}%)"

        elif subcmd == "trace-deps":
            res = trace_dependencies(parsed.entry, project_root=parsed.root, max_depth=parsed.depth)
            result_text = res["bundled_markdown"]
            stats_info = f"Gebündelte Dateien: {len(res['dependency_files'])}, Gesamt-Tokens: {res['tokens']:,}"

        elif subcmd == "diff-pack":
            res = package_git_diff(
                parsed.dir, staged=parsed.staged, include_skeletons=not parsed.no_skeletons
            )
            result_text = res["packaged_markdown"]
            stats_info = f"Betroffene Dateien: {len(res['diff_files'])}, Tokens: {res['tokens']:,}"

        # Handle Output
        if hasattr(parsed, "output") and parsed.output:
            out_path = Path(parsed.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(result_text, encoding="utf-8")
            print(f"[Erfolg] Ausgabe gespeichert in: {out_path}")
            if stats_info:
                print(f"[Statistik] {stats_info}")
        else:
            # Print to stdout
            print(result_text)
            if parsed.verbose and stats_info:
                print(f"\n# --- Info: {stats_info} ---", file=sys.stderr)

        return 0

    except Exception as exc:  # noqa: BLE001
        print(f"[Fehler] {exc}", file=sys.stderr)
        return 1
