import math
import argparse


ERROR_MESSAGE = "Incorrect parameters"
choices=["annuity", "diff"]
parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
args = parser.parse_args()
if args.type not in choices:
    print(ERROR_MESSAGE)
    exit()
elif args.type != "annuity" and args.payment:
    print(ERROR_MESSAGE)
    exit()
elif not args.interest:
    print(ERROR_MESSAGE)
    exit()

if len(str(args).split(",")) < 4:
    print(ERROR_MESSAGE)
    exit()

P = 0
n = 0
payment = 0
if args.principal:
    P = float(args.principal)
if args.periods:
    n = int(args.periods)
if args.payment:
    payment = int(args.payment)

interest = float(args.interest)
payment_type = args.type


if P < 0 or interest < 0 or n < 0:
    print(ERROR_MESSAGE)
    exit()

i = interest / (12 * 100)
if payment_type == "diff":
    payment_sum = 0
    for m in range(1, n + 1):
        D = math.ceil((P / n) + i * (P - (P * (m - 1) / n)))
        print(f"Month {m}: payment is {D}")
        payment_sum += D

    print()
    print(f"Overpayment = {payment_sum - P}")
elif payment_type == "annuity":
    if P != 0 and n != 0:
        numerator = i * (math.pow(1 + i, n))
        denominator = (math.pow(1 + i, n) - 1)
        annuity_payment = math.ceil(P * (numerator / denominator))
        print(f"Your annuity payment = {annuity_payment}!")
        print(f"Overpayment = {n * annuity_payment - P}")
    elif payment != 0 and n != 0:
        numerator = i * (math.pow(1 + i, n))
        denominator = (math.pow(1 + i, n) - 1)
        P = math.floor(payment / (numerator / denominator))
        print(f"Your loan principal = {P}!")
        print(f"Overpayment = {n * payment - P}")
    elif payment != 0 and P != 0:
        base = 1 + i
        x = (payment / (payment - i * P))
        ans = math.ceil(math.log(x, base))
        month_form = "month" if ans == 1 else "months"
        year = ans // 12
        year_form = "year" if year == 1 else "years"
        month = math.ceil(ans - (year * 12))
        if year == 0:
            print(f"It will take {month} {month_form} to repay this loan!")
        elif month == 0 and year != 1:
            print(f"It will take {year} {year_form} to repay this loan!")
        else:
            print(f"It will take {year} years and {month} {month_form} to repay this loan!")
        print(f"Overpayment = {payment * ans - P}")


