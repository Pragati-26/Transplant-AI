from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Match, User
from ..schemas import MatchRequest, MatchResult
from ..dependencies import get_current_user
from ..services.ml_service import compute_ml_score
from ..services.ai_service import get_explanation

router = APIRouter(prefix="/match", tags=["Match"])

@router.post("/", response_model=MatchResult)
def create_match(
    payload:      MatchRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    data = payload.model_dump()

    # Step 1 — ML model gives numeric score
    ml_score = compute_ml_score(data)

    # Step 2 — Claude gives recommendation + explanation
    ai_result = get_explanation(data, ml_score)

    # Step 3 — Save to database
    match = Match(
        user_id             = current_user.id,
        patient_age         = data['patient_age'],
        patient_weight      = data['patient_weight'],
        patient_bmi         = data['patient_bmi'],
        patient_blood_type  = data['patient_blood_type'],
        donor_age           = data['donor_age'],
        donor_weight        = data['donor_weight'],
        donor_blood_type    = data['donor_blood_type'],
        donor_min_age       = data['donor_min_age'],
        donor_max_age       = data['donor_max_age'],
        donor_min_weight    = data['donor_min_weight'],
        donor_max_weight    = data['donor_max_weight'],
        health_score        = data['health_score'],
        biological_markers  = data['biological_markers'],
        survival_chance     = data['survival_chance'],
        compatibility_score = ml_score,
        recommendation      = ai_result['recommendation'],
        explanation         = ai_result['explanation']
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match