import math

from astropy import units as u
from speclite.filters import ab_reference_flux, load_filter

from galcheat import available_surveys, get_survey

speclite_survey_prefixes = {
    "DES": "decam2014-",
    "Euclid_VIS": "Euclid-",
    "HSC": "hsc2017-",
    "Rubin": "lsst2016-",
}


def calculate_zero_point(band_name, reference_mag=24):
    """Compute the zeropoint of a given filter with speclite"""
    filt = load_filter(band_name)
    filt_conv = filt.convolve_with_function(ab_reference_flux)
    filt_scaled = filt_conv * 10 ** (-0.4 * reference_mag)
    filt_units = filt_scaled.to(1 / (u.s * u.m**2))
    return filt_units


def check_zeropoints(survey_name):
    """Recompute the zeropoints with speclite and the effective area
    and compare them to their current values
    """

    if survey_name in speclite_survey_prefixes.keys():
        survey = get_survey(survey_name)
        print(survey_name, ":")

        speclite_prefix = speclite_survey_prefixes[survey_name]

        for filt_name in survey.available_filters:
            speclite_filt_name = f"{speclite_prefix}{filt_name}"
            zp_24 = (
                calculate_zero_point(speclite_filt_name)
                * survey.effective_area
                * (1 * u.s)
            )
            zp_btk = (math.log10(zp_24) + 0.4 * 24) / 0.4 * u.mag

            filt = survey.get_filter(filt_name)
            current_zp = filt.zeropoint
            print(f"  Filter {filt_name} ({speclite_filt_name} in speclite)")
            print(f"    Computed value: {zp_btk:.2f}")
            print(f"    Current value: {current_zp:.2f}")
    else:
        print(survey_name, ": filters are not available in speclite")


if __name__ == "__main__":
    for survey_name in available_surveys:
        check_zeropoints(survey_name)
