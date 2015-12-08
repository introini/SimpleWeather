import time
LED = 1
high = 150
seconds = 50/1000
def fade(sec, LED):
    while LED <= high:
        print(LED)
        LED = LED + 1
        time.sleep(sec)
        if LED == high:
            while LED > 1:
                print(LED)
                LED = LED - 1
                time.sleep(sec)

fade(seconds, LED)