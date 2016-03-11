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
        return '''
            <h1 class="page-header">
                {name}
            </h1>
            <form method="{method}" action="{action}" role="form">
            {csrf}
            {fields}
            </form>
        '''.format(
            {'csrf': '{% csrf_token %}', 'name': self.name, 'method': self.method, 'fields': ''.join(self.fields)})
