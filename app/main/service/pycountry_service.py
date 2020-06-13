import pycountry


def country_lookup(country_name):
    result = pycountry.countries.lookup(country_name)
    return None if result is None else result.alpha_2


