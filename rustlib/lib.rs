use pyo3::prelude::*;

#[pymodule]
mod _rustmod {
    use pyo3::prelude::*;

    #[pyfunction]
    fn rust_fib(n: i32) -> PyResult<i32> {
        if n <= 0 {
            return Ok(0);
        }

        if n == 1 || n == 2 {
            return Ok(1);
        }

        let mut a = 1;
        let mut b = 1;

        for _ in 3..=n {
            let c = a + b;
            a = b;
            b = c;
        }

        Ok(b)
    }
}
