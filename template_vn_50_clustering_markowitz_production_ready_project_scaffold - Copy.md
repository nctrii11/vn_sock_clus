# VN50 Clustering + Markowitz — End‑to‑End Project Scaffold

A production‑oriented template for a quant research repo using **hierarchical clustering** for asset grouping and **Markowitz mean–variance** for portfolio optimization. Designed to be reproducible, testable, and configurable via **Hydra/OmegaConf**.

---

## 0) Project Goals
- Fetch VN30/VN50 equities data and metadata
- Engineer features (returns, risk metrics, correlation/covariance, distance matrices)
- Cluster assets (HClust/HRP‑ready trees)
- Optimize portfolios (long‑only / with constraints)
- Backtest & report with deterministic configs and experiment tracking

---

## 1) Repository Layout
```
vn50-cluster-markowitz/
├─ README.md
├─ pyproject.toml               # build + dependencies (primary)
├─ requirements.txt             # optional export for pip users
├─ uv.lock                      # lockfile for reproducible installs
├─ .gitignore
├─ .pre-commit-config.yaml
├─ .env.example                 # API keys/toggles (never commit real .env)
├─ Makefile
├─ configs/
│  ├─ base.yaml                 # global defaults
│  ├─ data.yaml                 # data sources and instruments
│  ├─ features.yaml             # return windows, vol, etc.
│  ├─ cluster_hclust.yaml       # linkage/affinity, cut rules
│  ├─ optimizer_markowitz.yaml  # bounds, objective, regularizers
│  └─ experiment_hclust.yaml    # overrides to run a named experiment
├─ data/
│  ├─ raw/.gitkeep
│  ├─ interim/.gitkeep
│  ├─ processed/.gitkeep
│  └─ cache/.gitkeep
├─ notebooks/
│  ├─ 00_exploration.ipynb
│  └─ 10_report_example.ipynb
├─ reports/
│  ├─ figures/.gitkeep
│  └─ artifacts/.gitkeep
├─ src/
│  └─ vn50/
│     ├─ __init__.py
│     ├─ utils/
│     │  ├─ io.py               # read/save parquet/csv, cache helpers
│     │  ├─ logging.py          # structured logging config
│     │  └─ timer.py
│     ├─ data/
│     │  ├─ fetch.py            # vnstock/yfinance wrappers
│     │  └─ preprocess.py       # cleaning, adjust, align calendar
│     ├─ features/
│     │  ├─ returns.py          # log/arith returns
│     │  ├─ risk.py             # vol, drawdown, VaR
│     │  └─ corr.py             # corr/cov, distance matrices
│     ├─ clustering/
│     │  ├─ hclust.py           # linkage, dendrogram, cut/flat clusters
│     │  └─ utils.py
│     ├─ optimize/
│     │  ├─ markowitz.py        # MVO (cvxpy/pyportfolioopt)
│     │  └─ constraints.py      # long-only, sector caps, turnover
│     ├─ backtest/
│     │  ├─ engine.py           # walk-forward, rebalancing
│     │  └─ metrics.py          # Sharpe, Calmar, hit ratio, etc.
│     └─ cli/
│        ├─ fetch_data.py       # CLI entrypoints (Hydra configs)
│        ├─ build_features.py
│        ├─ run_clustering.py
│        ├─ optimize_portfolio.py
│        └─ backtest.py
├─ tests/
│  ├─ test_returns.py
│  ├─ test_corr.py
│  └─ test_markowitz.py
└─ .github/workflows/
   └─ ci.yaml                   # lint + tests on push/PR
```

---

## 2) Minimal `README.md`
```md
# VN50 Clustering + Markowitz
End‑to‑end pipeline: data → features → clusters → optimization → backtest.

## Quickstart
```bash
# 1) setup
pipx install uv || python -m pip install -U pip
uv venv && source .venv/bin/activate
uv sync
pre-commit install

# 2) run a full experiment
uv run python -m src.vn50.cli.fetch_data           +experiment=experiment_hclust
uv run python -m src.vn50.cli.build_features       +experiment=experiment_hclust
uv run python -m src.vn50.cli.run_clustering       +experiment=experiment_hclust
uv run python -m src.vn50.cli.optimize_portfolio   +experiment=experiment_hclust
uv run python -m src.vn50.cli.backtest             +experiment=experiment_hclust
```
```

---

## 3) Example Configs (Hydra/OmegaConf)

### `configs/base.yaml`
```yaml
project: vn50-cluster-markowitz
seed: 42
paths:
  data: data
  raw: ${paths.data}/raw
  interim: ${paths.data}/interim
  processed: ${paths.data}/processed
  cache: ${paths.data}/cache
  reports: reports
calendar:
  start: "2019-01-01"
  end:   "${now:YYYY-MM-DD}"
frequency: D   # D/W/M
logging:
  level: INFO
  rich: true
```

### `configs/data.yaml`
```yaml
source: vnstock   # or: yfinance
universe: VN50    # or: VN30, custom list below
symbols:
  custom: []      # e.g., ["VIC","VNM","VCB",...]
price:
  fields: [open, high, low, close, volume]
  adjust: true
cache: true
```

### `configs/features.yaml`
```yaml
returns:
  kind: log   # log|arith
  window: 1
risk:
  vol_window: 20
  ann_factor: 252
corr:
  method: pearson   # pearson|spearman
  window: 60
  shrinkage: lw     # none|lw|oas
```

### `configs/cluster_hclust.yaml`
```yaml
affinity: distance   # uses 1 - corr
linkage: ward        # ward|average|complete
n_clusters: auto     # auto|int
cut:
  max_depth: null
  max_distance: null
labels: sector       # optional metadata label to summarize clusters
```

### `configs/optimizer_markowitz.yaml`
```yaml
engine: cvxpy        # or: pypfopt
objective: max_sharpe   # max_sharpe|min_vol|custom
constraints:
  long_only: true
  weight_bounds: [0.0, 0.15]
  turnover_limit: 0.4
  budget: 1.0
risk_model:
  cov: shrinkage      # sample|shrinkage
  risk_free_rate: 0.02
rebalance:
  freq: M
  costs_bps: 10
```

### `configs/experiment_hclust.yaml`
```yaml
# Compose: `uv run python -m src.vn50.cli.optimize_portfolio   +experiment=experiment_hclust`
defaults:
  - base
  - data
  - features
  - cluster_hclust
  - optimizer_markowitz
  - _self_

project: vn50-hclust-markowitz-demo
calendar:
  start: "2020-01-01"
  end:   "${now:YYYY-MM-DD}"
frequency: D
```

---

## 4) Key Code Skeletons

### `src/vn50/utils/logging.py`
```python
import logging
from contextlib import contextmanager

FORMAT = "[%(levelname)s] %(asctime)s %(name)s: %(message)s"

def setup_logging(level: str = "INFO"):
    logging.basicConfig(level=getattr(logging, level), format=FORMAT)
    return logging.getLogger("vn50")

@contextmanager
def task(msg: str, logger=None):
    logger = logger or logging.getLogger("vn50")
    logger.info(msg + " ...")
    yield
    logger.info(msg + " ✓")
```

### `src/vn50/data/fetch.py`
```python
from __future__ import annotations
import pandas as pd
from pathlib import Path
from .preprocess import align_calendar

# Minimal stub — replace with vnstock/yfinance wrappers

def fetch_prices(symbols: list[str], start: str, end: str) -> pd.DataFrame:
    # columns: (symbol, date, open, high, low, close, volume)
    raise NotImplementedError("Implement vnstock/yfinance fetch here")

def load_or_fetch(cache_dir: Path, *args, **kwargs) -> pd.DataFrame:
    cache_file = cache_dir / "prices.parquet"
    if cache_file.exists():
        return pd.read_parquet(cache_file)
    df = fetch_prices(*args, **kwargs)
    df = align_calendar(df)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache_file)
    return df
```

### `src/vn50/features/corr.py`
```python
import numpy as np
import pandas as pd

def rolling_corr(returns: pd.DataFrame, window: int, method: str = "pearson") -> pd.DataFrame:
    return returns.rolling(window).corr(method=method)

def distance_from_corr(corr: pd.DataFrame) -> pd.DataFrame:
    # Mantegna distance
    return np.sqrt(0.5 * (1 - corr))
```

### `src/vn50/clustering/hclust.py`
```python
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster

def hclust_from_distance(D: pd.DataFrame, method: str = "ward", n_clusters: int | str = "auto"):
    # Convert distance matrix to condensed form
    tri = D.values[np.triu_indices_from(D, k=1)]
    Z = linkage(tri, method=method)
    if n_clusters == "auto":
        # naive heuristic — replace with better criterion (e.g., inconsistency, gap stat)
        n_clusters = 5
    labels = fcluster(Z, n_clusters, criterion="maxclust")
    return Z, labels
```

### `src/vn50/optimize/markowitz.py`
```python
import numpy as np
import pandas as pd
import cvxpy as cp

def mean_variance_weights(mu: pd.Series, Sigma: pd.DataFrame, lb=0.0, ub=0.15, rf=0.0, objective="max_sharpe"):
    n = len(mu)
    w = cp.Variable(n)
    constraints = [cp.sum(w) == 1, w >= lb, w <= ub]
    port_var = cp.quad_form(w, Sigma.values)
    port_mu = mu.values @ w
    if objective == "min_vol":
        prob = cp.Problem(cp.Minimize(cp.sqrt(port_var)), constraints)
    else:  # max_sharpe
        # maximize (mu-rf)/sigma  ≈ maximize mu - k*sigma (k chosen via bisection/line search)
        k = 1.0
        prob = cp.Problem(cp.Maximize(port_mu - k * cp.sqrt(port_var)), constraints)
    prob.solve(solver=cp.ECOS)
    return pd.Series(w.value, index=mu.index)
```

### `src/vn50/backtest/engine.py`
```python
import pandas as pd

def walk_forward(prices: pd.DataFrame, rebalance, optimize, freq="M"):
    rets = prices.pct_change().dropna()
    weights_hist = {}
    equity = 1.0
    for t, df_month in rets.groupby(pd.Grouper(freq=freq)):
        mu = df_month.mean() * 252
        Sigma = df_month.cov() * 252
        w = optimize(mu, Sigma)
        weights_hist[t] = w
        equity *= (1 + (df_month @ w).sum())
    return pd.Series(weights_hist), equity
```

### CLI example `src/vn50/cli/optimize_portfolio.py`
```python
import hydra
from omegaconf import DictConfig
from pathlib import Path
from vn50.utils.logging import setup_logging, task
from vn50.data.fetch import load_or_fetch
from vn50.features.returns import make_returns
from vn50.features.corr import rolling_corr, distance_from_corr
from vn50.clustering.hclust import hclust_from_distance
from vn50.optimize.markowitz import mean_variance_weights
from vn50.backtest.engine import walk_forward

@hydra.main(version_base=None, config_path="../../../configs", config_name="experiment_hclust")
def main(cfg: DictConfig):
    log = setup_logging(cfg.logging.level)
    with task("Load or fetch prices", log):
        prices = load_or_fetch(Path(cfg.paths.cache), cfg.data.symbols.custom or [], cfg.calendar.start, cfg.calendar.end)
    # TODO: implement make_returns
    # TODO: compute corr/distance, cluster, etc.
    # TODO: plug into backtest.walk_forward with optimizer

if __name__ == "__main__":
    main()
```

---

## 5) Tooling

### `requirements.txt` (optional)
Use only if you must share with plain `pip` users. Prefer `pyproject.toml` + `uv.lock`.
```
pandas
numpy
scipy
cvxpy
hydra-core
omegaconf
matplotlib
seaborn
pyyaml
rich
pytest
pyinstrument
# optional
vnstock
yfinance
pyportfolioopt
```
pandas
numpy
scipy
cvxpy
hydra-core
omegaconf
matplotlib
seaborn
pyyaml
rich
pytest
pyinstrument
# optional
vnstock
yfinance
pyportfolioopt
```

### `pyproject.toml` (primary for uv)
```toml
[project]
name = "vn50-cluster-markowitz"
version = "0.1.0"
dependencies = [
  "pandas","numpy","scipy","cvxpy","hydra-core","omegaconf",
  "matplotlib","pyyaml","rich","pytest","vnstock","yfinance"
]
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-q"
```

> Use `uv sync` to install, `uv add PKG` to modify, and `uv lock --python 3.11` to freeze.toml
[project]
name = "vn50-cluster-markowitz"
version = "0.1.0"
dependencies = [
  "pandas","numpy","scipy","cvxpy","hydra-core","omegaconf",
  "matplotlib","pyyaml","rich","pytest","vnstock","yfinance"
]
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-q"
```

### `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks: [{id: black}]
  - repo: https://github.com/pycqa/ruff-pre-commit
    rev: v0.6.9
    hooks: [{id: ruff}]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

### `.github/workflows/ci.yaml`
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - name: Install uv
        run: pipx install uv
      - name: Sync deps (frozen if lock exists)
        run: |
          if [ -f uv.lock ]; then uv sync --frozen; else uv sync; fi
      - name: Lint
        run: |
          uvx ruff check .
          uvx black --check .
      - name: Tests
        run: uv run pytest -q
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install -r requirements.txt
      - run: pytest -q
```

### `Makefile`
```make
.PHONY: setup lint test data features cluster opt backtest all

PY := 3.11

setup:
	uv venv --python $(PY)
	uv sync
	uvx pre-commit install

lint:
	uvx ruff check .
	uvx black --check .

test:
	uv run pytest -q

data:
	uv run uv run python -m src.vn50.cli.fetch_data           +experiment=experiment_hclust
features:
	uv run uv run python -m src.vn50.cli.build_features       +experiment=experiment_hclust
cluster:
	uv run uv run python -m src.vn50.cli.run_clustering       +experiment=experiment_hclust
opt:
	uv run uv run python -m src.vn50.cli.optimize_portfolio   +experiment=experiment_hclust
backtest:
	uv run uv run python -m src.vn50.cli.backtest             +experiment=experiment_hclust

all: data features cluster opt backtest
```make
.PHONY: setup lint test data features cluster opt backtest all
setup:
	python -m pip install -U pip
	pip install -r requirements.txt
	pre-commit install

lint:
	ruff check .
	black --check .
\pytest:
	pytest -q

data:
	uv run python -m src.vn50.cli.fetch_data           +experiment=experiment_hclust
features:
	uv run python -m src.vn50.cli.build_features       +experiment=experiment_hclust
cluster:
	uv run python -m src.vn50.cli.run_clustering       +experiment=experiment_hclust
opt:
	uv run python -m src.vn50.cli.optimize_portfolio   +experiment=experiment_hclust
backtest:
	uv run python -m src.vn50.cli.backtest             +experiment=experiment_hclust
all: data features cluster opt backtest
```

---

## 6) How to Use
1. **Clone + init:** `git init`, add remote, commit scaffold.
2. **Create venv + deps:** `pipx install uv && uv venv --python 3.11 && source .venv/bin/activate && uv sync`.
3. **Install hooks:** `uvx pre-commit install`.
4. **Edit `configs/*.yaml`** để đặt universe, ngày, tham số chiến lược.
5. **Implement data fetch** (vnstock/yfinance) ở `src/vn50/data/fetch.py`.
6. **Chạy pipeline** bằng `make all` (hoặc từng bước với `uv run ...`).
7. **Tái lập môi trường trên máy khác:** `uv sync --frozen` (dựa `uv.lock`).

---

## 7) Testing Stubs
```python
# tests/test_returns.py
import pandas as pd
from src.vn50.features.returns import make_returns

def test_make_returns_shapes():
    df = pd.DataFrame({"AAA": [1,2,3,4], "BBB": [2,3,5,7]})
    out = make_returns(df)
    assert out.shape[1] == 2
```

---

## 8) Next Improvements
- Add **HRP/Hierarchical Risk Parity** (cluster‑aware weighting)
- Add **mlflow** or **Weights & Biases** for experiment tracking
- Add **DVC** for immutable data versioning
- Add **Dockerfile** & **devcontainer** for reproducible environment

> This document is meant as a drop‑in blueprint you can adapt to your own VN30/VN50 research.

