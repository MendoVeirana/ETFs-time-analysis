#!pip install yfinance
import matplotlib.pyplot as plt


def scatterplot_ETFs(tickers, summary_stats, etf_info, sector_styles, current_date, limitx, lower_limity, limity):
    plt.figure(figsize=(12, 8))
    legend_labels = {}

    # Set fixed plot limits
    plt.xlim(0, limitx)
    plt.ylim(lower_limity, limity)

    # Scatter plot for ETFs with markers and colors
    for ticker in tickers:
        if ticker in summary_stats.index:
            vol = summary_stats.loc[ticker, 'Volatility']*100
            ret = summary_stats.loc[ticker, 'Avg Yearly Return']*100

            # Check if the data point is within the specified limits before plotting
            if vol <= limitx and lower_limity <= ret <= limity :
                sector = etf_info[ticker][1]
                color, marker = sector_styles[sector]
                if sector not in legend_labels:
                    plt.scatter(vol, ret, s=150, c=color, marker=marker, label=sector)
                    legend_labels[sector] = 1
                else:
                    plt.scatter(vol, ret, s=150, c=color, marker=marker)
                plt.text(vol + 0.5, ret - 0.25, ticker, fontweight='bold')

    # Add line from origin to SPY for comparison, if SPY data is available and within limits
    if 'SPY' in summary_stats.index:
        spy_vol = summary_stats.loc['SPY', 'Volatility'] * 100
        spy_ret = summary_stats.loc['SPY', 'Avg Yearly Return'] * 100
        if spy_vol <= limitx and spy_ret <= limity:
            slope = spy_ret / spy_vol
            plt.plot([0, limitx], [0, slope * limitx], 'k--', label='Line of SPY Performance')

    plt.title(f'ETF Performance from 2017-04 to {current_date.strftime("%Y-%m")}', fontweight='bold', fontsize=16)
    plt.xlabel('Volatility [%]', fontweight='bold', fontsize=16)
    plt.ylabel('Annual Average Return [%]', fontweight='bold', fontsize=16)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True)

    # Save plot to file
    plt.savefig(f'plots/{current_date.strftime("%Y-%m")}.png')
    plt.close()