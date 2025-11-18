def calc(compression):
    volume = 0

    algorithms = compression["algorithms"]
    for algorithm in algorithms:
        volume += algorithm['volume'] / algorithm['ratio']

    return volume