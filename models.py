from dataclasses import dataclass

@dataclass
class BuyOpportunity:
    """
    A class to represent a stock's buying opportunity.

    buy_price (float): The buying price for this opportunity.
    profit (float): The profit made from this opportunity.
    ticker (str): The ticker of interest.
    """
    buy_price: float
    profit: float
    ticker: str

    def print(self) -> None:
        """
        Prints the buying opportunity.
        """
        print(f"\t-{self.ticker} purchased at ${self.buy_price} for a profit of ${self.profit}.")
