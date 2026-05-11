# ibmdb2-sqlglot-plugin

IBM DB2 dialect plugin for [sqlglot](https://github.com/tobymao/sqlglot) — bidirectional transpilation between IBM DB2 and any SQL dialect.

## Installation

```bash
pip install ibmdb2-sqlglot-plugin
```

## Usage

After installing the package, the `db2` dialect is available in sqlglot automatically — no extra imports needed:

```python
import sqlglot

# Any dialect → IBM DB2
result = sqlglot.transpile("SELECT * FROM users WHERE id = 1", read="mysql", write="db2")[0]
# → SELECT * FROM `users` WHERE id = 1

# IBM DB2 → any dialect
result = sqlglot.transpile("$t = (SELECT id FROM users); SELECT * FROM $t AS t", read="db2", write="postgres")[0]
# → WITH t AS (SELECT id FROM users) SELECT * FROM t AS t
```

## What the plugin does
@TODO
---

## Development

```bash
## pip install uv # if uv does not exist locally
uv sync            # install dependencies
uv run pytest      # run all tests
```

## License

APACHE LICENSE 2.0