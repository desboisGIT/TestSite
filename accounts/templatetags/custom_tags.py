from django import template
from accounts.models import CustomUser  # Adjust this import as per your project

register = template.Library()

@register.filter
def get_artist_rank(artist_name):
    try:
        user = CustomUser.objects.get(username=artist_name)
        return user.rank
    except CustomUser.DoesNotExist:
        return 'Unknown'
    
@register.filter
def uppercase_and_slice(value):
    if isinstance(value, str):
        return value.upper()[:9]
    return value