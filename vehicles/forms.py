from django import forms

import re

class VehicleSearchForm(forms.Form):
    vsn = forms.CharField(max_length=12, label='VSN')

    def clean_vsn(self):
        data = self.cleaned_data['vsn']

        if not len(data) == 12:
            raise forms.ValidationError('VSNs must be 12 characters long.')

        if data.find('*') >= 0:
            raise forms.ValidationError('You may not include wildcards in your search.')

        #vsn_regex = r'[a-zA-Z*]{6}[0-9*]{6}'
        vsn_regex = r'[a-zA-Z]{6}[0-9]{6}'
        if not re.match(vsn_regex, data):
            raise forms.ValidationError('Invalid VSN format. Must be 6 letters followed by 6 numbers.')

        return data
