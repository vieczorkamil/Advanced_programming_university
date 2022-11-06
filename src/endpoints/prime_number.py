from fastapi import APIRouter
import sympy

router = APIRouter(
    prefix="/prime",
    tags=["Zadanie 1"]
)


@router.get("/{number}")
async def check_number(number: int):
    if check_correctnes(number):
        response = {"Is number prime": sympy.isprime(number)}
    else:
        response = {"Error handler": "Not valid input number"}
    return response

""" Helpers functions """


def check_correctnes(number: int) -> bool:
    if number <= 1:
        return False
    else:
        return True
