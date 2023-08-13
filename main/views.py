import requests, json, math
from django.conf import settings
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .serializers import *
from rest_framework.permissions import AllowAny
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins


class StoreViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    # 두 지점 간의 거리를 계산하는 함수
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # 위도와 경도를 라디안 단위로 변환
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # 지구 반경 (미터)
        R = 6371000

        # 위도 및 경도 차이 계산
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine 공식 계산
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance
    
    @action(detail=False, methods=['GET'])
    def get_near_store(self, request):#,request):
        # user_latitude = request.GET.get('latitude')
        # user_longitude = request.GET.get('longitude')
        # 임시로 확인할 값. 추후 request로 받아올 예정
        user_latitude = 37.4688345
        user_longitude = 127.0412415
        
        stores = Store.objects.all()

        nearby_stores = []  # 주변 가게들을 담을 리스트

        for store in stores:
            store_latitude = float(store.latitude)
            store_longitude = float(store.longitude)

            distance = self.calculate_distance(user_latitude, user_longitude, store_latitude, store_longitude)
            
            if distance <= 500:
                # 임시로 카페 기준으로만 500m 내의 가게들 불러옴. 베이커리, 아이스크림 기타 등등 존재. 식당은 아직 구현 X
                if "카페" in store.type:
                    nearby_stores.append(store)

        queryset = nearby_stores[:20]
        serializer = StoreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def scrap(self, request, pk=None):
        store = get_object_or_404(Store, pk=pk)
        user = request.user

        scrap, created = Scrap.objects.get_or_create(user=user, store=store)
        
        if created:
            return Response({'message': 'Store has been scrapped.'}, status=201)
        else:
            return Response({'message': 'Store is already scrapped.'}, status=200)
        
    
    @action(detail=True, methods=['POST'])
    def unscrap_store(self, request, pk=None):
        store = get_object_or_404(Store, pk=pk)
        user = request.user

        try:
            scrap = Scrap.objects.get(user=user, store=store)
            scrap.delete()
            return Response({'message': 'Store unscrapped successfully.'}, status=200)
        except Scrap.DoesNotExist:
            return Response({'error': 'Store is not scrapped.'}, status=400)
    

    def get_store_detail(request):
        store_id = request.GET.get('store_id')
        queryset = Store.objects.filter(store_id=store_id)
        serializer = StoreSerializer(queryset)
        return Response(serializer.data)
    