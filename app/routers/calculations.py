from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Calculation
from app.schemas import CalculationCreate, CalculationRead, CalculationUpdate

router = APIRouter(prefix="/calculations", tags=["Calculations"])


@router.get("", response_model=list[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    calculations = db.query(Calculation).all()
    return calculations


@router.get("/{calculation_id}", response_model=CalculationRead)
def read_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    return calculation


@router.post("", response_model=CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(calculation_data: CalculationCreate, db: Session = Depends(get_db)):
    new_calculation = Calculation(
        expression=calculation_data.expression,
        result=calculation_data.result,
    )

    db.add(new_calculation)
    db.commit()
    db.refresh(new_calculation)

    return new_calculation


@router.put("/{calculation_id}", response_model=CalculationRead)
def update_calculation(
    calculation_id: int,
    calculation_data: CalculationUpdate,
    db: Session = Depends(get_db),
):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    update_data = calculation_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(calculation, field, value)

    db.commit()
    db.refresh(calculation)

    return calculation


@router.patch("/{calculation_id}", response_model=CalculationRead)
def patch_calculation(
    calculation_id: int,
    calculation_data: CalculationUpdate,
    db: Session = Depends(get_db),
):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    update_data = calculation_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(calculation, field, value)

    db.commit()
    db.refresh(calculation)

    return calculation


@router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    db.delete(calculation)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)