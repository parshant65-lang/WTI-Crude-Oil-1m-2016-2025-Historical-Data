# WTI-Crude-Oil-1m-2016-2025-Historical-Data

[![Data Status](https://img.shields.io/badge/Data-Verified-brightgreen)](#)
[![Timeframe](https://img.shields.io/badge/Timeframe-1m%20(1--Minute)-blue)](#)
[![Instrument](https://img.shields.io/badge/Instrument-USOIL%20Crude%20Oil-black)](#)
[![Coverage](https://img.shields.io/badge/Coverage-2016--2025-orange)](#)

High-resolution, institutional-grade 1-minute OHLCV (Open, High, Low, Close, Volume) historical market data archive for **WTI Crude Oil (USOIL) 1-Minute Historical Market Data Archive (2016–2025)** in US Dollars, covering the 10-year span from **2016 to 2025**.

---

## 📂 Repository Structure

All data is structured identically to institutional market data conventions by Year, Month, and Date:

```text
WTI-Crude-Oil-1m-2016-2025-Historical-Data/
├── README.md
└── USOIL/
    └── 1m/
        ├── 2016/
        │   ├── 01/
        │   │   ├── USOIL_1m_2016-01-02.csv
        │   │   └── ...
        │   └── ...
        └── 2025/
            └── ...
```

---

## 📊 CSV Schema

| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `timestamp` | `int64` | Unix Epoch timestamp in milliseconds (UTC) | `1704153600000` |
| `datetime_utc` | `string` | UTC datetime in `YYYY-MM-DD HH:MM:SS` format | `2024-01-02 00:00:00` |
| `open` | `float` | Open price (USD per Barrel) | `71.25` |
| `high` | `float` | High price in the 1-minute bar (USD per Barrel) | `71.40` |
| `low` | `float` | Low price in the 1-minute bar (USD per Barrel) | `71.18` |
| `close` | `float` | Close price (USD per Barrel) | `71.32` |
| `volume` | `int` | **Tick Volume** (Frequency of price quotes per minute) | `85` |

---

## 🔍 Understanding the "Volume" Field (Tick Volume vs. Share Volume)

If you are coming from equity stock markets (where volume reflects thousands or millions of traded shares), the volume values here may appear modest at first glance (e.g., `12`, `45`, `310`). Here is the essential structural distinction:

### 1. Decentralized (OTC) Nature of Spot Commodities
Unlike centralized equity exchanges (such as the NYSE, NASDAQ, or NSE) where every single transacted share is centrally tallied by a clearinghouse, global commodities trade across an interconnected interbank network. There is no single universal clearinghouse that records total physical barrels or dollar totals in real-time.

### 2. What is "Tick Volume"?
In spot foreign exchange and commodity markets, the industry standard metric for volume is **Tick Volume** (also called **Tick Count**):
* **It measures market activity**: Specifically, how many times the price changed (ticked or was updated) within that 60-second window.
* **Not barrel/contract count**: It does not represent physical barrels of oil, but rather the intensity of quotation activity.

### 3. How to Interpret Tick Volume Numbers

| Volume Range | Market Activity | Description |
| :--- | :--- | :--- |
| **0 – 15** | **Low / Dormant** | Quiet trading hours, Asian/Pacific late-night sessions, or market holidays. |
| **20 – 100** | **Moderate / Active** | Standard institutional liquidity during active European and US energy trading sessions. |
| **100 – 500+** | **High Volatility Burst** | Major inventory news releases (e.g., US EIA Weekly Petroleum Status Report, OPEC meetings, geopolitical updates). |

### 4. Quantitative Validity
Quantitative and financial econometric research has established that **tick volume exhibits a >90% statistical correlation with actual cash trading volume and market volatility**. A surge in tick count directly signals institutional order flow and active price discovery.

---

## 🚀 Quick Usage in Python

```python
import pandas as pd

# Load a specific day
file_path = "USOIL/1m/2016/06/USOIL_1m_2016-06-15.csv"
df = pd.read_csv(file_path, parse_dates=["datetime_utc"])

print(df.head())
print(f"Total 1m candles for the day: {len(df)}")
```

---

## 🔗 Related Archives in this Energy Series

* **WTI 2005–2015:** [WTI-Crude-Oil-1m-2005-2015-Historical-Data](https://github.com/parshant65-lang/WTI-Crude-Oil-1m-2005-2015-Historical-Data)
* **WTI 2016–2025:** [WTI-Crude-Oil-1m-2016-2025-Historical-Data](https://github.com/parshant65-lang/WTI-Crude-Oil-1m-2016-2025-Historical-Data)
* **Brent 2005–2015:** [Brent-Crude-Oil-1m-2005-2015-Historical-Data](https://github.com/parshant65-lang/Brent-Crude-Oil-1m-2005-2015-Historical-Data)
* **Brent 2016–2025:** [Brent-Crude-Oil-1m-2016-2025-Historical-Data](https://github.com/parshant65-lang/Brent-Crude-Oil-1m-2016-2025-Historical-Data)
