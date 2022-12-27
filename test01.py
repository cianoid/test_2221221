class Car:
    color: str
    speed: float

    def __init__(self, color, speed):
        self.color = color
        self.speed = speed


def run():
    blue_car = Car("blue", 120)
    return blue_car.speed


if __name__ == "__main__":
    print(run())
