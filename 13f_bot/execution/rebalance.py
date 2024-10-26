import alpaca_trade_api as tradeapi
import logging
import extraction.data_collection as data_collection  # Import from data_collection
import main.config as config  # Importing config from the scripts directory
import pandas as pd

# Setting up Alpaca API using keys from config.py
api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.BASE_URL)
logger = logging.getLogger(__name__)

def rebalance_portfolio(investor_cik):
    """
    Rebalances the portfolio to mimic the 13F filings of an institutional investor.
    """
    # Fetch 13F filings from SEC EDGAR using data_collection
    filings_df = data_collection.get_13f_filings(investor_cik)
    if filings_df.empty:
        logger.error("No 13F filings found.")
        return

    # Get account information
    account = api.get_account()
    portfolio_value = float(account.portfolio_value)
    current_cash = float(account.cash)

    # Fetch current positions
    positions = api.list_positions()
    current_allocations = {position.symbol: float(position.market_value) / portfolio_value for position in positions}

    # Rebalance based on 13F filings
    for _, row in filings_df.iterrows():
        symbol = row['symbol']
        target_pct = row['allocation'] / 100  # Convert allocation to percentage
        target_value = portfolio_value * target_pct
        current_value = portfolio_value * current_allocations.get(symbol, 0)

        # Buy or sell based on current vs target allocation
        if target_value > current_value:
            buy_amount = target_value - current_value
            if buy_amount <= current_cash:
                qty_to_buy = buy_amount // float(api.get_last_trade(symbol).price)
                if qty_to_buy > 0:
                    api.submit_order(
                        symbol=symbol,
                        qty=qty_to_buy,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                    )
                    logger.info(f"Bought {qty_to_buy} shares of {symbol} to mimic 13F filings.")
                    current_cash -= buy_amount

        elif target_value < current_value:
            sell_amount = current_value - target_value
            qty_to_sell = sell_amount // float(api.get_last_trade(symbol).price)
            if qty_to_sell > 0:
                api.submit_order(
                    symbol=symbol,
                    qty=qty_to_sell,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                logger.info(f"Sold {qty_to_sell} shares of {symbol} to rebalance.")

    logger.info(f"Rebalancing based on 13F filings completed. Remaining cash: {current_cash}")

if __name__ == "__main__":
    # Example: CIK for Berkshire Hathaway (Warren Buffett)
    investor_cik = "0001067983"
    rebalance_portfolio(investor_cik)
    logger.info("13F bot execution completed.")
