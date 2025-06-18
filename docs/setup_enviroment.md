# Hướng Dẫn Thiết Lập Môi Trường Python với `uv` và `pre-commit`

Hướng dẫn này cung cấp các bước chi tiết để thiết lập một dự án Python sử dụng `uv` (một công cụ quản lý môi trường ảo và gói nhanh), cài đặt các công cụ linting/formatting (`flake8`, `isort`, `autoflake`, `black`), và cấu hình `pre-commit` để đảm bảo chất lượng code. Ngoài ra, hướng dẫn cũng bao gồm cách thiết lập `pytest` và `pytest-cov` để đạt coverage trên 5%.

---

## 1. Cài đặt `uv`

`uv` là công cụ quản lý môi trường ảo và gói Python, được viết bằng Rust, nhanh hơn so với `pip` hoặc `poetry`.

- **Cài đặt `uv`**:

  - Trên macOS/Linux:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
  - Trên Windows (PowerShell):
    ```powershell
    iwr https://astral.sh/uv/install.ps1 | iex
    ```
  - Hoặc dùng `pip`:
    ```bash
    pip install uv
    ```
- **Kiểm tra cài đặt**:

  ```bash
  uv --version
  ```

---

## 2. Thiết lập dự án Python với `uv`

1. **Tạo thư mục dự án**:

   ```bash
   mkdir my-python-project
   cd my-python-project
   ```
2. **Khởi tạo môi trường ảo**:

   ```bash
   uv venv
   ```

   Môi trường ảo sẽ được tạo tại `.venv`.
3. **Kích hoạt môi trường ảo**:

   - Trên macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - Trên Windows:
     ```bash
     .\.venv\Scripts\activate
     ```
4. **Khởi tạo tệp `pyproject.toml`**:

   ```bash
   uv init
   ```

   Tệp `pyproject.toml` sẽ được tạo để quản lý phụ thuộc và cấu hình dự án.

---

## 3. Cài đặt các thư viện cần thiết

Cài đặt các công cụ phát triển (`flake8`, `isort`, `autoflake`, `black`, `pytest`, `pytest-cov`, `pre-commit`) vào môi trường ảo.

- **Thêm các gói vào `pyproject.toml`**:

  ```bash
  uv add --dev flake8 isort autoflake black pytest pytest-cov pre-commit
  ```
- **Đồng bộ môi trường**:

  ```bash
  uv sync
  ```
- **Kiểm tra các gói đã cài**:

  ```bash
  uv pip list
  ```

---

## 4. Cấu hình `pre-commit`

`pre-commit` giúp chạy các công cụ linting/formatting trước khi commit code, đảm bảo chất lượng code.

1. **Tạo tệp `.pre-commit-config.yaml`**:
   Tạo tệp `.pre-commit-config.yaml` trong thư mục gốc của dự án với nội dung sau:

   ```yaml
   repos:
   - repo: https://github.com/pre-commit/pre-commit-hooks
     rev: v5.0.0
     hooks:
     - id: check-yaml
     - id: end-of-file-fixer
     - id: trailing-whitespace
   - repo: https://github.com/PyCQA/flake8
     rev: 7.1.1
     hooks:
     - id: flake8
   - repo: https://github.com/PyCQA/isort
     rev: 5.13.2
     hooks:
     - id: isort
       args: ["--profile", "black"]
   - repo: https://github.com/PyCQA/autoflake
     rev: v2.3.1
     hooks:
     - id: autoflake
       args: ["--in-place", "--remove-all-unused-imports", "--expand-star-imports", "--remove-duplicate-keys"]
   - repo: https://github.com/psf/black
     rev: 24.8.0
     hooks:
     - id: black
   ```
2. **Cài đặt `pre-commit` vào Git hooks**:

   ```bash
   pre-commit install
   ```
3. **Kiểm tra toàn bộ dự án**:

   ```bash
   pre-commit run --all-files
   ```

---

## 5. Thiết lập `coverage` để đạt tối thiểu 5%

Sử dụng `pytest` và `pytest-cov` để đo lường độ bao phủ của code (coverage).

1. **Tạo tệp `.coveragerc`**:
   Tạo tệp `.coveragerc` trong thư mục gốc của dự án:

   ```ini
   [run]
   source = .
   omit =
       tests/*
       .venv/*
       */__init__.py

   [report]
   fail_under = 5
   show_missing = true
   ```
2. **Ví dụ: Tạo mã và bài kiểm tra**:

   - Tạo tệp `my_module.py`:

     ```python
     def add(a, b):
         return a + b
     ```
   - Tạo thư mục `tests/` và tệp `tests/test_my_module.py`:

     ```python
     from my_module import add

     def test_add():
         assert add(2, 3) == 5
         assert add(-1, 1) == 0
     ```
3. **Chạy bài kiểm tra và đo coverage**:

   ```bash
   uv run pytest --cov=. --cov-report=term-missing
   ```
4. **Tạo báo cáo HTML (tùy chọn)**:

   ```bash
   uv run pytest --cov=. --cov-report=html
   ```

   Mở `htmlcov/index.html` trong trình duyệt để xem báo cáo chi tiết.
5. **Tích hợp coverage vào `pre-commit` (tùy chọn)**:
   Thêm hook sau vào `.pre-commit-config.yaml`:

   ```yaml
   - repo: local
     hooks:
     - id: pytest-cov
       name: Check test coverage
       entry: uv run pytest --cov=. --cov-fail-under=5
       language: system
       pass_filenames: false
       types: [python]
   ```

   Cài đặt lại hook:

   ```bash
   pre-commit install
   ```

---

## 6. Cấu hình `pyproject.toml` cho `pytest`

Thêm cấu hình `pytest` vào `pyproject.toml` để tự động áp dụng các tham số coverage:

```toml
[tool.pytest.ini_options]
addopts = "--cov=. --cov-report=term-missing --cov-report=html --cov-fail-under=5"
testpaths = ["tests"]
```

---

## 7. Workflow tổng quát

1. **Code**: Viết code trong các tệp Python (ví dụ: `my_module.py`).
2. **Test**: Viết bài kiểm tra trong thư mục `tests/` (ví dụ: `tests/test_my_module.py`).
3. **Linting/Formatting**: Chạy `pre-commit` để kiểm tra và định dạng code với `flake8`, `isort`, `autoflake`, và `black`.
4. **Coverage**: Chạy `pytest` để đo coverage, đảm bảo trên 5%.
5. **Commit**: Mỗi lần commit, `pre-commit` tự động kiểm tra code.

- **Kiểm tra toàn bộ**:
  ```bash
  pre-commit run --all-files
  uv run pytest --cov=. --cov-report=term-missing
  ```

---

## 8. Khắc phục sự cố

- **Lỗi `pytest` không nhận `--cov` hoặc `--cov-report`**:

  - Đảm bảo `pytest-cov` đã được cài đặt:
    ```bash
    uv add --dev pytest-cov
    uv sync
    ```
  - Kiểm tra danh sách gói:
    ```bash
    uv pip list
    ```
- **Coverage dưới 5%**:

  - Thêm nhiều bài kiểm tra vào thư mục `tests/` để bao phủ các phần code còn lại.
- **Lỗi `pre-commit`**:

  - Chạy `pre-commit run --all-files` để xem chi tiết lỗi.
  - Cập nhật phiên bản trong `.pre-commit-config.yaml` nếu cần.

---

## 9. Tài liệu tham khảo

- [uv documentation](https://docs.astral.sh/uv/)
- [pre-commit documentation](https://pre-commit.com/)
- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [coverage documentation](https://coverage.readthedocs.io/)
