import subprocess
import time
import os, psutil, shutil
from distutils.dir_util import copy_tree

def copy_source(location):

    destination_dir = "./sysevr/test_codes/"
    source_dir = "./test_source_codes/" + location


    filenames = os.listdir(destination_dir)
    filenames.sort(key=int)
    source_dir_name = source_dir.split("/")[-1]

    if len(filenames) == 0:
        lastfile = -1
    else:
        lastfile = int(filenames[-1])
    copy_tree(source_dir, destination_dir+str(lastfile+1)+"/"+source_dir_name)

    destination_path = destination_dir+str(lastfile+1)+"/"+source_dir_name

    joern_dir = "./external_softwares/joern-0.3.1/bin/joern.jar"

    process = ["java","-jar", joern_dir, destination_path]

    p = subprocess.Popen(process, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

    for stdout_line in iter(p.stdout.readline, ""):
            print(stdout_line)
    p.stdout.close()

    p.wait()


    joern_index_path = destination_path.replace(source_dir_name,"") + ".joernIndex"
    current_dir = os.path.abspath(os.getcwd())
    current_dir = os.path.join(current_dir,".joernIndex")
    current_dir = current_dir.replace("\\","/")

    copy_tree(current_dir,joern_index_path)

    shutil.rmtree(current_dir)

    return joern_index_path.replace(".joernIndex","")

def make_directories(working_directory):
    cfg_db_path = working_directory + 'cfg_db'
    pdg_db_path = working_directory + 'pdg_db'
    call_graph_path = working_directory + 'dict_call2cfgNodeID_funcID'
    slice_point_path = working_directory + "slice_points"
    slice_file_path = working_directory + "slice_files"
    corpus_path = working_directory + "corpus"
    vector_path = working_directory + "vector"
    mode_input_path = working_directory + "model_input"

    os.makedirs(cfg_db_path)
    os.makedirs(pdg_db_path)
    os.makedirs(call_graph_path)
    os.makedirs(slice_file_path)
    os.makedirs(slice_point_path)
    os.makedirs(corpus_path)
    os.makedirs(vector_path)
    os.makedirs(mode_input_path)