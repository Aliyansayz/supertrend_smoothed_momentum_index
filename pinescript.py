"""
https://chatgpt.com/share/6777011d-f520-8010-961c-5f62aecfa5f8
"""

//@version=6
indicator("Combined Supertrend and Double Smoothed Stochastic", overlay=false)

// Supertrend Settings
factor = input.float(3.0, title="Supertrend Factor")
period = input.int(10, title="Supertrend Period")

// ATR Calculation
atr = ta.atr(period)

// Basic Upper and Lower Bands
basicUpperBand = hlc3 + factor * atr
basicLowerBand = hlc3 - factor * atr

// Final Upper and Lower Bands
var float finalUpperBand = na
var float finalLowerBand = na

if (na(finalUpperBand))
    finalUpperBand := basicUpperBand
else
    finalUpperBand := basicUpperBand < finalUpperBand[1] and close[1] > finalUpperBand[1] ? basicUpperBand : finalUpperBand[1]

if (na(finalLowerBand))
    finalLowerBand := basicLowerBand
else
    finalLowerBand := basicLowerBand > finalLowerBand[1] and close[1] < finalLowerBand[1] ? basicLowerBand : finalLowerBand[1]

// Supertrend Direction
var int trend = 1
trend := close > finalLowerBand[1] ? 1 : close < finalUpperBand[1] ? -1 : nz(trend[1], 1)

// Supertrend Line
supertrendLine = trend == 1 ? finalLowerBand : finalUpperBand

// Plotting Supertrend
plot(supertrendLine, title="Supertrend", color=trend == 1 ? color.green : color.red, linewidth=2)
bgcolor(trend == 1 ? color.new(color.green, 90) : color.new(color.red, 90))

// Double Smoothed Stochastic Settings
lengthK = input.int(14, title="Stochastic K Length", group="Double Smoothed Stochastic")
smoothK = input.int(3, title="Stochastic K Smoothing", group="Double Smoothed Stochastic")
smoothD = input.int(3, title="Stochastic D Smoothing", group="Double Smoothed Stochastic")
emaSmoothingK = input.int(3, title="EMA Smoothing for %K", group="Double Smoothed Stochastic")
emaSmoothingD = input.int(3, title="EMA Smoothing for %D", group="Double Smoothed Stochastic")

// Calculate Stochastic %K
stochK = ta.sma(ta.stoch(close, high, low, lengthK), smoothK)

// Apply EMA to %K
emaK = ta.ema(stochK, emaSmoothingK)

// Apply EMA to %D
emaD = ta.ema(emaK, emaSmoothingD)

// Highlight when slow moving line crosses fast moving line
crossUp = ta.crossover(emaK, emaD)
crossDown = ta.crossunder(emaK, emaD)

// Plotting Double Smoothed Stochastic
plot(emaK, title="%K", color=color.blue, linewidth=2)
plot(emaD, title="%D", color=color.orange, linewidth=2)
bgcolor(crossUp ? color.new(color.green, 90) : na)
bgcolor(crossDown ? color.new(color.red, 90) : na)
hline(80, "Overbought", color=color.red, linestyle=hline.style_dotted)
hline(20, "Oversold", color=color.green, linestyle=hline.style_dotted)
