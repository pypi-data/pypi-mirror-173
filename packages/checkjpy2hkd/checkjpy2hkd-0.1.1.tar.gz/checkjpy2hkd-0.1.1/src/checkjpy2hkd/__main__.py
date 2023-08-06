# __main__.py

from checkjpy2hkd import CONFIG
from checkjpy2hkd import checker


def main():
    jpy2hkd_data = checker.get_jpy2hkd_rates()
    print("-----------------")
    print("Running from Main!")
    print(CONFIG["url"]["ttrate"])
    for k, v in jpy2hkd_data.items():
        print(f"Vendor={k}; Rate={v}")


if __name__ == "__main__":
    main()