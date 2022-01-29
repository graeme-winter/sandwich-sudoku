import pickle
import random
from PIL import Image, ImageDraw, ImageFont


def generate():
    with open("packed_games.pkl", "rb") as f:
        game = list(map(int, random.choice(pickle.load(f))))

    grid = [game[9 * j : 9 * (j + 1)] for j in range(9)]

    row_sums = []
    for row in grid:
        one = row.index(1)
        nine = row.index(9)
        if abs(one - nine) == 1:
            s = 0
        elif one > nine:
            s = sum(row[nine + 1 : one])
        else:
            s = sum(row[one + 1 : nine])
        row_sums.append(s)

    cols = []
    for j in range(9):
        col = []
        for i in range(9):
            col.append(grid[i][j])
        cols.append(col)

    col_sums = []
    for col in cols:
        one = col.index(1)
        nine = col.index(9)
        if abs(one - nine) == 1:
            s = 0
        elif one > nine:
            s = sum(col[nine + 1 : one])
        else:
            s = sum(col[one + 1 : nine])
        col_sums.append(s)

    return grid, row_sums, col_sums


grid, row_sums, col_sums = generate()

sol = Image.new("RGB", (1200, 1200), color="white")
s_draw = ImageDraw.Draw(sol)

puz = Image.new("RGB", (1200, 1200), color="white")
p_draw = ImageDraw.Draw(puz)

s_draw.rectangle([(0, 0), (1200, 1200)], outline="black", width=10)
fnt = ImageFont.truetype("Arial Unicode.ttf", 60)

# generate starting squares

xy = []
while len(xy) < 10:
    t = (random.randrange(9), random.randrange(9))
    if t not in xy:
        xy.append(t)

# draw 9 x 9 grid with numbers

for i in range(1, 10):
    for j in range(1, 10):
        s_draw.rectangle(
            [(i * 100, j * 100), ((i + 1) * 100, (j + 1) * 100)], outline="black"
        )
        p_draw.rectangle(
            [(i * 100, j * 100), ((i + 1) * 100, (j + 1) * 100)], outline="black"
        )
        s_draw.text(
            (i * 100 + 35, j * 100 + 15),
            "{}".format(grid[i - 1][j - 1]),
            font=fnt,
            fill=(0, 0, 0, 255),
        )

        if (i - 1, j - 1) in xy:
            p_draw.text(
                (i * 100 + 35, j * 100 + 15),
                "{}".format(grid[i - 1][j - 1]),
                font=fnt,
                fill=(0, 0, 0, 255),
            )


# draw 3 x 3 thick grid
for i in range(3):
    for j in range(3):
        s_draw.rectangle(
            [
                (i * 300 + 100, j * 300 + 100),
                ((i + 1) * 300 + 100, (j + 1) * 300 + 100),
            ],
            outline="black",
            width=5,
        )
        p_draw.rectangle(
            [
                (i * 300 + 100, j * 300 + 100),
                ((i + 1) * 300 + 100, (j + 1) * 300 + 100),
            ],
            outline="black",
            width=5,
        )


# draw row + column sums
for i in range(9):
    s_draw.text(
        (1025, i * 100 + 110), "{}".format(col_sums[i]), font=fnt, fill=(0, 0, 0, 255)
    )
    p_draw.text(
        (1025, i * 100 + 110), "{}".format(col_sums[i]), font=fnt, fill=(0, 0, 0, 255)
    )
    if int(row_sums[i] / 10) == 0:
        s_draw.text(
            (i * 100 + 135, 1015),
            "{}".format(row_sums[i]),
            font=fnt,
            fill=(0, 0, 0, 255),
        )
        p_draw.text(
            (i * 100 + 135, 1015),
            "{}".format(row_sums[i]),
            font=fnt,
            fill=(0, 0, 0, 255),
        )
    else:
        s_draw.text(
            (i * 100 + 120, 1015),
            "{}".format(row_sums[i]),
            font=fnt,
            fill=(0, 0, 0, 255),
        )
        p_draw.text(
            (i * 100 + 120, 1015),
            "{}".format(row_sums[i]),
            font=fnt,
            fill=(0, 0, 0, 255),
        )


sol.save("solution.png", "PNG")
puz.save("puzzle.png", "PNG")
