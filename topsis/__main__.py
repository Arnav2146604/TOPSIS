import pandas as pd
import os
import sys


def Normalize(temp_dataset, nCol, weights):
    for i in range(1, nCol):
        temp = 0
        for j in range(len(temp_dataset)):
            temp = temp + temp_dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(temp_dataset)):
            temp_dataset.iat[j, i] = (
                temp_dataset.iloc[j, i] / temp)*weights[i-1]
    return temp_dataset


def Calc_Values(temp_dataset, nCol, impact):
    p_sln = (temp_dataset.max().values)[1:]
    n_sln = (temp_dataset.min().values)[1:]
    for i in range(1, nCol):
        if impact[i-1] == '-':
            p_sln[i-1], n_sln[i-1] = n_sln[i-1], p_sln[i-1]
    return p_sln, n_sln


def topsis(temp_dataset, dataset, nCol, weights, impact):
    temp_dataset = Normalize(temp_dataset, nCol, weights)

    p_sln, n_sln = Calc_Values(temp_dataset, nCol, impact)

    score = []
    for i in range(len(temp_dataset)):
        temp_p, temp_n = 0, 0
        for j in range(1, nCol):
            temp_p = temp_p + (p_sln[j-1] - temp_dataset.iloc[i, j])**2
            temp_n = temp_n + (n_sln[j-1] - temp_dataset.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    dataset['Topsis Score'] = score

    dataset['Rank'] = (dataset['Topsis Score'].rank(
        method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})
    dataset.to_csv(sys.argv[4], index=False)


def main():
    if len(sys.argv) != 5:
        print("Incorrect Number of Parameters")
        exit(1)
    elif not os.path.isfile(sys.argv[1]):
        print("File not found")
        exit(1)
    else:
        dataset, temp_dataset = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        nCol = len(temp_dataset.columns.values)

        if nCol < 3:
            print("Input file have less than 3 columns")
            exit(1)

        for i in range(1, nCol):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

        weights = [int(i) for i in sys.argv[2].split(',')]
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                exit(1)

        if nCol != len(weights)+1 or nCol != len(impact)+1:
            print(
                "Number of weights, impacts and columns are not same")
            exit(1)

        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        topsis(temp_dataset, dataset, nCol, weights, impact)


if __name__ == "__main__":
    main()
