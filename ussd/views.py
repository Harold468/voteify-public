from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import EVENT
from events.models import ContestantInfo

@csrf_exempt
def index(request):
    if request.method == 'POST':
        # Get data from Africa's Talking POST request
        session_id = request.POST.get('sessionId')
        phone_number = request.POST.get('phoneNumber')
        service_code = request.POST.get('serviceCode')
        text = request.POST.get('text', '')

        text_array = text.split('*')
        
        # USSD logic based on user input
        events = EVENT.objects.all().order_by('id')

        if text == '':
            # First screen: Check Events
            response = "CON Welcome to voteify developed by Harold\n1. Check Events"
        
        elif text == '1':
            # Second screen: Select Event
            resp_data = 'Select Event\n'
            for index, event in enumerate(events):
                resp_data += f'{index+1}. {event.name_of_event.title()}\n'  # Display event options
            response = f"CON {resp_data}"
        
        elif len(text_array) == 2:
            # Third screen: Select Contestant based on selected event
            try:
                # Ensure input is valid and within range
                event_index = int(text_array[1]) - 1  # Convert to zero-based index
                if event_index < 0 or event_index >= len(events):
                    raise ValueError("Invalid event index")
                
                selected_event = events[event_index].id
                
                contestants = ContestantInfo.objects.filter(event__id=selected_event).order_by('id')
                
                if contestants.exists():
                    contestant_resp_data = 'Select Contestant\n'
                    for index, contestant in enumerate(contestants):
                        contestant_resp_data += f'{index+1}. {contestant.name.title()}\n'
                    response = f"CON {contestant_resp_data}"
                else:
                    response = "END No contestants available for this event."
            
            except (ValueError, IndexError):
                response = "END Invalid selection. Please try again."
        
        elif len(text_array) == 3:
            # Fourth screen: Vote for a contestant
            try:
                # Ensure input is valid and within range for contestant selection
                event_index = int(text_array[1]) - 1  # Convert to zero-based index
                if event_index < 0 or event_index >= len(events):
                    raise ValueError("Invalid event index")
                
                selected_event = events[event_index].id
                if (events[event_index].paid ==False):
                    response ="END This a paid event. For convient and security reasons please visit our website voteify. Thank you."
                contestants = ContestantInfo.objects.filter(event__id=selected_event).order_by('id')

                contestant_index = int(text_array[2]) - 1  # Convert to zero-based index
                if contestant_index < 0 or contestant_index >= len(contestants):
                    raise ValueError("Invalid contestant index")
                
                selected_contestant = contestants[contestant_index]
                vote_resp_data = f'Vote for {selected_contestant.name.title()}\n'
                
                # Provide voting options (e.g., 1. 2 votes, 2. 3 votes, etc.)
                for i in range(1, 10):
                    vote_resp_data += f'{i}. {i+1} Votes\n'
                response = f"CON {vote_resp_data}"
            
            except (ValueError, IndexError):
                response = "END Invalid selection. Please try again."
        
        elif len(text_array) == 4:
            try:
                # Ensure input is valid and within range for contestant selection
                event_index = int(text_array[1]) - 1  # Convert to zero-based index
                if event_index < 0 or event_index >= len(events):
                    raise ValueError("Invalid event index")
                
                selected_event = events[event_index].id
                contestants = ContestantInfo.objects.filter(event__id=selected_event).order_by('id')

                contestant_index = int(text_array[2]) - 1  # Convert to zero-based index
                if contestant_index < 0 or contestant_index >= len(contestants):
                    raise ValueError("Invalid contestant index")
                
                selected_contestant = contestants[contestant_index]
                
                # Provide voting options (e.g., 1. 2 votes, 2. 3 votes, etc.)
                
                response = f"END you cast {int(text_array[-1])+1} votes for {selected_contestant.name.title()}"
            
            except (ValueError, IndexError):
                response = "END Invalid selection. Please try again."

        elif text == '2':
            # Exit option
            response = "END Goodbye"
        
        else:
            response = "END Invalid input."

        return HttpResponse(response, content_type='text/plain')
