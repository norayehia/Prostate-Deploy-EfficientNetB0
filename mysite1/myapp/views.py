from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from .models import Image

# Load the trained model
model = load_model('E:/firstpro/trained/prostate.h5')

def predict_image(request):
    if request.method == 'POST':
        # Get the uploaded image from the form
        uploaded_image = request.FILES['image']

        # Save the uploaded image to a temporary location
        fs = FileSystemStorage()
        image_path = fs.save(uploaded_image.name, uploaded_image)
        image_url = fs.url(image_path)

        # Load and preprocess the image using the ImageDataGenerator
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0  # Normalize the image
        img_array = img_array.reshape(1, 224, 224, 3)

        # Make the prediction using the loaded model
        prediction = model.predict(img_array)
        predicted_class = prediction.argmax()

        # Save the image and its prediction to the database
        Image.objects.create(image=image_url, prediction=predicted_class)

        # Pass the prediction result to the template
        context = {'image_url': image_url, 'predicted_class': predicted_class}
        return render(request, 'result.html', context)

    return render(request, 'upload.html')