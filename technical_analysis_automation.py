#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Technical Analysis Automation Module
Auto-fetches RSI, MACD, SMA for watchlist assets from Twelve Data
"""

import sys
import requests
import json
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

TWELVE_DATA_KEY = "07f9ead31a5c426ea238e71895beeaa1"
WATCHLIST = ["BTC/USD", "ETH/USD", "MSTR", "HIMS"]

def fetch_indicator(symbol, indicator, interval="1day"):
    """Fetch a technical indicator from Twelve Data"""
    try:
        url = f"https://api.twelvedata.com/{indicator}"
        params = {
            "symbol": symbol,
            "interval": interval,
            "apikey": TWELVE_DATA_KEY,
            "outputsize": 1
        }
        if indicator == "rsi":
            params["time_period"] = 14
        
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        
        if "values" in data and len(data["values"]) > 0:
            latest = data["values"][0]
            return {
                "symbol": symbol,
                "indicator": indicator.upper(),
                "value": latest.get("rsi") or latest.get("macd") or latest.get("ema") or latest.get("value"),
                "datetime": latest.get("datetime"),
                "status": "ok"
            }
        else:
            return {"symbol": symbol, "indicator": indicator, "value": None, "status": "no_data", "error": data.get("message", "Unknown")}
    except Exception as e:
        return {"symbol": symbol, "indicator": indicator, "value": None, "status": "error", "error": str(e)}

def fetch_price(symbol):
    """Fetch current price"""
    try:
        url = f"https://api.twelvedata.com/quote"
        params = {"symbol": symbol, "apikey": TWELVE_DATA_KEY}
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        return {
            "price": float(data.get("close", 0)),
            "change": float(data.get("percent_change", 0)),
            "volume": data.get("volume", "N/A")
        }
    except:
        return {"price": None, "change": None, "volume": None}

def interpret_rsi(value):
    """Interpret RSI value"""
    if value is None:
        return "N/A"
    val = float(value)
    if val >= 70:
        return f"OVERBOUGHT ({val:.1f}) - Potential sell"
    elif val <= 30:
        return f"OVERSOLD ({val:.1f}) - Potential buy"
    elif val > 55:
        return f"Bullish momentum ({val:.1f})"
    elif val < 45:
        return f"Bearish momentum ({val:.1f})"
    else:
        return f"Neutral ({val:.1f})"

def interpret_macd(value, signal=None):
    """Interpret MACD value"""
    if value is None:
        return "N/A"
    val = float(value)
    if signal:
        sig = float(signal)
        if val > sig:
            return f"BULLISH crossover (MACD: {val:.4f} > Signal: {sig:.4f})"
        else:
            return f"BEARISH crossover (MACD: {val:.4f} < Signal: {sig:.4f})"
    return f"MACD: {val:.4f}"

def generate_signals(results):
    """Generate trading signals from indicators"""
    signals = []
    for symbol, data in results.items():
        rsi = data.get("rsi", {}).get("value")
        macd = data.get("macd", {}).get("value")
        
        if rsi and float(rsi) <= 30:
            signals.append(f"🟢 BUY signal: {symbol} RSI oversold ({rsi})")
        elif rsi and float(rsi) >= 70:
            signals.append(f"🔴 SELL signal: {symbol} RSI overbought ({rsi})")
    
    return signals

def save_to_json(results):
    """Save results to a JSON file for dashboard integration"""
    output = {
        "generated_at": datetime.now().isoformat(),
        "results": results
    }
    Path("data").mkdir(exist_ok=True)
    filepath = Path("data") / f"technical_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, default=str)
    return filepath

def main():
    print("=" * 70)
    print("TECHNICAL ANALYSIS AUTOMATION MODULE")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} Paris Time")
    print("=" * 70)
    
    results = {}
    all_signals = []
    
    for symbol in WATCHLIST:
        print(f"\n📈 {symbol}:")
        print("-" * 50)
        
        # Price
        price_data = fetch_price(symbol)
        if price_data["price"]:
            print(f"  Price:     ${price_data['price']:,.2f} ({price_data['change']:+.2f}%)")
        
        results[symbol] = {}
        
        # RSI
        rsi_data = fetch_indicator(symbol, "rsi")
        results[symbol]["rsi"] = rsi_data
        if rsi_data["value"]:
            interpretation = interpret_rsi(rsi_data["value"])
            print(f"  RSI(14):   {interpretation}")
        else:
            print(f"  RSI(14):   [Unavailable - {rsi_data.get('error', 'Unknown')[:50]}]")
        
        # MACD
        macd_data = fetch_indicator(symbol, "macd")
        results[symbol]["macd"] = macd_data
        if macd_data["value"]:
            interpretation = interpret_macd(macd_data["value"])
            print(f"  MACD:      {interpretation}")
        else:
            print(f"  MACD:      [Unavailable - {macd_data.get('error', 'Unknown')[:50]}]")
        
        # SMA 20
        sma_data = fetch_indicator(symbol, "sma")
        results[symbol]["sma20"] = sma_data
        if sma_data["value"]:
            print(f"  SMA(20):   {float(sma_data['value']):,.2f}")
        else:
            print(f"  SMA(20):   [Unavailable]")
    
    # Generate signals
    print("\n🚦 TRADING SIGNALS:")
    print("-" * 50)
    signals = generate_signals(results)
    if signals:
        for signal in signals:
            print(f"  {signal}")
    else:
        print("  No strong signals detected.")
    
    # Save results
    try:
        saved_path = save_to_json(results)
        print(f"\n💾 Data saved to: {saved_path}")
    except Exception as e:
        print(f"\n⚠️ Could not save JSON: {e}")
    
    print("\n" + "=" * 70)
    print("Next: Integrate with Mission Control Dashboard")
    print("=" * 70)

if __name__ == '__main__':
    main()
