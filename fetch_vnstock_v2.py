"""
Fetch VN30 data using vnstock 0.2.9
Saves data to data/raw/prices_vnstock_v2.csv and prices_vnstock_v2.parquet
"""

import pandas as pd
import sys
import io
import time

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Import vnstock
try:
    from vnstock import stock_historical_data

    print("Imported vnstock successfully!")
except ImportError as e:
    print(f"Error importing vnstock: {e}")
    sys.exit(1)

# VN30 stock symbols
VN30_SYMBOLS = [
    "ACB",
    "BCM",
    "BID",
    "BVH",
    "CTG",
    "FPT",
    "GAS",
    "GVR",
    "HDB",
    "HPG",
    "MBB",
    "MSN",
    "MWG",
    "PLX",
    "POW",
    "SAB",
    "SHB",
    "SSB",
    "SSI",
    "STB",
    "TCB",
    "TPB",
    "VCB",
    "VHM",
    "VIB",
    "VIC",
    "VJC",
    "VNM",
    "VPB",
    "VRE",
]

# Date range
START_DATE = "2020-10-11"  # 11/10/2020
END_DATE = "2025-10-31"

print("=" * 70)
print("TAI DU LIEU VN30 BANG THU VIEN VNSTOCK (v0.2.9)")
print("=" * 70)
print(f"\nThoi gian: {START_DATE} -> {END_DATE}")
print(f"So ma co phieu: {len(VN30_SYMBOLS)}")
print("\nBat dau tai du lieu...\n")

# Fetch data for each symbol
all_prices = {}
success_count = 0
failed_symbols = []

for i, symbol in enumerate(VN30_SYMBOLS, 1):
    try:
        print(f"[{i:2d}/{len(VN30_SYMBOLS)}] Dang tai {symbol}...", end=" ")

        # Get historical data using vnstock
        df = stock_historical_data(
            symbol=symbol, start_date=START_DATE, end_date=END_DATE, resolution="1D", type="stock"
        )

        if df is not None and not df.empty:
            # Check for close column
            if "close" in df.columns:
                # Set index to time/date column
                if "time" in df.columns:
                    df["time"] = pd.to_datetime(df["time"])
                    df = df.set_index("time")
                elif "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"])
                    df = df.set_index("date")

                all_prices[symbol] = df["close"]
                success_count += 1
                print(f"OK ({len(df)} ngay)")
            else:
                print("FAILED (khong co cot 'close')")
                failed_symbols.append(symbol)
        else:
            print("FAILED (khong co du lieu)")
            failed_symbols.append(symbol)

    except Exception as e:
        error_msg = str(e)[:50]
        print(f"ERROR: {error_msg}")
        failed_symbols.append(symbol)

    # Sleep to avoid rate limiting
    time.sleep(0.3)

print("\n" + "=" * 70)
print("KET QUA TAI DU LIEU:")
print(f"  - Thanh cong: {success_count}/{len(VN30_SYMBOLS)} ma")
if failed_symbols:
    print(f"  - That bai: {len(failed_symbols)} ma")
    print(f"    {', '.join(failed_symbols)}")

if all_prices:
    # Create DataFrame - handle different lengths by aligning indices
    print("\n  Dang xu ly du lieu...")

    # Get union of all dates
    all_dates = pd.DatetimeIndex([])
    for symbol, series in all_prices.items():
        # Remove duplicates from each series first
        series = series[~series.index.duplicated(keep="first")]
        all_prices[symbol] = series
        all_dates = all_dates.union(series.index)

    all_dates = all_dates.sort_values()

    # Create DataFrame with aligned dates
    prices_df = pd.DataFrame(index=all_dates)
    for symbol, series in all_prices.items():
        prices_df[symbol] = series

    # Sort by date
    prices_df = prices_df.sort_index()

    # Fill forward missing values
    prices_df = prices_df.ffill()

    print(f"\n  - Kich thuoc du lieu: {prices_df.shape}")
    print(f"  - Thoi gian: {prices_df.index.min().date()} -> {prices_df.index.max().date()}")

    # Save to CSV
    csv_path = "data/raw/prices_vnstock.csv"
    prices_df.to_csv(csv_path)
    print(f"\n  ✓ Da luu CSV: {csv_path}")

    # Save to Parquet
    parquet_path = "data/raw/prices_vnstock.parquet"
    prices_df.to_parquet(parquet_path)
    print(f"  ✓ Da luu Parquet: {parquet_path}")

    # Show file sizes
    import os

    csv_size = os.path.getsize(csv_path) / 1024
    parquet_size = os.path.getsize(parquet_path) / 1024
    print(f"\n  - Kich thuoc CSV: {csv_size:.2f} KB")
    print(f"  - Kich thuoc Parquet: {parquet_size:.2f} KB")

    # Show preview
    print(f"\n  XEM TRUOC DU LIEU (5 dong dau):")
    print(prices_df.head())

    # Create metadata
    metadata = f"""# DU LIEU VN30 TU VNSTOCK

## Thong tin
- Nguon du lieu: vnstock (v0.2.9)
- Thoi gian: {prices_df.index.min().date()} -> {prices_df.index.max().date()}
- So ma co phieu: {len(prices_df.columns)}
- So ngay giao dich: {len(prices_df)}
- Thanh cong: {success_count}/{len(VN30_SYMBOLS)} ma

## Danh sach ma co phieu VN30:
{', '.join(sorted(prices_df.columns))}

## Ma that bai (neu co):
{', '.join(failed_symbols) if failed_symbols else 'Khong co'}
"""

    with open("data/raw/prices_vnstock_README.txt", "w", encoding="utf-8") as f:
        f.write(metadata)
    print(f"  ✓ Da luu README: data/raw/prices_vnstock_README.txt")

else:
    print("\nKHONG CO DU LIEU NAO DUOC TAI!")

print("\n" + "=" * 70)
print("HOAN THANH!")
print("=" * 70)
