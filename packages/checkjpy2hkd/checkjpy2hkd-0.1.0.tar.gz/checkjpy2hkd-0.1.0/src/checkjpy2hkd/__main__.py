# __main__.py

from checkjpy2hkd import CONFIG

def get_jpy2hkd_rates():
    jpy2hkd_data = {"匯豐": 0.053100, "恒生": 0.052950, "南洋": 0.052680}
    return jpy2hkd_data


def main():
    jpy2hkd_data = get_jpy2hkd_rates()
    print("-----------------")
    print("Running from Main!")
    print(CONFIG["url"]["ttrate"])
    for k, v in jpy2hkd_data.items():
        print(f"Vendor={k}; Rate={v}")

if __name__ == "__main__":
    main()