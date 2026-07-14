import logging

from fastapi import APIRouter
from pydantic import BaseModel

from fastapi_project_template import c_fib, rust_fib

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/extensions', tags=['extensions'])


class FibonacciRequest(BaseModel):
    n: int


class FibonacciResponse(BaseModel):
    n: int
    c_result: int
    rust_result: int


@router.post('/fibonacci', response_model=FibonacciResponse)
async def calculate_fibonacci(request: FibonacciRequest) -> FibonacciResponse:
    """
    Demonstrates the usage of C and Rust extensions by calculating Fibonacci numbers.
    """
    c_res = c_fib(request.n)
    rust_res = rust_fib(request.n)

    return FibonacciResponse(
        n=request.n,
        c_result=c_res,
        rust_result=rust_res,
    )
