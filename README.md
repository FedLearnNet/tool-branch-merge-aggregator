# branch-merge-aggregator

Combines two workflow tables by concatenating rows or columns, or by joining on a shared key.

This app is a lightweight branch merge utility for workflow pipelines. It accepts two
input CSV files, loads them as pandas DataFrames, merges them according to the selected
mode, and returns the merged result as a single output CSV.

## Supported merge modes

- `concat_columns`: concatenates both inputs column-wise after resetting their indices.
- `concat_rows`: concatenates both inputs row-wise and reindexes the result.
- `merge_on_key`: performs a pandas merge using a shared key column and a configurable join strategy.

## Inputs

- `left`: left input CSV, loaded as a pandas DataFrame.
- `right`: right input CSV, loaded as a pandas DataFrame.

## Hyperparameters

- `mode`: merge mode to use. One of `concat_columns`, `concat_rows`, or `merge_on_key`.
- `key`: optional merge key column. Required when `mode=merge_on_key`.
- `how`: join strategy for `merge_on_key`. One of `inner`, `left`, `right`, or `outer`.

## Output

- `output`: merged pandas DataFrame written as CSV.

## Behavior

The app validates that both inputs are present and are pandas DataFrames.
Then it applies the selected merge strategy:

- For `concat_rows`, it uses `pd.concat(..., axis=0, ignore_index=True)`.
- For `concat_columns`, it resets both indices and concatenates with `axis=1`.
- For `merge_on_key`, it validates the merge key and applies `pd.merge(..., on=key, how=how)`.

## Example

### Column-wise concatenation

- `mode=concat_columns`
- combines both tables side by side

### Row-wise concatenation

- `mode=concat_rows`
- stacks both tables vertically

### Key-based merge

- `mode=merge_on_key`
- `key=id`
- `how=inner`
- joins both tables using the shared `id` column

## Column and row alignment

Column concatenation aligns row positions after resetting indices and adds `_left`
and `_right` suffixes to all column names. Unequal input lengths are padded with
missing values. Row concatenation preserves the union of columns and resets the
output index. Key-based joins use pandas merge semantics.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Set APP_ID and platform URLs in .env before connecting.
python main.py
```

The Docker base image provides the FL-Net API and its pandas dependencies.
`requirements.txt` contains only additional runtime dependencies;
`requirements-dev.txt` includes the API for local development.

The example files are Iris flower tables. Regenerate the two input tables with
`python generate_example_data.py` from the repository root.

Build with `docker build -t tool-branch-merge-aggregator .`.
