import json
import yfinance as yf

from constants import NUM_WORKERS, TICKERS_JSON
from models import BuyOpportunity
from multiprocessing import Pool
from typing import List


def load_tickers() -> List[str]:
    """
    Returns the list of tickers from the JSON file.
    """
    with open(TICKERS_JSON, 'r') as f:
        return json.load(f)


def calculate_buy_opportunity(ticker: str, buy_sell_prices: List[float]) -> BuyOpportunity:
    """
    Returns the best buying opportunity for the provided ticker given its daily open and close prices.

    ticker (str): ticker of interest.
    buy_sell_prices (List[float]): prices at which the ticker can be bought or sold.
    """
    min_price: float = float('inf')
    max_profit: float = 0.0
        
    for price in buy_sell_prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    
    return BuyOpportunity(buy_price=round(min_price, 1), profit=round(max_profit, 1), ticker=ticker)


def get_buy_opportunity(ticker: str) -> BuyOpportunity:
    """
    Fetches the ticker's last month of data and returns its best buying opportunity.

    ticker (str): ticker of interest.
    """
    buy_sell_prices: List[float] = []
    monthly_data = yf.Ticker(ticker).history(period="1mo")

    for _, daily_data in monthly_data.iterrows():
        buy_sell_prices.append(daily_data['Open'])
        buy_sell_prices.append(daily_data['Close'])
    
    buy_opportunity: BuyOpportunity = calculate_buy_opportunity(ticker=ticker, buy_sell_prices=buy_sell_prices)
    return buy_opportunity
    

def get_all_buy_opportunities(tickers: List[str]) -> List[BuyOpportunity]:
    """
    Returns the best buying opportunities for each provided ticker.

    tickers (List[str]): tickers of interest.
    """
    with Pool(processes=NUM_WORKERS) as process_pool:
        buy_opportunities: List[BuyOpportunity] = process_pool.map(get_buy_opportunity, tickers)
    
    return buy_opportunities


def get_top_buy_opportunites(budget: float, buy_opportunities: List[BuyOpportunity]) -> List[BuyOpportunity]:
    """
    Returns the best buying opportunities which can be afforded under the given budget.

    budget (float]): budget in USD.
    buy_opportunities (List[BuyOpportunity]): best buying opportunities for all tickers of interest.
    """
    top_buy_opportunities: List[BuyOpportunity] = []
    remaining_budget: int = budget
    buy_opportunities.sort(key=lambda buy_opportunity: buy_opportunity.profit, reverse=True)

    for top_buy_opportunity in buy_opportunities:
        remaining_budget -= top_buy_opportunity.buy_price
        if remaining_budget < 0: break
        top_buy_opportunities.append(top_buy_opportunity)

    return top_buy_opportunities


def get_total_profit(top_buy_opportunities: List[BuyOpportunity]) -> float:
    """
    Returns the total profit made.

    top_buy_opportunities (List[BuyOpportunity]): top buying opportunities under the given budget.
    """
    total_profit: float = 0.0

    for top_buy_opportunity in top_buy_opportunities:
        total_profit += top_buy_opportunity.profit
        
    return round(total_profit, 1)


def print_buy_opportunites(budget: float, total_profit: float, top_buy_opportunities: List[BuyOpportunity]) -> None:
    """
    Prints the buying opportunities.

    budget (float]): budget in USD.
    total_profit (float): total profit made in USD.
    top_buy_opportunities (List[BuyOpportunity]): top buying opportunities under the given budget.
    """
    if not top_buy_opportunities:
        print(f"You did not miss any buy opportunities this month for a budget of ${budget}:")
        return

    print(f"Here are the buy opportunities you missed this month with a budget of ${budget}:")
    for top_buy_opportunity in top_buy_opportunities:
        top_buy_opportunity.print()
    print(f"For a total profit of ${total_profit}.")


def explore_buy_opportunities(budget: float) -> None:
    """
    Explores and outputs on standard output the best buying opportunity one could have
    made in the last month given a budget.

    budget (float]): budget in USD.
    """
    tickers: List[str] = load_tickers()
    buy_opportunities: List[BuyOpportunity] = get_all_buy_opportunities(tickers=tickers)
    top_buy_opportunities: List[BuyOpportunity] = get_top_buy_opportunites(budget=budget, buy_opportunities=buy_opportunities)
    total_profit: int = get_total_profit(top_buy_opportunities=top_buy_opportunities)
    print_buy_opportunites(budget=budget, total_profit=total_profit, top_buy_opportunities=top_buy_opportunities)
