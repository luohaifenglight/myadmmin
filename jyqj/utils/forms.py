#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class ChoiceNoValidateField(forms.ChoiceField):
    def validate(self, value):
        if value in self.empty_values and self.required:
            raise forms.ValidationError(
                self.error_messages['required'], code='required')


class MultiChoiceNoValidateField(forms.MultipleChoiceField):
    def validate(self, value):
        if value in self.empty_values and self.required:
            raise forms.ValidationError(
                self.error_messages['required'], code='required')