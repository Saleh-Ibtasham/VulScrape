from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from .serializers import SourceCodeSerializer
from .slicer.source_code_copy_utility import copy_source, make_directories
from .slicer.handle_node4j_server import run_graph_server, stop_graph_server
from .slicer.get_cfg_relation import deliverCfg
from .slicer.complete_PDG import *
from .slicer.access_db_operate import *
from .slicer.points_get import deliverSlicePoints
from .slicer.extract_df import deliverProgramSlices
from .slicer.process_dataflow_func import deliverCorpus
from .slicer.get_dl_input import deliverVectors
from .slicer.slice_cleanup import clean_slices
import time
from .slicer.sysevr_model import getDetectionsSys
from .vdpecker.vd_model import getDetectionsVd

global working_code_directory

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/cve-list/<str:pk>/',
        'Program Slice View': '/program-list/<str:pk>/',
    }

    return Response(api_urls)

@api_view(['POST'])
@parser_classes([MultiPartParser,FileUploadParser])
def uploadCode(request):
    print("printing", request.data)
    code_serializer = SourceCodeSerializer(data=request.data)
    if code_serializer.is_valid():
        source_code_location = code_serializer.data.get("files").split('/')[0]
        slicer(source_code_location)
    else:
        print("didn't find it")
    return Response(working_code_directory)

@api_view(['GET','POST'])
def sysevrlist(request):
    print(request.data)
    working_code_directory = request.data;
    vulnerable_cve_list = getDetectionsSys(working_code_directory)
    print(vulnerable_cve_list)
    return Response("getting there")

@api_view(['Get','POST'])
def vuldeepeckerlist(request):
    print(request.data)
    working_code_directory = "./sysevr/test_codes/1/"
    # vulnerable_cve_list = getDetectionsVd(working_code_directory)
    # print(vulnerable_cve_list)
    return Response("getting there vuldeepecker")



def slicer(source_code_location):
    global working_code_directory
    working_code_directory = copy_source(source_code_location)
    graph_config = run_graph_server(working_code_directory)
    time.sleep(15.00)
    print(working_code_directory, graph_config)
    make_directories(working_code_directory)
    deliverCfg(working_code_directory)
    deliverePdg(working_code_directory)
    deliverCallGraph(working_code_directory)
    deliverSlicePoints(working_code_directory)
    stop_graph_server()
    deliverProgramSlices(working_code_directory)
    # clean_slices(working_code_directory)
    deliverCorpus(working_code_directory)
    deliverVectors(working_code_directory)
