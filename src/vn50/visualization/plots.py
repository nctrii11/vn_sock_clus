"""Visualization utilities for VN50 clustering and portfolio analysis."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


def plot_price_evolution(prices: pd.DataFrame, title: str = "Biến động Giá Cổ phiếu VN30") -> None:
    """Plot normalized price evolution for all stocks."""
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Normalize prices to start at 100
    normalized_prices = prices.div(prices.iloc[0]) * 100
    
    for col in normalized_prices.columns:
        ax.plot(normalized_prices.index, normalized_prices[col], 
                label=col.replace('.VN', ''), linewidth=1.5, alpha=0.8)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Ngày', fontsize=12)
    ax.set_ylabel('Giá Chuẩn hóa (Cơ sở = 100)', fontsize=12)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(corr: pd.DataFrame, title: str = "Ma trận Tương quan Cổ phiếu") -> None:
    """Plot correlation heatmap with clustering."""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Plot heatmap
    sns.heatmap(corr, mask=mask, annot=True, cmap='RdBu_r', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                fmt='.2f', ax=ax)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Clean up tick labels
    tick_labels = [label.replace('.VN', '') for label in corr.columns]
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')
    ax.set_yticklabels(tick_labels, rotation=0)
    
    plt.tight_layout()
    return fig


def plot_cluster_dendrogram(linkage_matrix: np.ndarray, labels: list, 
                          title: str = "Biểu đồ Phân cụm Phân cấp") -> None:
    """Plot dendrogram for hierarchical clustering."""
    from scipy.cluster.hierarchy import dendrogram
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    dendrogram(linkage_matrix, labels=labels, ax=ax, 
               leaf_rotation=90, leaf_font_size=10)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Cổ phiếu', fontsize=12)
    ax.set_ylabel('Khoảng cách', fontsize=12)
    
    plt.tight_layout()
    return fig


def plot_portfolio_weights(weights: pd.Series, title: str = "Tỷ trọng Danh mục Đầu tư") -> None:
    """Plot portfolio weights as horizontal bar chart."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Filter out zero weights for cleaner visualization
    non_zero_weights = weights[weights > 0.001]
    
    # Create horizontal bar chart
    bars = ax.barh(range(len(non_zero_weights)), non_zero_weights.values)
    
    # Color bars based on weight magnitude
    colors = plt.cm.viridis(non_zero_weights.values / non_zero_weights.max())
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    # Customize plot
    ax.set_yticks(range(len(non_zero_weights)))
    ax.set_yticklabels([label.replace('.VN', '') for label in non_zero_weights.index])
    ax.set_xlabel('Tỷ trọng Danh mục', fontsize=12)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Add value labels on bars
    for i, (idx, weight) in enumerate(non_zero_weights.items()):
        ax.text(weight + 0.005, i, f'{weight:.1%}', 
                va='center', fontweight='bold')
    
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    return fig


def plot_equity_curve(equity: pd.Series, benchmark: Optional[pd.Series] = None,
                     title: str = "Đường cong Vốn Danh mục") -> None:
    """Plot equity curve with optional benchmark."""
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot portfolio equity curve
    ax.plot(equity.index, equity.values, linewidth=2.5, 
            label='Danh mục', color='#2E86AB')
    
    # Plot benchmark if provided
    if benchmark is not None:
        ax.plot(benchmark.index, benchmark.values, linewidth=2, 
                label='Chỉ số VN-Index', color='#A23B72', alpha=0.8)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Ngày', fontsize=12)
    ax.set_ylabel('Lợi nhuận Tích lũy', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Format y-axis as percentage
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    
    plt.tight_layout()
    return fig


def plot_rolling_metrics(returns: pd.Series, window: int = 252,
                        title: str = "Chỉ số Hiệu suất Trượt") -> None:
    """Plot rolling Sharpe ratio and volatility."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)
    
    # Rolling Sharpe ratio
    rolling_sharpe = returns.rolling(window).mean() / returns.rolling(window).std() * np.sqrt(252)
    ax1.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=2, color='#F18F01')
    ax1.set_title(f'Chỉ số Sharpe Trượt (cửa sổ {window} ngày)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Chỉ số Sharpe', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Sharpe = 1')
    ax1.legend()
    
    # Rolling volatility
    rolling_vol = returns.rolling(window).std() * np.sqrt(252)
    ax2.plot(rolling_vol.index, rolling_vol.values, linewidth=2, color='#C73E1D')
    ax2.set_title(f'Độ biến động Trượt (cửa sổ {window} ngày)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Ngày', fontsize=12)
    ax2.set_ylabel('Độ biến động Hàng năm', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    return fig


def plot_drawdown(equity: pd.Series, title: str = "Phân tích Sụt giảm Danh mục") -> None:
    """Plot drawdown analysis."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)
    
    # Equity curve
    ax1.plot(equity.index, equity.values, linewidth=2, color='#2E86AB')
    ax1.set_title('Đường cong Vốn Danh mục', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Lợi nhuận Tích lũy', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    
    # Drawdown
    rolling_max = equity.expanding().max()
    drawdown = (equity - rolling_max) / rolling_max
    
    ax2.fill_between(drawdown.index, drawdown.values, 0, 
                     color='red', alpha=0.3, label='Sụt giảm')
    ax2.plot(drawdown.index, drawdown.values, color='red', linewidth=1)
    ax2.set_title('Sụt giảm Danh mục', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Ngày', fontsize=12)
    ax2.set_ylabel('Sụt giảm', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    return fig


def plot_performance_summary(metrics: dict, title: str = "Tóm tắt Hiệu suất") -> None:
    """Plot performance metrics as a summary dashboard."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Key metrics
    key_metrics = ['total_return', 'annualized_return', 'volatility', 'sharpe_ratio']
    values = [metrics.get(m, 0) for m in key_metrics]
    labels = ['Lợi nhuận Tổng', 'Lợi nhuận Hàng năm', 'Độ biến động', 'Chỉ số Sharpe']
    
    bars = ax1.bar(labels, values, color=['#2E86AB', '#F18F01', '#C73E1D', '#A23B72'])
    ax1.set_title('Chỉ số Hiệu suất Chính', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Risk metrics
    risk_metrics = ['max_drawdown', 'sortino_ratio', 'calmar_ratio']
    risk_values = [abs(metrics.get(m, 0)) for m in risk_metrics]  # abs for max_drawdown
    risk_labels = ['Sụt giảm Tối đa', 'Chỉ số Sortino', 'Chỉ số Calmar']
    
    bars2 = ax2.bar(risk_labels, risk_values, color=['#E63946', '#F77F00', '#FCBF49'])
    ax2.set_title('Chỉ số Rủi ro', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    for bar, value in zip(bars2, risk_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Hit ratio pie chart
    hit_ratio = metrics.get('hit_ratio', 0)
    ax3.pie([hit_ratio, 1-hit_ratio], labels=['Ngày Lãi', 'Ngày Lỗ'], 
            colors=['#2E86AB', '#E63946'], autopct='%1.1f%%', startangle=90)
    ax3.set_title('Tỷ lệ Lãi', fontsize=14, fontweight='bold')
    
    # Performance score (composite metric)
    score_components = ['sharpe_ratio', 'sortino_ratio', 'calmar_ratio']
    scores = [metrics.get(m, 0) for m in score_components]
    ax4.bar(['Sharpe', 'Sortino', 'Calmar'], scores, 
            color=['#2E86AB', '#F18F01', '#C73E1D'])
    ax4.set_title('Điểm Hiệu suất', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Điểm')
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    return fig


def save_figure(fig, filename: str, output_dir: str = "reports/figures") -> None:
    """Save figure to file with high quality."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / f"{filename}.png"
    fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"Figure saved: {filepath}")


def create_all_visualizations(data_dir: str = "data/processed", 
                             output_dir: str = "reports/figures") -> None:
    """Create all visualizations from processed data."""
    data_path = Path(data_dir)
    
    print("Creating visualizations...")
    
    # Load data
    prices = pd.read_parquet(data_path / "prices.parquet")
    returns = pd.read_parquet(data_path / "returns.parquet")
    corr = pd.read_parquet(data_path / "correlation.parquet")
    
    # Load results if available
    try:
        equity_curve = pd.read_csv("reports/artifacts/equity_curve.csv", index_col=0)
        metrics = pd.read_csv("reports/artifacts/metrics.csv", index_col=0).iloc[0].to_dict()
        weights = pd.read_csv("reports/artifacts/initial_weights.csv", index_col=0).iloc[:, 0]
    except FileNotFoundError:
        print("Results not found. Run the pipeline first.")
        return
    
    # Create visualizations
    print("1. Price evolution...")
    fig1 = plot_price_evolution(prices)
    save_figure(fig1, "price_evolution")
    
    print("2. Correlation heatmap...")
    fig2 = plot_correlation_heatmap(corr)
    save_figure(fig2, "correlation_heatmap")
    
    print("3. Portfolio weights...")
    fig3 = plot_portfolio_weights(weights)
    save_figure(fig3, "portfolio_weights")
    
    print("4. Equity curve...")
    fig4 = plot_equity_curve(equity_curve['equity'])
    save_figure(fig4, "equity_curve")
    
    print("5. Rolling metrics...")
    fig5 = plot_rolling_metrics(equity_curve['returns'])
    save_figure(fig5, "rolling_metrics")
    
    print("6. Drawdown analysis...")
    fig6 = plot_drawdown(equity_curve['equity'])
    save_figure(fig6, "drawdown")
    
    print("7. Performance summary...")
    fig7 = plot_performance_summary(metrics)
    save_figure(fig7, "performance_summary")
    
    print(f"\nAll visualizations saved to: {output_dir}")
    print("Visualization complete!")


if __name__ == "__main__":
    create_all_visualizations()
