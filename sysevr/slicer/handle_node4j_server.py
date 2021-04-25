import subprocess
import os, psutil
import time

def run_graph_server(working_directory):

    neo4j_dir = os.path.abspath(os.getcwd()).replace("\\","/") + "/external_softwares/neo4j-community-2.1.8-windows/bin/Neo4j.bat"

    config_file = open("./external_softwares/neo4j-community-2.1.8-windows/conf/neo4j-server.properties","r")

    result_line = None
    result_index = None
    lines = config_file.readlines()
    config_file.close()

    for index, line in enumerate(lines):
        if "org.neo4j.server.database.location" in line:
            temp_line = line.split("=")
            new_configs = temp_line[0] + "=" + os.path.abspath(os.getcwd()) + working_directory.replace(".","") + ".joernIndex/" + "\n"
            result_line = new_configs.replace("\\","/")
            result_index = index

    lines[result_index] = result_line
    config_file = open("./external_softwares/neo4j-community-2.1.8-windows/conf/neo4j-server.properties","w")

    config_file.writelines(lines)
    config_file.close()

    process = [neo4j_dir]

    p = subprocess.Popen(process, shell=True)

    # return result_line
    return neo4j_dir

def stop_graph_server():

    process_name = "java"

    PID = None

    for proc in psutil.process_iter():
        if process_name in proc.name().lower():
            PID = proc.pid

    print(PID)

    os.system("taskkill  /F /pid "+str(PID))