import json
import subprocess
import os

class VersionComparison:

    version_1 = ''
    version_2 = ''
    match_count = 0
    line_count = 0
    jsinspect_report_json = {}

    def __init__(self, version_1, version_2):
        self.version_1 = version_1
        self.version_2 = version_2
        self.compare()


    def prepare_comparison_folders(self):
        """
        Make a comparison folder in /usr/tmp/
        :return:
        """
        FNULL = open(os.devnull, 'w')

        # Remove folder of last compare
        command = 'rm -rf /usr/tmp/'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=FNULL)
        process.communicate()
        process.wait()

        # Create a new comparison folder
        command = 'mkdir /usr/tmp/'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=FNULL)
        process.communicate()
        process.wait()

        # Make a folder for version_1
        command = 'mkdir /usr/tmp/1/'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=FNULL)
        process.communicate()
        process.wait()

        # Place the src of version_1 in its compare folder
        command = f'cp -r /usr/jquery-data/{self.version_1.version}/src/ /usr/tmp/1/'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=FNULL)
        process.communicate()
        process.wait()

        # Make a folder for version_2
        command = 'mkdir /usr/tmp/2/'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=FNULL)
        process.communicate()
        process.wait()

        # Place the src of version_2 in its compare folder
        command = f'cp -r /usr/jquery-data/{self.version_2.version}/src/ /usr/tmp/2/'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=FNULL)
        process.communicate()
        process.wait()

    def parse_jsinspect_json(self, output):
        pass


    def compare(self, threshold = 30):
        self.prepare_comparison_folders()

        # run jsinspect
        command = f'jsinspect -t {threshold} -r json --ignore .min.js /usr/tmp/'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        process.wait()

        output = json.loads(output)
        self.parse_jsinspect_json(output)
