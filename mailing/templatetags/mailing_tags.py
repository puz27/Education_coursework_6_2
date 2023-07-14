from django import template
register = template.Library()


@register.simple_tag(name="media_path")
def get_image_path(image_path):
    """
    Get path for images.
    :param image_path: image path from db
    :return: full image path
    """
    return f"/media/{image_path}"
