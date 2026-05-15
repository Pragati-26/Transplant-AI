from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Match, User
from ..schemas import MatchHistoryItem
from ..dependencies import get_current_user
from ..utils.errors import NotFoundError

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/", response_model=List[MatchHistoryItem])
def get_history(
    skip:         int     = Query(default=0, ge=0),
    limit:        int     = Query(default=20, ge=1, le=100),
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    return (
        db.query(Match)
        .filter(Match.user_id == current_user.id)
        .order_by(Match.created_at.desc())
        .offset(skip).limit(limit)
        .all()
    )

@router.delete("/{match_id}", status_code=204)
def delete_match(
    match_id:     int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    match = db.query(Match).filter(
        Match.id == match_id,
        Match.user_id == current_user.id
    ).first()
    if not match:
        raise NotFoundError("Match not found")
    db.delete(match)
    db.commit()