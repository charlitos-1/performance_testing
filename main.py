from resources.decorators import function_performance
import pandas as pd


def generate_random_data(num_cols, num_rows, filename="data.csv"):
    header = ",".join([f"header{i+1}" for i in range(num_cols)]) + "\n"
    with open(filename, "w") as fout:
        fout.write(header)
        for i in range(num_rows):
            data = ",".join(
                [f"column{j+1}+row{i+1}" for j in range(num_cols)]) + "\n"
            fout.write(data)


@function_performance
def read_csv(filename="data.csv"):
    df = pd.read_csv(filename)
    # print(df)
    return


@function_performance
def read_csv_and_append_cols(filename="data.csv", add_n_colums=5):
    df = pd.read_csv(filename)
    for i in range(add_n_colums):
        new_col_name = f"newheader{i}"
        data = f"static_data{i}"
        df[new_col_name] = data

    return


def main():
    num_starting_cols = 20
    additional_cols = 10
    num_rows = 100_000
    generate_random_data(num_starting_cols, num_rows, "data.csv")
    generate_random_data(num_starting_cols+additional_cols, num_rows, "data2.csv")

    read_csv("data2.csv")
    read_csv_and_append_cols("data.csv", add_n_colums=additional_cols)
    return


if __name__ == "__main__":
    main()
