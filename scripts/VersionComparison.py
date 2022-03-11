import json
import subprocess
import os

class VersionComparison:

    version_1 = ''
    version_2 = ''
    match_count = 0
    line_count = 0
    duplicate_dict = {}
    files_dict = {}
    jsinspect_report_json = {}
    similarity_score = 0
    total_lines = 0

    def __init__(self, version_1, version_2):
        self.version_1 = None
        self.version_2 = None
        self.match_count = 0
        self.line_count = 0
        self.duplicate_dict = {}
        self.files_dict = {}
        self.jsinspect_report_json = {}
        self.version_1 = version_1
        self.version_2 = version_2
        if self.version_1.version == self.version_2.version:
            self.similarity_score = 1
            return
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

        # outro.js and intro.js generate issues, so we remove them
        command = 'rm /usr/tmp/1/src/outro.js'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        process.communicate()
        process.wait()
        command = 'rm /usr/tmp/1/src/intro.js'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
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

        # outro.js and intro.js generate issues, so we remove them
        command = 'rm /usr/tmp/2/src/outro.js'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        process.communicate()
        process.wait()
        command = 'rm /usr/tmp/2/src/intro.js'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        process.communicate()
        process.wait()


    def parse_jsinspect_json(self, output):
        self.duplicate_dict = {}
        for duplicate in output:
            instance = duplicate['instances'][0]
            # If we already parsed this duplicate then skip
            if (duplicate['id'] in self.duplicate_dict):
                break

            self.duplicate_dict[duplicate['id']] = True
            self.line_count += instance['lines'][1] - instance['lines'][0]
            # to keep track of the amount of files
            if not instance['path'] in self.files_dict:
                self.files_dict[instance['path']] = True


    def calculate_total_lines(self):
        for x in range(2):
            # run cloc
            command = f'cloc /usr/tmp/{x+1}/'
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            process.wait()
            output = output.decode('utf-8')
            number_of_lines = 0
            for line in output.splitlines():
                if 'JavaScript' in line or 'javascript' in line or 'Javascript' in line:
                    number_of_lines += int(line.split()[4])
            self.total_lines = max(self.total_lines, number_of_lines)

    def compare(self, threshold = 33):
        self.prepare_comparison_folders()

        # run jsinspect
        command = f'jsinspect -t {threshold} -I -r json --ignore .min.js /usr/tmp/'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        process.wait()

        output = json.loads(output)
        self.jsinspect_report_json = output
        self.parse_jsinspect_json(output)
        self.match_count = len(self.duplicate_dict)

        self.calculate_total_lines()

        self.similarity_score = self.line_count / self.total_lines

        res = F"""
Done comparing {self.version_1.version} with {self.version_2.version}
Amount of duplicate lines: {self.line_count}, 
Amount of total_lines: {self.total_lines}, 
Amount of similar files: {len(self.files_dict)}
Amount of duplicates: {len(self.duplicate_dict)}
Similarity score: {self.similarity_score}
        
        
"""
        print(res)
        f = open("output.txt", "a")
        f.write(res)
        f.close()
