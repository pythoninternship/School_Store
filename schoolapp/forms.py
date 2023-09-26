from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Department, Course, Purpose, Material

class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class OrderForm(forms.Form):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    PURPOSE_CHOICES = Purpose.objects.all().values_list('id', 'name')

    MATERIALS_CHOICES = Material.objects.all().values_list('id', 'name')

    name = forms.CharField(label='Name')
    dob = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))
    age = forms.IntegerField(label='Age')
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect)
    phone = forms.CharField(label='Phone Number', max_length=15)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Address', widget=forms.Textarea)
    department = forms.ModelChoiceField(label='Department', queryset=Department.objects.all())
    course = forms.ModelChoiceField(label='Course', queryset=Course.objects.none(), required=False)
    purpose = forms.ChoiceField(label='Purpose', choices=PURPOSE_CHOICES)
    materials = forms.MultipleChoiceField(label='Materials Provide', choices=MATERIALS_CHOICES, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Initially, set an empty queryset for the course field
        self.fields['course'].queryset = Course.objects.none()

        # Populate course choices based on the selected department (if any)
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['course'].queryset = Course.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass

    # Override clean method to validate course based on the selected department
    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        course = cleaned_data.get('course')

        if department and not course:
            raise forms.ValidationError("Please select a course for the selected department.")

        return cleaned_data
