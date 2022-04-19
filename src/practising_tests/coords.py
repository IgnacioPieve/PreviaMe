from pymongo import MongoClient, GEO2D
import matplotlib.pyplot as plt

client = MongoClient()
db = client['test_database']



def start_database():
    db["map"].create_index([("loc", GEO2D)])
    for i in range(100):
        for j in range(100):
            db["map"].insert_one({"loc": [i, j]})


def get_all_coords():
    return db["map"].find()


def get_specific_coords(x, y, max_distance):
    return db["map"].find({
        "loc": {"$near": [x, y], "$maxDistance": max_distance}
    })


def plot_coords(coords, color):
    x = []
    y = []
    for coord in coords:
        x.append(coord["loc"][0])
        y.append(coord["loc"][1])
    plt.scatter(x, y, c=color)


if __name__ == "__main__":
    coords = get_all_coords()
    filtered_coords = get_specific_coords(50, 50, 10)
    plot_coords(coords, "blue")
    plot_coords(filtered_coords, "red")
    plt.savefig('result.png', format='png')


