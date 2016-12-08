**How to test**

To run tests with pytest, type:
```bash
python3 -m pytest
```

To checkout coverage, install pytest-cov and run:
```bash
python3 -m pytest --cov=.
```

And then:

```bash
python3 -m pytest --cov=. --cov-config .coveragerc
```

**Tools installation**

```bash
pip3 install pytest pytest-cov
```
