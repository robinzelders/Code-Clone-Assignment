import csv

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

if __name__ == "__main__":
    versions = parse_jquery_versions()
    comparison = VersionComparison(versions[0], versions[1])




