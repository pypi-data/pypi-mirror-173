# Python wrapper for Sort Me API

## Quick start
```python
import sortme

api = sortme.API()

print(api.problems.get_by_id(1).statement.legend)
# Требуется сложить два целых числа $$A$$ и $$B$$.

print(api.users.get_by_id(578).handle)
# imachug
```


