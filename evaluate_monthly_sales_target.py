# -*- coding: utf-8 -*-
"""
Calculate the probability of meeting the monthly sales target given the current date and amount left.

This module can be imported in e.g. jupyter notebook for more interactive use.

Example:
    python evaluate_monthly_sales_target.py "2016-07-14" 20000 1000 200

    Will return the probability of making $20k in sales in the rest of July,
    starting from 2016-07-14. Assuming that the mean of daily sales is $1000 and standard deviation
    is 200.

Example 2:
    python evaluate_monthly_sales_target.py "2016-07-14" 20000 1000 200 --iterations 10000 --wekend 2

    Optional parameters available:
        --weekend: Effect on sales during the weekend. 1 - no effect,
            0.5 - mean of sales reduced 50%, 1.5 - mean of sales increased 50%, etc. Default: 0.

        --iterations: Number of iterations to run. Default: 1000.

"""

import arrow
import numpy.random


def simulate_monthly_sales(sales_mean, sales_stddev, starting_date, iterations=2000, weekend_effect=1):
    """
    Return list of simulated daily sales
    :param sales_mean: Mean of daily sales
    :param sales_stddev: Standard deviation of daily sales
    :param starting_date: Simulation starting date
    :param iterations: Number of iterations to perform
    :return: List of lists of daily simulated sales (dollar amount).
    """

    simulated_sales = list()

    for run_id in range(iterations):
        current_date = arrow.get(starting_date)
        starting_month = current_date.format("M")
        sales_cumulative = [0] # starting with $0 on day 1

        while current_date.format("M") == starting_month:
            if int(current_date.format("d")) in [6,7]:
                daily_sales = numpy.random.normal(sales_mean * weekend_effect, sales_stddev)
            else:
                daily_sales = numpy.random.normal(sales_mean, sales_stddev)
            sales_cumulative.append(sales_cumulative[-1] + daily_sales)

            current_date = current_date.replace(days=1) # advance one day

        simulated_sales.append(sales_cumulative)

    return simulated_sales

def target_met_frequency(simulated_daily_sales, target):
    """
    Percentage of simulations where the sales target has been met.
    :param simulated_daily_sales: Results of simulations.
    :param target: The sales target.
    :return: Percentage (e.g. 0.95).
    """
    days_when_target_met = [sales[-1] for sales in simulated_daily_sales if sales[-1] >= target]

    return float(len(days_when_target_met)) / len(simulated_daily_sales)

if __name__ == '__main__':
    import argparse

    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument("starting_date", help="Simulation starting date")
    arguments_parser.add_argument("target", help="Target sales amount", type=float)
    arguments_parser.add_argument("mean", help="Mean of daily sales", type=float)
    arguments_parser.add_argument("stddev", help="Standard deviation of daily sales", type=float)

    #optional
    arguments_parser.add_argument("--iterations", help="Number of simulations to run", type=int)
    arguments_parser.add_argument("--weekend", help="Weekend multiplier for the mean", type=float)

    args = arguments_parser.parse_args()

    iterations = args.iterations if args.iterations is not None else 1000
    weekend_multiplier = args.weekend if args.weekend is not None else 1

    simulated_sales = simulate_monthly_sales(
        args.mean, args.stddev, args.starting_date,
        iterations=iterations, weekend_effect=weekend_multiplier
    )

    print("Starting date: {s_date}".format(s_date=args.starting_date))
    print(u"μ=${:.2f}, SD={:.2f}".format(args.mean, args.stddev))
    print("Target: ${:.2f}".format(args.target))
    print("Target met: {}%".format(target_met_frequency(simulated_sales, args.target) * 100))