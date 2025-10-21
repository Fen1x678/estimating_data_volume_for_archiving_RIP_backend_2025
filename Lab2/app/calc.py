def calc(algorithms):
    volume = 0

    for pc in algorithms:
        algorithm = pc.algorithm
        volume += pc.volume / algorithm.ratio

    return volume
