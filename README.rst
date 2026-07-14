FastAPI Project Template
========================

An idiomatic FastAPI project template featuring integrated C and Rust extension modules.

Features
--------

* **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.14.
* **Maturin**: Build system for Rust and C extensions, providing a seamless bridge between native code and Python.
* **Mixed Native Extensions**: Demonstrates how to include both C and Rust code in a single Python package.
* **Modern Tooling**: Uses ``uv`` for dependency management, ``ruff`` for linting/formatting, and ``pytest`` for testing.
* **Scalable Structure**: Organized for growth with clear separation of concerns.

Project Structure
-----------------

* ``src/fastapi_project_template/``: Main Python source code.
* ``rustlib/``: Rust extension source code.
* ``clib/``: C extension source code.
* ``Cargo.toml`` & ``build.rs``: Configuration for building native extensions.
* ``tests/``: Unit and integration tests.

Prerequisites
-------------

* Python 3.14+
* Rust toolchain (for building extensions)
* ``uv`` (recommended for dependency management)

Getting Started
---------------

1. **Clone the repository**:

   .. code-block:: bash

      git clone https://github.com/kamikaze/fastapi-project-template.git
      cd fastapi-project-template

2. **Set up the virtual environment**:

   .. code-block:: bash

      uv venv
      source .venv/bin/activate

3. **Install dependencies and build extensions**:

   For development, use ``maturin develop`` to build and install the native extensions in-place:

   .. code-block:: bash

      uv sync --group dev --group testing
      maturin develop

4. **Run the application**:

   .. code-block:: bash

      fastapi dev src/fastapi_project_template/api/http.py

Native Extensions
-----------------

The project includes a unified extension module ``_ext`` that exposes both C and Rust implementations:

* ``c_fib(n)``: Fibonacci calculation implemented in C.
* ``rust_fib(n)``: Fibonacci calculation implemented in Rust.

Example API Endpoint
^^^^^^^^^^^^^^^^^^^^

A demonstration endpoint is available at ``/api/app/v1/extensions/fibonacci``:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/app/v1/extensions/fibonacci \
        -H "Content-Type: application/json" \
        -d '{"n": 10}'

Development
-----------

Running Tests
^^^^^^^^^^^^^

.. code-block:: bash

   pytest

Linting and Formatting
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   ruff check .
   ruff format .

Building for Release
^^^^^^^^^^^^^^^^^^^^

To build a wheel for distribution:

.. code-block:: bash

   maturin build --release
