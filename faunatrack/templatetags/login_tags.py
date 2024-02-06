from django import template

register = template.Library()


@register.filter(name="to_euro")
def to_euro(value):
    return f"{value} €"

@register.filter(name="add_class")
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})