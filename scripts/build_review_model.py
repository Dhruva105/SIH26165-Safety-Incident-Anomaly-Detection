"""Fit the deployable incident-review model from the local OSHA source file."""
from pathlib import Path
import argparse
import pandas as pd
from safety_anomaly.operational_review import IncidentReviewEngine

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample-size', type=int, default=5000)
    parser.add_argument('--input', default=str(ROOT / 'data/raw/January2015toNovember2025.csv'))
    parser.add_argument('--output', default=str(ROOT / 'artifacts/models/incident_review_engine.joblib'))
    args = parser.parse_args()
    frame = pd.read_csv(args.input, low_memory=False)
    engine = IncidentReviewEngine.fit(frame, sample_size=args.sample_size)
    engine.save(args.output)
    print(f'Saved: {args.output}')
    print(f'Reference rows: {len(engine.reference_rows):,}')
    print(f'Feature dimensions: {engine.features.X.shape[1]}')
    print(f'Flag threshold: {engine.threshold:.6f}')
    print(f'Model version: {engine.model_version}')

if __name__ == '__main__':
    main()
