# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Identity, MapCompose


def str_to_num(number_str: str):
    try:
        int_number = int(number_str.replace("\xa0", ""))
    except ValueError:
        int_number = None
    return int_number


def list_to_str(maybe_list: list):
    result = ''
    for itm in maybe_list:
        itm.replace('\xa0', '')
        result += itm
    return result.strip()


def get_salary(salary_str: list, loader_context):
    salary_dict = dict.fromkeys(['min_salary', 'max_salary'])
    amounts = sorted([amt for amt in map(str_to_num, salary_str) if amt is not None])
    if len(amounts) > 0:
        first_str = salary_str[0].strip().lower()
        if first_str == 'от':
            salary_dict['min_salary'] = amounts[0]
        elif first_str == 'до':
            salary_dict['max_salary'] = amounts[0]
    if len(amounts) > 1:
        salary_dict['max_salary'] = amounts[1]
    return salary_dict


def get_business_lines(lines_str):
    if lines_str is not None:
        return [line.strip() for line in list_to_str(lines_str).split(',')]
    else:
        return []


def get_title(title_str):
    return list_to_str(title_str).removeprefix('Вакансии компании').strip()


def get_full_url(url: str, loader_context):
    a = 1
    b = loader_context.get('response')
    return loader_context.get('response').urljoin(url)


class EmployerItem(Item):
    title = Field()
    url = Field()
    business_line = Field()
    description = Field()


class EmployerLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    business_line_out = get_business_lines
    title_out = get_title
    description_out = Identity()


class VacancyItem(Item):
    title = Field()
    employer_url = Field()
    skills = Field()
    salary = Field()
    url = Field()


class VacancyLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    skills_out = Identity()
    salary_out = get_salary
    employer_url_in = MapCompose(get_full_url)
