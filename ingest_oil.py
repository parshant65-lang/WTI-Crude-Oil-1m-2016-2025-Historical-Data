#!/usr/bin/env python3
import os
import sys
import io
import re
import json
import argparse
import subprocess
import urllib.request
from pathlib import Path
import pandas as pd

def git_commit_and_push(msg: str):
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "config", "http.postBuffer", "524288000"], check=True)
    subprocess.run(["git", "add", "-A"], check=True)
    diff = subprocess.run(["git", "diff", "--staged", "--quiet"])
    if diff.returncode != 0:
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print(f"[✓] Successfully committed and pushed: {msg}")

def run(symbol: str, dataset: str, start_year: int, end_year: int):
    print(f"[*] Starting Cloud Ingestion for {symbol} ({start_year} - {end_year}) from {dataset}...")
    base_dir = Path(f"{symbol}/1m")
    list_url = f"https://huggingface.co/api/datasets/{dataset}/tree/main/1"

    req = urllib.request.Request(list_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        tree = json.loads(resp.read().decode())

    parquet_files = [f["path"] for f in tree if f["path"].endswith(".parquet")]
    
    target_files = []
    for fpath in parquet_files:
        m = re.search(r"_(\d{4})-(\d{2})-", fpath)
        if m:
            yr = int(m.group(1))
            if start_year <= yr <= end_year:
                target_files.append((yr, m.group(2), fpath))

    target_files.sort(key=lambda x: (x[0], x[1]))
    print(f"[*] Found {len(target_files)} monthly parquet files to process.")

    current_batch_year = None
    years_processed = 0

    for yr, mo, fpath in target_files:
        file_url = f"https://huggingface.co/datasets/{dataset}/resolve/main/{fpath}"
        print(f"[*] Streaming & parsing {symbol} {yr}-{mo}...")

        f_req = urllib.request.Request(file_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(f_req) as f_resp:
            df = pd.read_parquet(io.BytesIO(f_resp.read()))

        if df.empty:
            continue

        t0 = df["time"].iloc[0]
        if t0 > 1e16:
            dt = pd.to_datetime(df["time"], unit="ns", utc=True)
            ts_ms = (df["time"] // 1_000_000).astype("int64")
        elif t0 > 1e12:
            dt = pd.to_datetime(df["time"], unit="ms", utc=True)
            ts_ms = df["time"].astype("int64")
        else:
            dt = pd.to_datetime(df["time"], unit="s", utc=True)
            ts_ms = (df["time"] * 1000).astype("int64")

        df["timestamp"] = ts_ms
        df["datetime_utc"] = dt.dt.strftime("%Y-%m-%d %H:%M:%S")
        df["date"] = dt.dt.strftime("%Y-%m-%d")

        for date_str, grp in df.groupby("date"):
            y_str = date_str[0:4]
            m_str = date_str[5:7]
            out_file = base_dir / y_str / m_str / f"{symbol}_1m_{date_str}.csv"
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_cols = ["timestamp", "datetime_utc", "open", "high", "low", "close", "volume"]
            grp[out_cols].to_csv(out_file, index=False)

        if current_batch_year != yr:
            current_batch_year = yr
            years_processed += 1
            if years_processed % 3 == 0:
                git_commit_and_push(f"Batch push: {symbol} 1m data through year {yr}")

    # Final commit and push
    git_commit_and_push(f"Complete {symbol} 1m historical archive ({start_year}-{end_year})")
    print(f"[✓] Finished ingestion for {symbol} ({start_year}-{end_year})!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--end-year", type=int, required=True)
    args = parser.parse_args()
    run(args.symbol, args.dataset, args.start_year, args.end_year)
