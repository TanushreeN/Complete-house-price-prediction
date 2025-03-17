from django.shortcuts import render, redirect
from .forms import PropertyForm
from .models import Property
import pickle
import django_tables2 as tables
from .table import Mytable

# Create your views here.
def add_property(request):
    if 'form_data' not in request.session:
        request.session['form_data'] = {}
    if 'step' not in request.session:
        request.session['step'] = 1

    step = request.session['step']
    form_data = request.session['form_data']

    if step == 1:
        fields = ['area', 'area_unit', 'bedrooms', 'bathrooms', 'state', 'city', 'zipcode']  # Added area_unit
        background_image = "step1_bg.jpeg"
    elif step == 2:
        fields = ['stories', 'mainroad', 'guestroom']
        background_image = "step2_bg.jpg"
    else:
        fields = ['basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus']
        background_image = "step3_bg.jpg"

    form = PropertyForm(request.POST or None)

    for field in list(form.fields):
        if field not in fields:
            form.fields.pop(field)

    if request.method == 'POST' and form.is_valid():
        form_data.update(form.cleaned_data)
        request.session['form_data'] = form_data

        if step < 3:
            request.session['step'] = step + 1
            return redirect('add_property')

        # Convert area based on selected unit
        area = float(form_data.get('area', 0))
        area_unit = form_data.get('area_unit')

        if area_unit == 'sq_feet':
            area = area * 0.092903  # Convert sq feet to sq meters

        data = [
            float(form_data.get('area', 0)),  # Area in sq meters
            int(form_data.get('area', 0)),  # Area in sq meters
            int(form_data.get('bedrooms', 0)),
            int(form_data.get('bathrooms', 0)),
            int(form_data.get('stories', 0)),
            int(form_data.get('mainroad', 0)),
            int(form_data.get('guestroom', 0)),
            int(form_data.get('basement', 0)),
            int(form_data.get('hotwaterheating', 0)),
            int(form_data.get('airconditioning', 0)),
            int(form_data.get('parking', 0)),
            int(form_data.get('prefarea', 0))
        ]

        furnishingstatus = form_data.get('furnishingstatus')
        if furnishingstatus == 'furnished':
            data.extend([1, 0, 0])
        elif furnishingstatus == 'unfurnished':
            data.extend([0, 1, 0])
        else:
            data.extend([0, 0, 1])

        data = [float(value) if isinstance(value, (int, float)) else 0.0 for value in data]

        regressor = pickle.load(open("random_forest.pkl", 'rb'))
        result = regressor.predict([data[:-1]])

        # Predicted price
        predicted_price = result[0]

        # Calculate cost per square meter or square foot
        if area_unit == 'sq_feet':
            cost_per_unit = predicted_price / (area / 0.092903)  # Cost per sq foot
        else:
            cost_per_unit = predicted_price / area  # Cost per sq meter

        # Final Estimation (you can modify this logic based on your needs)
        final_estimation = predicted_price * 1.1  # Adding a 10% increase for final estimation

        # Add to form data and save property
        form_data['predictedprice'] = predicted_price
        form_data['costpersqunit'] = cost_per_unit
        form_data['final_estimation'] = final_estimation

        Property.objects.create(**form_data)

        del request.session['form_data']
        del request.session['step']

        result_text = f"Predicted House Price: ₹{int(predicted_price)}"
        cost_text = f"Cost per {area_unit}: ₹{int(cost_per_unit)}"
        final_estimation_text = f"Final Estimation after 10% tax: ₹{int(final_estimation)}"
        house_image = "step3_bg.jpg"

        return render(request, 'add_property.html', {
            "result2": result_text,
            "cost_text": cost_text,
            "final_estimation_text": final_estimation_text,
            "house_image": house_image
        })

    return render(request, 'add_property.html', {'form': form, 'step': step, 'background_image': background_image})

def property_list(request):
    properties = Property.objects.all().order_by('-predictedprice')
    table = Mytable(properties)
    return render(request, 'property_list.html', {'table': table})
