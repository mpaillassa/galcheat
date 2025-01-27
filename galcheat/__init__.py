r"""

  ____       _  ____ _                _
 / ___| __ _| |/ ___| |__   ___  __ _| |_
| |  _ / _` | | |   | '_ \ / _ \/ _` | __|
| |_| | (_| | | |___| | | |  __/ (_| | |_
 \____|\__,_|_|\____|_| |_|\___|\__,_|\__|

The tiny library of galaxy surveys
most useful parameters (with units)

The data can be viewed in a terminal with

    python -m galcheat

To access the quantities, retrieve the
`Survey` objects with `get_survey`.

    >>> from galcheat import get_survey
    >>> Rubin = get_survey('Rubin')
    >>> Rubin.mirror_diameter
    <Quantity 8.36 m>

Each `Survey` contains a list of filters
whose names can be obtained as

    >>> Rubin.available_filters

Each `Filter` class is then accessible either
as an attribute from the `Survey`

    >>> u_filter = Rubin.filters.u

or through a method

    >>> u_filter = Rubin.get_filter('u')

For a given survey, a dictionary of the available
filters is returned by

    >>> Rubin.get_filters()

Parameter values can be converted to any physical
units using the `astropy.units` scheme

    >>> u_filter.psf_fwhm
    <Quantity 0.859 arcsec>
    >>> u_filter.value
    0.859

    >>> import astropy.units as u
    >>> u_filter.psf_fwhm.to(u.arcmin).value
or
    >>> u_filter.psf_fwhm.to_value(u.arcmin)
    0.014316666666666667

Feel free to contribute by submitting
parameter values for your surveys of
interest or reporting unconsitent
values.

"""
from pathlib import Path

from galcheat.survey import Survey

__all__ = ["available_surveys", "get_filter", "get_survey"]

_BASEDIR = Path(__file__).parent.resolve()
_survey_info = {
    path.stem: Survey.from_yaml(path) for path in _BASEDIR.glob("data/*.yaml")
}

from galcheat.helpers import available_surveys, get_filter, get_survey  # noqa
