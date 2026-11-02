"""Command-line interface."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from safety_anomaly.config import resolve_project_path
from safety_anomaly.data.audit import run_audit
from safety_anomaly.pipeline import run_pipeline


def build_parser():
    parser = argparse.ArgumentParser(prog="safety-anomaly", description="OSHA incident anomaly analysis")
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="Run a dataset quality audit")
    audit.add_argument("--data", default="data/raw/January2015toNovember2025.csv")
    audit.add_argument("--output", default="reports/data_audit")
    run = sub.add_parser("run", help="Run feature engineering and IF/LOF experiments")
    run.add_argument("--data", default="data/raw/January2015toNovember2025.csv")
    run.add_argument("--config", default="configs/default.yaml")
    run.add_argument("--sample-size", type=int, default=None)
    run.add_argument("--quick", action="store_true", help="Run smaller parameter grids")
    run.add_argument("--representation", choices=["structured", "structured_injury", "structured_text"], default=None)
    run.add_argument("--output", default="artifacts")
    return parser


def main():
    args = build_parser().parse_args()
    if args.command == "audit":
        result = run_audit(resolve_project_path(args.data), resolve_project_path(args.output))
    else:
        result = run_pipeline(args.data, config_path=args.config, sample_size=args.sample_size,
                              quick=args.quick, representation=args.representation, output_dir=args.output)
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
