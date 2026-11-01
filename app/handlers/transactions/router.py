from fastapi import APIRouter

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("")
async def get_transactions():
    return {"status": "ok"}
