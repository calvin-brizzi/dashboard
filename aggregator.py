from afriscraper import afrihost_data
from vodascraper import MyVodacom


def main():
    print afrihost_data()
    data = MyVodacom("calvin.brizzi@gmail.com", "").login().get_bundle_balances(["0827138706"])
    print data["0827138706"]["Airtime"]["remaining"]

if __name__ == '__main__':
    main()
