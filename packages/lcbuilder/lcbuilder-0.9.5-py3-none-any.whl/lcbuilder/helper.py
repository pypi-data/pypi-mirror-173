import numpy as np
from foldedleastsquares import DefaultTransitTemplateGenerator
from lcbuilder import constants


class LcbuilderHelper:
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def calculate_period_grid(time, min_period, max_period, oversampling, star_info, transits_min_count,
                              max_oversampling=15):
        time_span_curve = time[-1] - time[0]
        dif = time[1:] - time[:-1]
        jumps = np.where(dif > 1)[0]
        jumps = np.append(jumps, len(time) - 1)
        previous_jump_index = 0
        time_span_all_sectors = 0
        empty_days = 0
        for jumpIndex in jumps[0:-1]:
            empty_days = empty_days + time[jumpIndex + 1] - time[jumpIndex - 1]
        if oversampling is None:
            oversampling = int(1 / ((time_span_curve - empty_days) / time_span_curve))
            oversampling = oversampling if oversampling < max_oversampling else max_oversampling
            oversampling = oversampling if oversampling > 3 else 3
        for jumpIndex in jumps:
            time_chunk = time[
                         previous_jump_index + 1:jumpIndex]  # ignoring first measurement as could be the last from the previous chunk
            if len(time_chunk) > 0:
                time_span_all_sectors = time_span_all_sectors + (time_chunk[-1] - time_chunk[0])
            previous_jump_index = jumpIndex
        return DefaultTransitTemplateGenerator() \
                   .period_grid(star_info.radius, star_info.mass, time_span_curve, min_period,
                                max_period, oversampling, transits_min_count, time_span_curve), oversampling

    @staticmethod
    def compute_cadence(time):
        cadence_array = np.diff(time) * 24 * 60 * 60
        cadence_array = cadence_array[~np.isnan(cadence_array)]
        cadence_array = cadence_array[cadence_array > 0]
        return int(np.round(np.nanmedian(cadence_array)))

    @staticmethod
    def estimate_transit_cadences(cadence_s, duration_d):
        cadence = cadence_s / 3600 / 24
        return duration_d // cadence

    @staticmethod
    def mission_lightkurve_sector_extraction(mission, lightkurve_item):
        sector_name = None
        sector = None
        if mission == constants.MISSION_TESS:
            sector = lightkurve_item.sector
            sector_name = 'sector'
        elif mission == constants.MISSION_KEPLER:
            sector = lightkurve_item.quarter
            sector_name = 'quarter'
        elif mission == constants.MISSION_K2:
            sector = lightkurve_item.campaign
            sector_name = 'campaign'
        return sector_name, sector

    @staticmethod
    def mission_pixel_size(mission):
        px_size_arcs = None
        if mission == constants.MISSION_TESS:
            px_size_arcs = 20.25
        elif mission == constants.MISSION_KEPLER:
            px_size_arcs = 4
        elif mission == constants.MISSION_K2:
            px_size_arcs = 4
        return px_size_arcs
