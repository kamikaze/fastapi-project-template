from fastapi_project_template import c_fib, rust_fib


def test_c_fib() -> None:
    n = 10
    expected = 55
    assert c_fib(0) == 0
    assert c_fib(1) == 1
    assert c_fib(n) == expected


def test_rust_fib() -> None:
    n = 10
    expected = 55
    assert rust_fib(0) == 0
    assert rust_fib(1) == 1
    assert rust_fib(n) == expected
