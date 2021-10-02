import sys

from stocks import explore_buy_opportunities

if __name__ == "__main__":
    """
    This program computes, given a budget (in USD) the maximum profit that one could have
    made in the past month. Assuming you can only buy one stock per ticker and buy/sale
    either at open or close of the market. In other words, this passive investor is not
    involved in day trading. This is a concurrent program that could take advantage of
    hardware that supports parallel execution.
    """
    if len(sys.argv) != 2:  # wrong usage of program
        print(f"Error: {sys.argv[0]} [budget]")
        exit(0)
    budget: float = float(sys.argv[1])
    explore_buy_opportunities(budget=budget)
