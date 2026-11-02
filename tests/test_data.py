import pandas as pd
from safety_anomaly.data.audit import audit_frame
from safety_anomaly.data.clean import prepare_records


def sample_frame():
    return pd.DataFrame({
        "ID": [10, 10, 12], "UPA": [100, 101, 102],
        "EventDate": ["1/1/2020", "1/2/2020", "bad-date"],
        "Primary NAICS": ["123456", None, "123456"],
        "Final Narrative": ["Worker fell", "Burn injury", "Machine incident"],
        "NatureTitle": ["Fracture", "Burn", "Cut"],
        "Part of Body Title": ["Leg", "Arm", "Hand"],
        "EventTitle": ["Fall", "Burn", "Caught in"],
        "SourceTitle": ["Floor", "Torch", "Machine"],
        "Secondary Source Title": [None, "Surface", "Guard"],
    })


def test_audit_distinguishes_id_reuse_from_full_duplicates():
    audit = audit_frame(sample_frame())
    assert audit["rows"] == 3
    assert audit["unique_upa"] == 3
    assert audit["exact_duplicate_rows"] == 0
    assert audit["duplicated_id_rows_including_first"] == 2


def test_prepare_records_parses_dates_and_keeps_rows():
    prepared = prepare_records(sample_frame())
    assert len(prepared) == 3
    assert str(prepared["EventDate"].dtype).startswith("datetime64")
    assert prepared["EventDate"].isna().sum() == 1
