from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings


def switch_lang_code(path, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]
    if path == "":
        raise Exception("URL path for language switch is empty")
    if path[0] != "/":
        raise Exception('URL path for language switch does not start with "/"')
    if language not in lang_codes:
        raise Exception("%s is not a supported language code" % language)
    parts = path.split("/")
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language
    return "/".join(parts)


register = template.Library()


@register.filter
def switch_i18n(request, language):
    return switch_lang_code(request.get_full_path(), language)
