from django.shortcuts import render
from django.conf import settings

from .serializer import (
    OrderSerializer,
    AccountSerializer, 
    PositionSerializer, 
    PortfolioHistorySerializer, 
    ActivitiesSerializer, 
    ClockSerializer,
    BarsSerializer
)
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, viewsets
from rest_framework import request
from django.http import HttpResponse

alpaca = settings.ALPACA_CONN
 
@ensure_csrf_cookie
@permission_classes([AllowAny])
def generateCSRF(request):

    return HttpResponse('')

class AccountInfo(APIView):
    """
    Account info.
    """
    def get(self, request, format=None):
        """
        return: account info
        rtype: object
        """ 
        acct_info = AccountSerializer(alpaca.get_account())
        return Response(acct_info.data)

class Positions(APIView):
    """
    GET open positions. GET position details.
    """
    def get(self, request, **kwargs):
        """
        return: list of positions or detail of position
        """
        positions = alpaca.list_positions()
        sym = self.request.query_params.get('sym', None)
        
        if sym is not None:
            position = alpaca.get_position(sym)
            print(sym)
            return Response(position)
        
        return Response(positions)

class Orders(APIView):
    """
    GET order(s). DELETE order(s). POST order.
    """
    def get(self, request, **kwargs):
        """
        return: list of orders or details of a single order
        """
        orders = alpaca.list_orders()
        order_id = self.request.query_params.get('order_id', None)

        if order_id is not None:
            order = OrderSerializer(alpaca.get_order(order_id))
            return Response(order.data)

        orders = alpaca.list_orders()
        return Response(orders)
        
    def delete(self, request, order_id, format=None):
        pass

class Assets(APIView):
    """
    """
    pass

class Portfolio(APIView):
    """
    GET portfolio history.
    """
    def get(self, request, **kwargs):
        """
        """
        # print(self.request.query_params)
        date_start = self.request.query_params.get('date_start'),
        date_end = self.request.query_params.get('date_end', None),  
        period = self.request.query_params.get('period') + self.request.query_params.get('period_unit'),
        timeframe = self.request.query_params.get('timeframe'),
        extended_hours = self.request.query_params.get('ext-hrs')

        params = [date_start, date_end, period, timeframe, extended_hours]

        print(*params)

        history = PortfolioHistorySerializer(alpaca.get_portfolio_history(*params))
        return Response(history.data)

class Activities(APIView):
    """
    """
    def get(self, request):
        activities = ActivitiesSerializer(alpaca.get_activities())
        return Response(activities.data)

class Clock(APIView):
    """
    """
    def get(self, request):
        clock = ClockSerializer(alpaca.get_clock())
        return Response(clock.data)

class Bars(APIView):
    """
    Historic Data.
    
    return: Object(Timestamp, Open, High, Low, Close, Volume)
    """
    def get(self, request, **kwargs):
        bars = BarsSerializer(alpaca.get_bars())
        return Response(bars)

@api_view(['GET'])
def home(request, format=None):
    """
    HTML displays account info, positions, transaction history, portfolio history.

    return: HTML webpage
    """

    return render(request, 'alpaca/home.html')