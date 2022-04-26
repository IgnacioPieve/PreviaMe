import math

import matplotlib.pyplot as plt
from pymongo import GEO2D, MongoClient

client = MongoClient()
db = client["test_database"]


def start_database():
    db["map"].create_index([("loc", GEO2D)])
    for i in range(100):
        for j in range(100):
            db["map"].insert_one({"loc": [i, j]})


def get_all_coords():
    return db["map"].find()


def get_specific_coords(bottom_corner, top_corner):
    x = (top_corner[0] + bottom_corner[0]) / 2
    y = (top_corner[1] + bottom_corner[1]) / 2
    distance = (
        math.sqrt(
            (top_corner[0] - bottom_corner[0]) ** 2
            + (top_corner[1] - bottom_corner[1]) ** 2
        )
        / 2
    )

    return db["map"].find({"loc": {"$near": [x, y], "$maxDistance": distance}})


def plot_coords(coords, color):
    x = []
    y = []
    for coord in coords:
        x.append(coord["loc"][0])
        y.append(coord["loc"][1])
    plt.scatter(x, y, c=color)


if __name__ == "__main__":
    # start_database()
    superior = (60, 60)
    inferior = (20, 30)
    coords = get_all_coords()
    filtered_coords = get_specific_coords(superior, inferior)
    plot_coords(coords, "blue")
    plot_coords(filtered_coords, "red")
    plt.scatter(superior[0], superior[1], c="yellow")
    plt.scatter(inferior[0], inferior[1], c="yellow")
    plt.savefig("result.png", format="png")
