# CodeFlow Visualizer - QA Test Suite

A comprehensive, modular, and production-grade quality assurance testing framework for the CodeFlow Visualizer API.

## Features

✅ **No Blocking Operations** - Fully automated, no user input required
✅ **Timeout Protection** - All requests have configurable timeouts (default: 5s)
✅ **Modular Structure** - Four independent test modules for selective execution
✅ **Detailed Logging** - Clear pass/fail reporting with timing metrics
✅ **Structured Output** - JSON reports for CI/CD integration
✅ **Fast Execution** - Completes in under 2 minutes
✅ **Production-Ready** - Error handling, concurrent testing, resource management

## Test Modules

### 1. Functional Tests (`test_functional.py`)
Core functionality validation:
- Health check endpoint
- Simple code execution
- Arithmetic operations
- Loops and control flow
- Function definitions
- List/Dictionary operations
- String operations
- Error handling (syntax, runtime, undefined variables)
- Input/output handling

**Count:** 12 tests

### 2. Performance Tests (`test_performance.py`)
Performance and throughput measurement:
- Simple operation response time (5 iterations)
- Complex operation response time (3 iterations)
- Concurrent request handling (5 parallel)
- Sequential throughput (10 requests)

**Count:** 4 tests

### 3. Security Tests (`test_security.py`)
Security posture and sandboxing validation:
- File system access control
- Subprocess module availability
- os.system() restrictions
- Code injection attempts
- SQL injection handling
- Memory exhaustion protection
- eval() function behavior
- Arbitrary code execution in sandbox
- Import wildcard handling

**Count:** 9 tests

### 4. Edge Case Tests (`test_edge_cases.py`)
Boundary conditions and input validation:
- Empty code input
- Whitespace-only code
- Comments-only code
- Large code input (~8KB)
- Code exceeding max size (>10KB)
- Infinite loop detection (while True, while 1)
- Deep recursion handling
- Missing required fields validation
- Invalid JSON handling
- Special characters and Unicode
- Long input_data handling
- Input exceeding max size

**Count:** 14 tests

**Total: 39 tests**

## Requirements

```
Python 3.10+
requests >= 2.28.0
```

Install dependencies:
```bash
pip install requests
```

## Usage

### Run All Tests
```bash
python test_runner.py
```

### Run Specific Module
```bash
python test_runner.py --module functional
python test_runner.py --module performance
python test_runner.py --module security
python test_runner.py --module edge_cases
```

### Run Against Custom API URL
```bash
python test_runner.py --url http://api.example.com:8000
```

### Get Help
```bash
python test_runner.py --help
```

## Output

### Console Output
Each test is reported in real-time:
```
✓ Simple Print                                         [145ms]
✓ Arithmetic Operations                               [138ms]
✗ Dangerous Import: subprocess                        [200ms] - subprocess module accessible - security risk
```

### Report File
A detailed JSON report is generated: `test_report.json`

Example structure:
```json
{
  "timestamp": "2026-03-24T12:00:00",
  "base_url": "http://localhost:8000",
  "summary": {
    "total_tests": 39,
    "passed": 37,
    "failed": 2,
    "total_duration_ms": 15234
  },
  "modules": {
    "functional": {
      "status": "completed",
      "passed": 12,
      "failed": 0,
      "tests": [...]
    },
    "performance": {
      "status": "completed",
      "passed": 4,
      "failed": 0,
      "tests": [...]
    },
    ...
  }
}
```

## Timeout Configuration

All HTTP requests use a default timeout of **5 seconds**. This is configurable in each test module:

```python
REQUEST_TIMEOUT = 5  # seconds
```

## Performance Expectations

| Test Category | Typical Duration | Notes |
|---|---|---|
| Functional | 1-2 min | 12 tests, instant execution |
| Performance | 30-45 sec | 5 iterations + 5 concurrent |
| Security | 20-30 sec | 9 security validation tests |
| Edge Cases | 20-45 sec | Includes timeout tests |
| **Total** | **<2 min** | All 39 tests complete |

## Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

Suitable for CI/CD pipeline integration.

## Key Design Decisions

### No Blocking Operations
- No `input()` calls
- No indefinite waits
- All operations have explicit timeouts
- Concurrent operations use `ThreadPoolExecutor` with `max_workers` limit

### Modular Architecture
- Each test category is a separate class
- Tests can be run independently
- Easy to add new tests (implement method in class)
- Common utilities shared across modules

### Robust Error Handling
- All exceptions are caught and reported
- Timeouts are gracefully handled
- Invalid responses don't crash the suite
- Partial results are logged

### Performance Optimized
- Concurrent execution for performance tests
- Limited thread pool (3 workers) to avoid overwhelming localhost
- Fast feedback via console output
- Efficient memory usage

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run QA Tests
  run: |
    cd qa
    python test_runner.py --report test_report.json
    
- name: Upload Report
  uses: actions/upload-artifact@v3
  with:
    name: qa-report
    path: qa/test_report.json
```

### Local Development
```bash
# Terminal 1: Start backend
cd backend
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm install
npm run dev

# Terminal 3: Run tests
cd qa
python test_runner.py
```

## Troubleshooting

### Tests timeout on localhost
- Ensure backend (`http://localhost:8000`) is running
- Check backend is responsive: `curl http://localhost:8000`
- Increase `REQUEST_TIMEOUT` if running on slow machine

### Import errors
- Ensure you're in the `qa/` directory
- Install requests: `pip install requests`
- Check Python version: `python --version` (should be 3.10+)

### Module not found
- Create `__init__.py` in qa directory
- Ensure all test files are present

## Future Enhancements

- [ ] API response validation schema
- [ ] Load testing with configurable concurrency
- [ ] HTML report generation
- [ ] Performance regression detection
- [ ] Screenshot capture for UI tests
- [ ] Automated security scanning integration
- [ ] Test coverage metrics

## License

Same as CodeFlow Visualizer project

## Author

QA Team - CodeFlow Visualizer
