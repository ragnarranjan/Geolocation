from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from xml.dom import minidom
import os
from .constants import XML, JSON, GOOGLE_API_URL
#include this file while setting this project
from  .credentials import KEY


class AddressDetail(APIView):
    def post(self, request, format=None):        
        address = request.data.get("address")
        output_format =  request.data.get("output_format")

        params = {
            "address":address,
            "key":KEY
        }

        response = requests.get(
            url=GOOGLE_API_URL, params=params
        )

        if str(response.status_code).startswith("2"):
            response = response.json()
            lat_lng = response.get("results")[0].get("geometry").get("location")
            lat = lat_lng.get("lat")
            lng = lat_lng.get("lng")

            if output_format == JSON:
                data = {
                    "coordinates": {
                        "lat": lat,
                        "lng": lng
                    },
                    "address":address
                }
                return Response(data, status=status.HTTP_200_OK)
            elif output_format == XML:
                root = minidom.Document()
                xml = root.createElement('root') 
                root.appendChild(xml)
                addressChild = root.createElement('addr')
                xml.appendChild(addressChild)
                text = root.createTextNode(str(address))
                addressChild.appendChild(text)
                addressChildcord = root.createElement('coordinate')
                xml.appendChild(addressChildcord)
                text = root.createTextNode('')
                addressChildcord.appendChild(text)
                lattiChild = root.createElement(str(lat))
                addressChildcord.appendChild(lattiChild)
                text = root.createTextNode("lat")
                lattiChild.appendChild(text)
                longiChild = root.createElement(str(lng))
                addressChildcord.appendChild(longiChild)
                text = root.createTextNode("Lattitide")
                longiChild.appendChild(text)
                xml_str = root.toprettyxml(indent ="\t") 
                save_path_file = "response.xml"                
                with open(save_path_file, "w") as f:
                    f.write(xml_str) 
                return HttpResponse(open(save_path_file).read(),content_type='text/xml')
        else:
            return Response({"message":"No result found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
