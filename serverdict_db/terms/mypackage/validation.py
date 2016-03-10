import re

from django.contrib.auth.models import User

from terms.mypackage.html_helper import Alert, get_random_magic_word


class FormValidator:
    email_regex = r'[^@]+@[^@]+\.[^@]+'
    password_regex = r'.{8,32}'
    username_regex = r'[a-zA-Z_-]'

    def __init__(self, remove_lists=True, **validation_kwargs):
        self._arguments = validation_kwargs
        self._errors = []
        if 'csrfmiddlewaretoken' in self._arguments:
            del self._arguments['csrfmiddlewaretoken']

        if remove_lists:
            for k, v in self._arguments.items():
                if isinstance(v, list):
                    self._arguments[k] = v[0]

        if 'first_name' in self._arguments.keys():
            self._arguments['first_name'] = self._arguments['first_name'].strip()
        if 'last_name' in self._arguments.keys():
            self._arguments['last_name'] = self._arguments['last_name'].strip()

    def errors(self):
        self.validate_password()
        self.validate_username()
        self.validate_email()
        return self._errors

    def form_data(self):
        v = dict(self._arguments)
        if 'csrfmiddlewaretoken' in v:
            del v['csrfmiddlewaretoken']
        if 'repeat_password' in v:
            del v['repeat_password']
        return v

    def validate_password(self):
        if not re.match(FormValidator.password_regex, self._arguments['password']):
            self._errors.append(Alert('<b>%s!</b> Password is too easy.' % get_random_magic_word()))

        if 'repeat_password' in self._arguments.keys():
            if self._arguments['password'] != self._arguments['repeat_password']:
                self._errors.append(Alert('<b>%s!</b> Passwords don\'t match.' % get_random_magic_word()))

    def validate_username(self):
        if 'username' in self._arguments.keys():
            self._arguments['username'] = self._arguments['username'].strip()
            if not re.match(FormValidator.username_regex, self._arguments['username']):
                self._errors.append(Alert(
                        '<b>%s!</b> Username "%s" is not valid.' % (
                            get_random_magic_word(), self._arguments['username'])))

    def validate_email(self):
        if 'email' in self._arguments.keys():
            self._arguments['email'] = self._arguments['email'].strip()
            if not re.match(FormValidator.email_regex, self._arguments['email']):
                self._errors.append(
                        Alert('<b>%s!</b> E-mail "%s" is not valid.' % (
                            get_random_magic_word(), self._arguments['email'])))


class RegisterFormValidator(FormValidator):
    def __init__(self, **validation_kwargs):
        FormValidator.__init__(self, **validation_kwargs)

    def validate_email(self):
        FormValidator.validate_email(self)
        if 'email' in self._arguments.keys():
            if self._arguments['email'] in [x.email for x in User.objects.all()]:
                self._errors.append(
                        Alert('<b>%s!</b> User with e-mail %s already exists.' % (
                            get_random_magic_word(), self._arguments['email'])))

    def validate_username(self):
        FormValidator.validate_username(self)
        if 'username' in self._arguments.keys():
            if self._arguments['username'] in [x.username for x in User.objects.all()]:
                self._errors.append(
                        Alert('<b>%s!</b> User with username "%s" already exists.' % (
                            get_random_magic_word(), self._arguments['username'])))

    def errors(self):
        necessary_parameters = (
            self._arguments['username'], self._arguments['password'], self._arguments['repeat_password'],
            self._arguments['email'])
        if '' in necessary_parameters:
            self._errors.append(Alert('<b>%s!</b> Some of necessary fields left empty.' % get_random_magic_word()))
        FormValidator.errors(self)
        return self._errors

