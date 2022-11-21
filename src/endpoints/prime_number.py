from fastapi import APIRouter
import sympy

router = APIRouter(
    prefix="/prime",
    tags=["Zadanie 1"]
)


@router.get("/{number}")
async def check_number(number: str):
    if check_correctnes(number):
        response = {"Is number prime": sympy.isprime(int(number))}
    else:
        response = {"Error handler": "Not valid input number"}
    return response

""" Helpers functions """


def check_correctnes(number: any) -> bool:
    try:
        temp = int(number)
        if temp <= 1 or temp > 9223372036854775807:
            return False
        else:
            return True
    except:
        return False
