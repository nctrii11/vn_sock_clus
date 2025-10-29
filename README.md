# VN50 Clustering + Markowitz

End-to-end pipeline for VN30/VN50 clustering-based portfolio optimization using hierarchical clustering and Markowitz mean-variance optimization.

## Project Overview

This project implements a complete quantitative research pipeline:

- **Data Fetching**: VN30/VN50 equity data via yfinance
- **Feature Engineering**: Returns, risk metrics, correlation matrices
- **Clustering**: Hierarchical clustering for asset grouping
- **Optimization**: Markowitz mean-variance portfolio optimization
- **Backtesting**: Walk-forward backtesting with performance metrics
- **Visualization**: Professional charts and dashboards

## Tech Stack

- Python 3.11
- **uv** for environment and dependency management
- Hydra/OmegaConf for configuration
- NumPy/SciPy/Pandas for data processing
- CVXPY for convex optimization
- matplotlib/seaborn for visualization
- pytest for testing

## Quickstart

### 1. Setup Environment

```bash
# Install uv (if not already installed)
pipx install uv

# Create virtual environment
make venv

# Install dependencies
make install
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
make install
```

On Linux/Mac:

```bash
source .venv/bin/activate
make install
```

### 2. Run Full Pipeline

**Option A: Complete pipeline with visualizations**

```bash
make all         # Run all steps including visualization
```

**Option B: Individual steps**

```bash
make data        # Fetch market data
make features    # Build features (returns, correlation, etc.)
make cluster     # Run hierarchical clustering
make opt         # Optimize portfolio
make backtest    # Run backtest
make visualize   # Create charts
```

**Option C: PowerShell scripts (Windows)**

```powershell
# Complete pipeline with visualizations
.\run_complete_pipeline.ps1

# View all generated charts
.\open_charts.ps1
```

### 3. Run Tests

```bash
make test
```

### 4. Lint Code

```bash
make lint
```

## Project Structure

```
vn50-cluster-markowitz/
├── configs/           # Hydra configuration files
├── data/             # Raw, interim, processed, cache
├── reports/          # Figures and artifacts
├── src/vn50/         # Source code
│   ├── utils/        # Utilities (io, logging)
│   ├── data/         # Data fetching and preprocessing
│   ├── features/     # Returns, risk, correlation
│   ├── clustering/   # Hierarchical clustering
│   ├── optimize/     # Markowitz optimization
│   ├── backtest/     # Backtesting engine and metrics
│   ├── visualization/ # Charts and dashboards
│   └── cli/          # CLI entrypoints
└── tests/            # Test suite
```

## Configuration

All parameters are managed via Hydra configs in `configs/`:

- `base.yaml`: Global defaults
- `data.yaml`: Data sources and symbols
- `features.yaml`: Feature engineering parameters
- `cluster_hclust.yaml`: Clustering configuration
- `optimizer_markowitz.yaml`: Optimization settings
- `experiment_hclust.yaml`: Complete experiment config

## Development

### Adding New Features

1. Place pure computation functions in appropriate modules (`features/`, `clustering/`, `optimize/`)
2. Add I/O logic to `utils/io.py` or CLI modules
3. Write tests in `tests/`
4. Update configs if new parameters are needed
5. Run `make test` and `make lint`

### Code Standards

- Use `uv run` for all Python commands
- All parameters from Hydra config (`cfg`)
- I/O only in `utils/io.py` or CLI modules
- Pure functions for computation
- Log via `utils.logging.task()`
- Write tests for new functions

## 📊 Visualization

The project includes comprehensive visualizations:

### Generated Charts

- **Price Evolution**: Normalized stock price movements
- **Correlation Heatmap**: Stock correlation matrix
- **Portfolio Weights**: Optimized portfolio allocation
- **Equity Curve**: Portfolio performance over time
- **Rolling Metrics**: Sharpe ratio and volatility trends
- **Drawdown Analysis**: Risk analysis and drawdown periods
- **Performance Summary**: Comprehensive performance dashboard

### Usage

```bash
# Create all visualizations
make visualize

# View charts (Windows)
.\open_charts.ps1
```

### Customization

- Modify `src/vn50/visualization/plots.py` for custom charts
- Adjust colors, sizes, and styles
- Add new visualization functions

See `VISUALIZATION_GUIDE.md` for detailed documentation.

## License

MIT
