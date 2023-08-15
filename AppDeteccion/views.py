import base64
import os
from django.conf import settings
from django.shortcuts import render
from .forms import ImageUploadForm
import subprocess

def detect_camera_image(request):
    
    image_uri = None
    

    if request.method == 'POST':
        # in case of POST: get the uploaded image from the form and process it
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            
            media_path = os.path.join(settings.MEDIA_ROOT, 'capturas')

            for filename in os.listdir(media_path):
                if filename.startswith('ejemplo_'):
                    file_path = os.path.join(media_path, filename)
                    os.remove(file_path)
            
            # Generate a unique filename for the uploaded image
            image_filename = f'ejemplo_{str(image.name)}'
            image_path = os.path.join(media_path, image_filename)
            
            # Save the image to the media folder
            with open(image_path, 'wb') as img_file:
                for chunk in image.chunks():
                    img_file.write(chunk)
            
            # Get the URL of the saved image
            image_uri = os.path.join(settings.MEDIA_URL, 'capturas', image_filename)

            try:
                print("SE REALIZO LA DETECCION")
                subprocess.run(["python3","AppDeteccion/pytorchretinanet/visualize_single_image.py","--image_dir","media/capturas/","--class_list","AppDeteccion/pytorchretinanet/classes.csv","--model","AppDeteccion/pytorchretinanet/model_final.pt"])

            except RuntimeError as re:
                print(re)
                

    else:
        # in case of GET: simply show the empty form for uploading images
        form = ImageUploadForm()

    # pass the form, image URI, and predicted label to the template to be rendered
    context = {
        'form': form,
        'image_uri': image_uri,
    }

    return render(request, 'index.html',context)