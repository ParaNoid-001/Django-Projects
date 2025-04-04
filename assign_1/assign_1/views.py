from django.shortcuts import render,redirect
from django.http import HttpResponse

#def home(request):
    #return render(request,'home/index.html')
    
# Define a view for converting text to uppercase
def uppercase_converter(request):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Get the text input from the form
        text = request.POST.get('text', '')
        
        # Convert the text to uppercase
        uppercase_text = text.upper()
        
        # Render the template with the converted text
        return render(request, 'home/index.html', {'uppercase_text': uppercase_text})
    
    # Render the template without converted text for GET requests
    return render(request, 'home/index.html')