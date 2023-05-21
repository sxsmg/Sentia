from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ExerciseSerializer, UserResponseSerializer
from .models import User, Exercise, UserResponse

import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            # Authentication successful
            # Generate token or session and return appropriate response
            return Response({'message': 'Authentication successful.'})
    except User.DoesNotExist:
        pass
    
    return Response({'message': 'Authentication failed.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_exercises(request):
    exercises = Exercise.objects.all()
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def submit_response(request, exercise_id):
    user = request.user
    exercise = Exercise.objects.get(id=exercise_id)
    response_text = request.data.get('response')

    serializer = UserResponseSerializer(data={'user': user.id, 'exercise': exercise.id, 'response': response_text})
    if serializer.is_valid():
        serializer.save()
        
        # Call OpenAI API for sentiment analysis
        response = openai.Completion.create(
            engine='text-davinci-003',  # Choose the appropriate OpenAI language model
            prompt=response_text,
            max_tokens=50,  # Adjust as per your requirement
            temperature=0.5,  # Adjust as per your preference
            n=1,  # Adjust as per your preference
            stop=None,  # Customize the stop condition if needed
        )
     
        # Generate personalized feedback based on OpenAI response
        feedback = response.choices[0].text.strip()
        
        # Save the feedback to the UserResponse instance
        user_response = serializer.instance
        user_response.feedback = feedback
        user_response.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
