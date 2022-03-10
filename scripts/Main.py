import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scripts.VersionComparison import VersionComparison
from scripts.jQueryVersion import JQueryVersion


def parse_jquery_versions():
    """
    Parse the csv file to get the versions
    :return:
    """
    jquery_versions = []
    with open('/usr/jquery-data/scripts/jquery_releases.csv', 'r') as csvfile:
        jquery_reader = csv.reader(csvfile, delimiter=',')

        for row in reversed(list(jquery_reader)):
            if row[0] == 'tag':
                break
            jquery_versions.append(JQueryVersion(row[0]))

    return jquery_versions


def parse_heatmap_data(comparisons):
    return {
        'version_1': [comparison.version_1.version for comparison in comparisons],
        'version_2': [comparison.version_2.version for comparison in comparisons],
        'similarity_score': [comparison.similarity_score for comparison in comparisons]
    }

def generate_heatmap(comparisons):
    data = parse_heatmap_data(comparisons)
    df = pd.DataFrame(data)
    df = df.groupby(['version_1', 'version_2']).mean()
    df = df.unstack(level=0)
    df = df.rename(columns=lambda x: x if x != 'similarity_score' else '')
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(df)

    plt.savefig('test.png')

if __name__ == "__main__":
    with open("output.txt", "r+") as f:
        f.truncate(0)
    versions = parse_jquery_versions()
    comparisons = []
    for i in range(len(versions)):
        for j in range(i,len(versions)):
            comparisons.append(VersionComparison(versions[i], versions[j]))
    #
    # for i in range(8):
    #     for j in range(i,8):
    #         comparisons.append(VersionComparison(versions[i], versions[j]))

    generate_heatmap(comparisons)
