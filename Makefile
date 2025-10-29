.PHONY: setup venv install lint test clean data features cluster opt backtest all help

PY := 3.11

help:
	@echo "Available commands:"
	@echo "  make setup       - Setup virtual environment and install dependencies"
	@echo "  make venv        - Create virtual environment only"
	@echo "  make install     - Install dependencies with uv sync"
	@echo "  make lint        - Run linting with ruff and black"
	@echo "  make test        - Run tests with pytest"
	@echo "  make data        - Run fetch_data step"
	@echo "  make features    - Run build_features step"
	@echo "  make cluster     - Run run_clustering step"
	@echo "  make opt         - Run optimize_portfolio step"
	@echo "  make backtest    - Run backtest step"
	@echo "  make visualize  - Create visualizations"
	@echo "  make all         - Run full pipeline (data → backtest → visualize)"
	@echo "  make clean        - Clean generated files"

setup: venv install

venv:
	uv venv --python $(PY)

install:
	uv sync
	uvx pre-commit install

lint:
	uvx ruff check .
	uvx black --check .

test:
	uv run pytest -q

data:
	uv run python -m src.vn50.cli.fetch_data +experiment=experiment_hclust

features:
	uv run python -m src.vn50.cli.build_features +experiment=experiment_hclust

cluster:
	uv run python -m src.vn50.cli.run_clustering +experiment=experiment_hclust

opt:
	uv run python -m src.vn50.cli.optimize_portfolio +experiment=experiment_hclust

backtest:
	uv run python -m src.vn50.cli.backtest +experiment=experiment_hclust

visualize:
	uv run python -m src.vn50.cli.create_visualizations +experiment=experiment_hclust

all: data features cluster opt backtest visualize

clean:
	rm -rf .venv
	rm -rf data/raw/* data/interim/* data/processed/* data/cache/*
	rm -rf reports/figures/* reports/artifacts/*
	rm -rf __pycache__ .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

