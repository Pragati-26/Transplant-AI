import joblib
import json
import numpy as np
import pandas as pd
from pathlib import Path
from ..utils.errors import AIServiceError

ML_DIR = Path(__file__).parent.parent / "ml"

try:
    model   = joblib.load(ML_DIR / "model.pkl")
    scaler  = joblib.load(ML_DIR / "scaler.pkl")
    with open(ML_DIR / "features.json") as f:
        FEATURES = json.load(f)
    print(f"ML model loaded successfully. Features: {FEATURES}")
except Exception as e:
    raise RuntimeError(f"Failed to load ML model files from {ML_DIR}: {e}")


def compute_ml_score(data: dict) -> float:
    try:
        # Blood type compatibility
        def clean(b): return str(b).upper().replace('+','').replace('-','')
        abo_map = {
            ('O','O'):1,   ('O','A'):0,   ('O','B'):0,   ('O','AB'):0,
            ('A','A'):1,   ('A','AB'):1,  ('A','O'):0,   ('A','B'):0,
            ('B','B'):1,   ('B','AB'):1,  ('B','O'):0,   ('B','A'):0,
            ('AB','AB'):1, ('AB','A'):0,  ('AB','B'):0,  ('AB','O'):0,
        }
        d_blood        = clean(data['donor_blood_type'])
        p_blood        = clean(data['patient_blood_type'])
        abo_compatible = abo_map.get((d_blood, p_blood), 0)
        blood_exact    = int(d_blood == p_blood)
        age_gap        = abs(data['patient_age'] - data['donor_age'])
        weight_gap     = abs(data['patient_weight'] - data['donor_weight'])
        donor_age_ok   = int(data['donor_min_age'] <= data['donor_age'] <= data['donor_max_age'])
        donor_wt_ok    = int(data['donor_min_weight'] <= data['donor_weight'] <= data['donor_max_weight'])

        feature_map = {
            'Patient_Age':                  data['patient_age'],
            'Patient_Weight':               data['patient_weight'],
            'Patient_BMI':                  data['patient_bmi'],
            'Donor_Age':                    data['donor_age'],
            'Donor_Weight':                 data['donor_weight'],
            'Donor_Min_Age':                data['donor_min_age'],
            'Donor_Max_Age':                data['donor_max_age'],
            'Donor_Min_Weight':             data['donor_min_weight'],
            'Donor_Max_Weight':             data['donor_max_weight'],
            'abo_compatible':               abo_compatible,
            'blood_exact_match':            blood_exact,
            'age_gap':                      age_gap,
            'weight_gap':                   weight_gap,
            'donor_age_in_range':           donor_age_ok,
            'donor_weight_in_range':        donor_wt_ok,
            'RealTime_Organ_HealthScore':   data['health_score'],
            'Biological_Markers':           data['biological_markers'],
            'Predicted_Survival_Chance':    data['survival_chance'],
            'Donor_Medical_Approval':       1,
        }

        row        = pd.DataFrame([[feature_map[f] for f in FEATURES]], columns=FEATURES)
        row_scaled = scaler.transform(row)
        prob       = float(model.predict_proba(row_scaled)[0][1])
        return round(prob, 4)

    except KeyError as e:
        raise AIServiceError(f"Missing feature — check features.json matches training: {e}")
    except Exception as e:
        raise AIServiceError(f"ML scoring error: {e}")