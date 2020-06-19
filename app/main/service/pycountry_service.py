import pycountry


def country_to_isocode(country_name):
    try:
        result = pycountry.countries.lookup(country_name)
    except LookupError:
        return None
    else:
        return result.alpha_2


