from django import forms


class TicketForm(forms.Form):
    date = forms.DateField(label="تاریخ حرکت", widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'persian-datepicker form-control'}
    ))
    time = forms.TimeField(label="زمان حرکت", widget=forms.TimeInput(
        attrs={'type': 'time', 'class': 'form-control'}
    ), required=False)

    is_qom_tehran = forms.TypedChoiceField(
        label="قم-تهران(تیک نزدن = تهران-قم)",
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        coerce=lambda x: x == 'True'
    )
