## Task 0: Parameterize a unit test

- Added `TestAccessNestedMap` in `test_utils.py`.
- Used `@parameterized.expand` to test multiple inputs:
  - `{"a": 1}, ("a",)` → `1`
  - `{"a": {"b": 2}}, ("a",)` → `{"b": 2}`
  - `{"a": {"b": 2}}, ("a", "b")` → `2`
- Verified outputs with `assertEqual`.
