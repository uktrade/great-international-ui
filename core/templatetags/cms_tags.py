import re
import dateparser

from bs4 import BeautifulSoup

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.text import slugify
from django.utils import translation


register = template.Library()


def build_anchor_id(element):
    return slugify(get_label(element) + '-section')


def get_label(element):
    return re.sub(r'^.* \- ', '', element.contents[0])


@register.filter
def add_anchors(value):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('h2'):
        element.attrs['id'] = build_anchor_id(element)
    return str(soup)


@register.filter
def table_of_contents(value):
    soup = BeautifulSoup(value, 'html.parser')
    return [
        (build_anchor_id(element), get_label(element))
        for element in soup.findAll('h2')
    ]


@register.filter
def first_paragraph(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('p')
    return str(element)


@register.filter
def first_image(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('img')
    if not element:
        return ''
    del element['height']
    return element


@register.filter
def grouper(value, n):
    ungrouped = value or []
    return [ungrouped[x:x+n] for x in range(0, len(ungrouped), n)]


@register.filter
def add_href_target(value, request):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('a', attrs={'href': re.compile("^http")}):
        if request.META['HTTP_HOST'] not in element.attrs['href']:
            element.attrs['target'] = '_blank'
    return str(soup)


@register.filter
def filter_by_active_language(pages):
    if pages:
        return [page for page in pages if is_translated_to_current_language(page)]
    return []


def is_translated_to_current_language(page):
    active_language = translation.get_language()
    for code, _ in page['meta']['languages']:
        if code == active_language:
            return True
    else:
        return False


@register.filter(is_safe=True)
@stringfilter
def title_from_heading(heading):
    if ':' in heading:
        return heading.split(':')[0].strip()
    # full width character used in ja and zh
    if '：' in heading:
        return heading.split('：')[0].strip()
    return heading


@register.filter
def parse_date(date_string):
    if date_string:
        return dateparser.parse(date_string).strftime('%d %B %Y')
    return None


def get_image_url(context, image_name):
    try:
        return context['page'][image_name]['url']
    except (KeyError, TypeError):
        return None


@register.inclusion_tag('directory_components/hero.html', takes_context=True)
def cms_hero(context, hero_text, hero_subheading=None):
    return {
        'hero_text': hero_text,
        'hero_subheading': hero_subheading,
        'image': get_image_url(context, 'hero_image'),
    }


@register.inclusion_tag('directory_components/hero_with_cta.html', takes_context=True)
def cms_hero_with_cta(context, heading, subheading=None, subtitle=None, cta_text=None, cta_link=None):
    return {
        'heading': heading,
        'subheading': subheading,
        'subtitle': subtitle,
        'cta_text': cta_text,
        'cta_link': cta_link,
        'image': get_image_url(context, 'hero_image'),
    }
