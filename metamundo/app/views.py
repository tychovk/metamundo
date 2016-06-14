from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')

def control_panel(request):
    return render(request, 'control_panel.html')
    #return render(request, 'control_panel.html')

    