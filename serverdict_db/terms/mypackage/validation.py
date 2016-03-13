import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from serverdict_db.settings import ADMIN_EMAIL
from terms.mypackage.html_helper import Alert, get_random_magic_word


class FormValidator:
    email_regex = r'[^@]+@[^@]+\.[^@]+'
    password_regex = r'.{8,32}'
    username_regex = r'[a-zA-Z_-]'

    def __init__(self, remove_lists=True, **validation_kwargs):
        self._arguments = validation_kwargs
        self._errors = []
        if remove_lists:
            for k, v in self._arguments.items():
                if isinstance(v, list):
                    self._arguments[k] = v[0]
        self.format_args()

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

    def format_args(self):
        if 'username' in self._arguments.keys():
            self._arguments['username'] = self._arguments['username'].strip().lower()
        if 'email' in self._arguments.keys():
            self._arguments['email'] = self._arguments['email'].strip().lower()
        if 'first_name' in self._arguments.keys():
            self._arguments['first_name'] = self._arguments['first_name'].strip().capitalize()
        if 'last_name' in self._arguments.keys():
            self._arguments['last_name'] = self._arguments['last_name'].strip().capitalize()


class RegisterFormValidator(FormValidator):
    def validate_email(self):
        super().validate_email()
        if 'email' in self._arguments.keys():
            if self._arguments['email'] in [x.email for x in User.objects.all()]:
                self._errors.append(
                    Alert('<b>%s!</b> User with e-mail %s already exists.' % (
                        get_random_magic_word(), self._arguments['email'])))

    def validate_username(self):
        super().validate_username()
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
        super().errors()
        return self._errors


class LoginFormValidator(FormValidator):
    def __init__(self, **validation_kwargs):
        super().__init__(remove_lists=True, **validation_kwargs)
        self.user = authenticate(username=self.form_data()['username'], password=self.form_data()['password'])

    def validate_user(self):
        # user = authenticate(username=self._arguments['username'], password=self._arguments['password'])
        if self.user is None:
            # return the same page with errors if no
            self._errors.append(
                Alert('<b>%s!</b> Wrong authentication data.' % (get_random_magic_word()), 'danger'))
        elif not self.user.is_active:
            msg = Alert(
                '<b>%s! Sorry!</b> This user is disabled. Contact <a href="mailto:%s">' % (
                    get_random_magic_word(), ADMIN_EMAIL) +
                'admin</a> to resolve this issue.')
            self._errors.append(msg)

    def errors(self):
        super().errors()
        self.validate_user()
        return self._errors


class AddTermFormValidator(FormValidator):
    max_term_name_length = 128
    min_term_name_length = 8

    def format_args(self):
        if 'term_name' in self._arguments.keys():
            self._arguments['term_name'] = self._arguments['term_name'].strip()
        if 'definition' in self._arguments.keys():
            self._arguments['definition'] = self._arguments['definition'].strip()
        if 'author' in self._arguments.keys():
            self._arguments['author'] = self._arguments['author'].strip().capitalize()

    def validate_term_name(self):
        if 'term_name' in self._arguments.keys():
            if not (AddTermFormValidator.min_term_name_length >= len(
                    self._arguments['term_name']) >= AddTermFormValidator.min_term_name_length):
                msg = '<b>%s!</b> Term name should be from %i to %i characters long.' % (
                    get_random_magic_word(), AddTermFormValidator.min_term_name_length,
                    AddTermFormValidator.max_term_name_length)
                self._errors.append(Alert(msg))

    # def validate_definition(self):
    #     if 'definition' in self._arguments.keys():
    # TODO validate definition, author and year

    def errors(self):
        self.validate_term_name()
        return self._errors
