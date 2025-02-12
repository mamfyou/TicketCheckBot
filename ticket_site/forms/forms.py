from django import forms


class TicketForm(forms.Form):
    date = forms.DateField(label="date", widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}  # You can add additional classes or attributes here.
    ))
    time = forms.TimeField(label="time", widget=forms.TimeInput(
        attrs={'type': 'time', 'class': 'form-control'}  # You can add additional classes or attributes here.
    ))
    from_city = forms.ChoiceField(label="from_city", choices={

    })
    to_city = forms.IntegerField(label="to_city")
    is_qom_tehran = forms.TypedChoiceField(
        label="Is Qom - Tehran?",
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        # Coerce the value from the radio button (which is a string) into a boolean.
        coerce=lambda x: x == 'True'
    )