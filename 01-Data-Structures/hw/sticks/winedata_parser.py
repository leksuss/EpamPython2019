from collections import namedtuple

print("Welcome to Epam Collect Statistics 2019!")
print("Please sit back and relax while this script works on your computer.")
print("It takes about 8-15 seconds depend on your CPU speed.")

# you must construct additional p̶y̶l̶o̶n̶s̶ structures!
# set data structure for variety statistics
varieties = {
    'Gewürztraminer',
    'Riesling',
    'Merlot',
    'Madera',
    'Tempranillo',
    'Red Blend'
}
var_stat = {}
for variety in varieties:
    var_stat[variety] = {
        'average_price': [],
        'min_price': 10e6,
        'max_price': 0,
        'most_common_region': {},
        'most_common_country': {},
        'average_score': [],
        'count': 0
    }

# set data structure for global statistics
glob_stat = {
    'most_expensive_wine': {'price': 0},
    'cheapest_wine': {'price': 10e6},
    'highest_score': {'points': 0},
    'lowest_score': {'points': 100},
    'most_expensive_coutry': {'price': 0},
    'cheapest_coutry': {'price': 10e6},
    'most_rated_country': {'points': 0},
    'underrated_country': {'points': 100},
    'tasters': {}
}

# set named tuple for object
wines = set()
Wine = namedtuple('Wine', [
    'points', 'title', 'description', 'taster_name',
    'taster_twitter_handle', 'price', 'designation',
    'variety', 'region_1', 'region_2', 'province', 'country', 'winery'
])

'''
3. Найти для каждого из сортов
`Gew[üu]rztraminer, Riesling, Merlot, Madera, Tempranillo, Red Blend`
 следующую информацию:
   * `average_price`
   * `min_price`
   * `max_price`
   * `most_common_region` где больше всего вин этого сорта производят ?
   * `most_common_country`
   * `avarage_score`

Для всех объектов:
   * `most_expensive_wine` в случае коллизий тут и далее делаем список.[]
   * `cheapest_wine`[]
   * `highest_score`[]
   * `lowest_score`[]
   * `most_expensive_coutry` в среднем самое дорогое вино среди стран
   * `cheapest_coutry` в среднем самое дешевое вино среди стран
   * `most_rated_country`
   * `underrated_country`
   * `most_active_commentator`
'''

# set source and result files
source_data_files = ['winedata_1.json', 'winedata_2.json']
result_files = {
    'markdown': 'README.md',
    'md_template': 'template.md',
    'winedata': 'winedata_full.json',
    'stats': 'stats.json'
}

# read files and get unique objects
raw_items = set()
for data_file in source_data_files:
    with open(data_file, 'r') as f:
        raw_file = f.read()
        raw_file_items = set(raw_file[2:-2].split('}, {'))
        raw_items.update(raw_file_items)

# parse object and get key-value pair
for raw_item in raw_items:
    wine_values = []
    for raw_property_line in raw_item.strip().split(', "'):
        raw_property = raw_property_line.strip().split('": ')
        key = raw_property[0].strip('" ')
        value = raw_property[1].strip('" ')
        # convert \u00xx sequence to UTF char.
        value = value.encode('utf-8').decode('unicode_escape')
        # processing str->int and null values
        if value == 'null':
            value = ''
        if value and key in ['price', 'points']:
            value = int(value)
        wine_values.append(value)

    # collect all object properties in named tuple
    wine = Wine(*wine_values)

    # calculate varieties statistics
    if wine.variety in varieties:
        if wine.price:
            var_stat[wine.variety]['average_price'].append(wine.price)
            var_stat[wine.variety]['average_score'].append(wine.points)
            var_stat[wine.variety]['count'] += 1

            # min-max price
            if var_stat[wine.variety]['max_price'] < wine.price:
                var_stat[wine.variety]['max_price'] = wine.price
            if var_stat[wine.variety]['min_price'] > wine.price:
                var_stat[wine.variety]['min_price'] = wine.price

        # most common regions
        if wine.region_1:
            if wine.region_1 not in \
                    var_stat[wine.variety]['most_common_region']:
                var_stat[wine.variety]['most_common_region'][wine.region_1] = 0
            var_stat[wine.variety]['most_common_region'][wine.region_1] += 1
        if wine.region_2:
            if wine.region_2 not in \
                    var_stat[wine.variety]['most_common_region']:
                var_stat[wine.variety]['most_common_region'][wine.region_2] = 0
            var_stat[wine.variety]['most_common_region'][wine.region_2] += 1

        # most common country
        if wine.country:
            if wine.country not in \
                    var_stat[wine.variety]['most_common_country']:
                var_stat[wine.variety]['most_common_country'][wine.country] = 0
            var_stat[wine.variety]['most_common_country'][wine.country] += 1

    # calculate global statistics
    if wine.price:
        # most expensive wine
        if wine.price > glob_stat['most_expensive_wine']['price']:
            glob_stat['most_expensive_wine']['price'] = wine.price
            glob_stat['most_expensive_wine']['items'] = {wine.title}
        elif wine.price == glob_stat['most_expensive_wine']['price']:
            glob_stat['most_expensive_wine']['items'].add(wine.title)
        # cheapest wine
        if wine.price < glob_stat['cheapest_wine']['price']:
            glob_stat['cheapest_wine']['price'] = wine.price
            glob_stat['cheapest_wine']['items'] = {wine.title}
        elif wine.price == glob_stat['cheapest_wine']['price']:
            glob_stat['cheapest_wine']['items'].add(wine.title)

        if wine.country:
            # most expensive country
            if wine.price > glob_stat['most_expensive_coutry']['price']:
                glob_stat['most_expensive_coutry']['price'] = wine.price
                glob_stat['most_expensive_coutry']['items'] = {wine.country}
            elif wine.price == glob_stat['most_expensive_coutry']['price']:
                glob_stat['most_expensive_coutry']['items'].add(wine.country)
            # cheapest country
            if wine.price < glob_stat['cheapest_coutry']['price']:
                glob_stat['cheapest_coutry']['price'] = wine.price
                glob_stat['cheapest_coutry']['items'] = {wine.country}
            elif wine.price == glob_stat['cheapest_coutry']['price']:
                glob_stat['cheapest_coutry']['items'].add(wine.country)

    if wine.country:
        # most rated country
        if wine.points > glob_stat['most_rated_country']['points']:
            glob_stat['most_rated_country']['points'] = wine.points
            glob_stat['most_rated_country']['items'] = {wine.country}
        elif wine.points == glob_stat['most_rated_country']['points']:
            glob_stat['most_rated_country']['items'].add(wine.country)
        # underrated country
        if wine.points < glob_stat['underrated_country']['points']:
            glob_stat['underrated_country']['points'] = wine.points
            glob_stat['underrated_country']['items'] = {wine.country}
        elif wine.points == glob_stat['underrated_country']['points']:
            glob_stat['underrated_country']['items'].add(wine.country)

    # highest score
    if wine.points > glob_stat['highest_score']['points']:
        glob_stat['highest_score']['points'] = wine.points
        glob_stat['highest_score']['items'] = {wine.title}
    elif wine.points == glob_stat['highest_score']['points']:
        glob_stat['highest_score']['items'].add(wine.title)

    # lowest_score
    if wine.points < glob_stat['lowest_score']['points']:
        glob_stat['lowest_score']['points'] = wine.points
        glob_stat['lowest_score']['items'] = {wine.title}
    elif wine.points == glob_stat['lowest_score']['points']:
        glob_stat['lowest_score']['items'].add(wine.title)

    # most_active_commentator
    if wine.taster_name:
        if wine.taster_name not in glob_stat['tasters']:
            glob_stat['tasters'][wine.taster_name] = 0
        glob_stat['tasters'][wine.taster_name] += 1

    wines.add(wine)
    len_wines = len(wines)

print(f"Found {len_wines} unique records")

# set structures for storing data for json and markdown formats
var_stat_json = []
var_stat_md = '''
| Variety | Av price | Min Price | Max Price | Region | Country | Av Score |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |\n'''
# process intermediate variety stat to finished
for variety in sorted(var_stat):
    # for json file
    if not var_stat[variety]['count']:
        print(f'Sorry, there is no variety "{variety}" in the collection')
        continue
    var_average_price = round(sum(
        var_stat[variety]['average_price']) / var_stat[variety]['count'], 2)
    var_average_score = round(sum(
        var_stat[variety]['average_score']) / var_stat[variety]['count'], 2)
    var_region = max(var_stat[variety]['most_common_region'],
                     key=var_stat[variety]['most_common_region'].get)
    var_country = max(var_stat[variety]['most_common_country'],
                      key=var_stat[variety]['most_common_country'].get)
    var_max_price = var_stat[variety]['max_price']
    var_min_price = var_stat[variety]['min_price']

    var_stat_json.append(f"""
        "{variety}": {{
            "average_price": {var_average_price},
            "min_price": {var_min_price},
            "max_price": {var_max_price},
            "most_common_region": "{var_region}",
            "most_common_country": "{var_country}",
            "average_score": "{var_average_score}"
        }}""")
    # for markdown file
    var_stat_md += f"| {variety} | {var_average_price} | " + \
                    f"{var_min_price} | {var_max_price} | " + \
                    f"{var_region} | {var_country} | {var_average_score} |\n"

# most active commentator(s)
max_comm = max(glob_stat['tasters'].values())
list_comm = [k for k, v in glob_stat['tasters'].items() if v == max_comm]


def to_str_json(s):
    if len(s) > 1:
        return '[\n        "' + '",\n        "'.join(s) + '"\n    ]'
    else:
        return '"' + next(iter(s)) + '"'


# for json file
glob_stat_json = f"""
    "most_expensive_wine": {
    to_str_json(glob_stat['most_expensive_wine']['items'])},
    "cheapest_wine": {
    to_str_json(glob_stat['cheapest_wine']['items'])},
    "highest_score": {
    to_str_json(glob_stat['highest_score']['items'])},
    "lowest_score": {
    to_str_json(glob_stat['lowest_score']['items'])},
    "most_expensive_coutry": {
    to_str_json(glob_stat['most_expensive_coutry']['items'])},
    "cheapest_coutry": {
    to_str_json(glob_stat['cheapest_coutry']['items'])},
    "most_rated_country": {
    to_str_json(glob_stat['most_rated_country']['items'])},
    "underrated_country": {
    to_str_json(glob_stat['underrated_country']['items'])},
    "most_active_commentator": {
    to_str_json(list_comm)}
"""


def to_str_md(s):
    if len(s) > 1:
        return ' - ' + '\n - '.join(s) + '\n'
    else:
        return ' - ' + next(iter(s)) + '\n'


# for markdown file
glob_stat_md = f"""
Most expensive wine (price = {glob_stat['most_expensive_wine']['price']}):
{to_str_md(glob_stat['most_expensive_wine']['items'])}
Cheapest wine (price = {glob_stat['cheapest_wine']['price']}):
{to_str_md(glob_stat['cheapest_wine']['items'])}
Highest score (score = {glob_stat['highest_score']['points']}):
{to_str_md(glob_stat['highest_score']['items'])}
Lowest score (score = {glob_stat['lowest_score']['points']}):
{to_str_md(glob_stat['lowest_score']['items'])}
Most expensive country (price = {glob_stat['most_expensive_coutry']['price']}):
{to_str_md(glob_stat['most_expensive_coutry']['items'])}
Cheapest country (price = {glob_stat['cheapest_coutry']['price']}):
{to_str_md(glob_stat['cheapest_coutry']['items'])}
Most rated country (score = {glob_stat['most_rated_country']['points']}):
{to_str_md(glob_stat['most_rated_country']['items'])}
Underrated country (score = {glob_stat['underrated_country']['points']}):
{to_str_md(glob_stat['underrated_country']['items'])}
Most active commentator (tasted {max_comm} times):
{to_str_md(list_comm)}"""

# write results to md file
with open(result_files['md_template'], 'r') as md_file:
    md_content = md_file.read()
    md_content = md_content.replace('{glob_stat_md}', glob_stat_md)
    md_content = md_content.replace('{var_stat_md}', var_stat_md)
with open(result_files['markdown'], 'w') as md_file:
    md_file.write(md_content)
print(result_files['md_template'], "file completed")

# write results to json file
stat_json_string = f"""{{"statistics": {{
    "wine": {{{','.join(var_stat_json)}
    }},{glob_stat_json}  }}
}}"""

with open(result_files['stats'], 'w') as stat_json_file:
    stat_json_file.write(stat_json_string)
print(result_files['stats'], "file completed")

# sort all list of objects
list_wines = list(wines)
list_wines.sort(key=lambda wine: wine.variety)
list_wines.sort(key=lambda wine: int(wine.price) if wine.price else 0,
                reverse=True)

counter = 1
full_json_str = '['
for wine in list_wines:
    attr_json_str = ''
    for name in wine._fields:
        value = getattr(wine, name)
        if value:
            if name not in ['price', 'points']:
                value = f'"{value}"'
            else:
                value = str(value)
        else:
            value = 'null'
        value += ',' if name != 'winery' else ''
        attr_json_str += f"""
    "{name}": {value}"""
    full_json_str += f"""{{{attr_json_str}
}}{',' if counter != len_wines else ']'}
"""
    counter += 1

with open(result_files['winedata'], 'w') as full_json_file:
    full_json_file.write(full_json_str)
print(result_files['winedata'], "file completed")
