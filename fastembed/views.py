from rest_framework.decorators import api_view
from rest_framework.response import Response
from .predictor.lookup import getCveList
import json


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/prediction-list/',
    }

    return Response(api_urls)


@api_view(['POST'])
def uploadCve(request):
    print("printing", request.data)
    response = request.data
    cve_list = getCveList(response)

    json_indexed_cve_list = json.loads(json.dumps(cve_list.to_json(orient= "records")))
    print(json_indexed_cve_list)

    return Response(json_indexed_cve_list)