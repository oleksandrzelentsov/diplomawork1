class Field:
    """Class that represents the Field widget for custom forms."""

    def __init__(self, name: str, input_type="text", required=False, return_=True):
        self.required = required
        self.input_type = input_type
        self.name = name
        self.return_ = return_

    def __str__(self):
        s = """
        <div class="row">
            <div class="col-xs-6 col-sm-6 col-md-4 col-lg-2">
                <div class="form-group">
        """
        s += str.format('<label for="{0}_">', self.name.lower())
        if self.required:
            s += '<span class="glyphicon glyphicon-asterisk" style="color:red;"></span> ' + self.name.capitalize()
        else:
            s += self.name.capitalize()

        s += "</label>"

        if self.return_:
            if self.input_type == 'textarea':
                s += str.format("""{% if {0} %}
                    <textarea rows="5" class="form-control" name="{0}" id="{0}_" value="{{ {0} }}" />
                    {% else %}
                    <textarea rows="5" class="form-control" name="{0}" id="{0}_" />
                    {% endif %}""", self.name.lower(), self.input_type)
            else:
                s += str.format("""{% if {0} %}
                    <input type="{1}" class="form-control" name="{0}" id="{0}_" value="{{ {0} }}" />
                    {% else %}
                    <input type="{1}" class="form-control" name="{0}" id="{0}_" />
                    {% endif %}""", self.name.lower(), self.input_type)
        else:
            if self.input_type == 'textarea':
                s += str.format('<textarea rows="5" class="form-control" name="{0}" id="{0}_"/>', self.name.lower())
            else:
                s += str.format('<input type="{1}" class="form-control" name="{0}" id="{0}_" />', self.name.lower())

        s += """</div>
            </div>
        </div>"""

        return s


class Form:
    def __init__(self, name, method, action):
        self.name = name
        self.method = method
        self.action = action
        self.fields = []

    def add_field(self, field_: Field):
        self.fields.append(field_)

    def __str__(self):
        return str.format('''
            <h1 class="page-header">
                {name}
            </h1>
            <form method="{method}" action="{action}" role="form">
            {% csrf_token %}
            {fields}
            </form>
        ''', {'name': self.name, 'method': self.method, 'fields': ''.join(self.fields)})


template = ''

extend_ = input('type something if you want your template to extend from something ')

if extend_:
    extend_ = input('type base template: ')
    template += "{}{}{}".format('{% extends "', extend_, '" %}')


def forms():
    form = Form(input('type form name: '), input('type form method: '), input('type form action: '))
    field = input('do you want a field? ')
    while field:
        field = Field(input('type field\'s name: '), input('type the field type: '),
                      True if input('type smth if field is required ') else False,
                      True if input('type smth if field should save its value on form send') else False)
        form.add_field(field)
        field = input('do you want one more field? ')
    global template
    template += str.format('{a}<div class="container">{form}</div>{b}',
                           {'form': form, 'a': '{% block main_content %}', 'b': '{% endblock %}'})


def block():
    global template
    template += "{}{}{}".format('%s%s%s' % ('{% block ', input('type the blockname: '), ' %}'), input('type the content: \n'), '{% endblock %}')


def blocks():
    t = input('type smth if you want any blocks')
    while t:
        t = input('type block name: ')
        if t == 'form':
            forms()
        else:
            block()
        t = input('type smth if you want any blocks')

blocks()

filename = input('type filename: ')

with open(filename) as f:
    f.write(template)

print(template)