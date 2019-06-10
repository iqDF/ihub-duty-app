from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from utils.singletons import SingletonModel
from duties.errors import (
	MaxDutyCountError, UnfinishedDutyError
)

User = get_user_model()
duty_manager = DutyManager.load()

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def duty_api_start_view(request):
    user = request.user
    try:
        duty_manager.remove_finished_duties()
        duty = duty_manager.start_duty(user)
    except UnfinishedDutyError as e:
        return Response(
            {
                'success': False,
                'message': e.message,
            },
            status=status.HTTP_400_BAD_REQUEST 
        )
    except MaxDutyCountError as e:
        return Response(
            {
                'success': False,
                'message': e.message,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {
                'success': False,
                'message': e.message,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Success
    serializer = DutySerializer(duty)
    return Response(
        {
            'success': True,
            'message': "Object %s created successfully" % duty,
            'payload': serializer.data,
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def duty_api_detail_view(request):
    user = request.user
    duty_manager.remove_finished_duties()

    if user.duty_set.count() == 0:
        return Response(
            {
                'success': False, 
                'message': "User has no ongoing duty at the moment."
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    elif duty_manager.is_onduty(user) == False:
        return return Response(
            {
                'success': False, 
                'message': "User's duty is not registered in manager"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Success
    duty = duty_manager.get_duties_of(user)
    serializer = DutySerializer(duty, many=True)
    return Response(
        {
            'success': True,
            'message': "%s sent" % duty,
            'payload': serializer.data
        },
        status=status.HTTP_200_OK
    )
