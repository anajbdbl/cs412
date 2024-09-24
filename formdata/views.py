from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

def form(request):
    '''Show the web page with the form.'''
    template_name = "formdata/form.html"
    return render(request, template_name)

def submit(request):
    '''Process the form submission, and generate a result.'''
    template_name = "formdata/submit.html"
    
    # read the form data into python variables:
    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']
        context = {
            'name': name,
            'favorite_color':  favorite_color,

        }
        return render(request, template_name, context=context)

    return redirect("")

