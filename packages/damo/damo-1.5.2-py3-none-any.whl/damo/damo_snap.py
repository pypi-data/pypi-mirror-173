#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

"""
Snap DAMON monitoring results.
"""

import argparse

import _damon

def set_argparser(parser):
    _damon.set_common_argparser(parser)

def main(args=None):
    if not args:
        parser = argparse.ArgumentParser()
        set_argparser(parser)
        args = parser.parse_args()

    _damon.ensure_root_permission()
    _damon.ensure_initialized(args, skip_dirs_population=True)

    if _damon.damon_interface() == 'debugfs':
        print('snap does not support debugfs interface at the moment')
        exit(1)

    if not _damon.is_damon_running():
        print('DAMON is not turned on')
        exit(1)

    # TODO: Support multiple kdamonds
    kdamonds = _damon.current_kdamonds()
    ctx = kdamonds[0].contexts[0]
    nr_schemes = len(ctx.schemes)
    scheme = _damon.Damos(name='%s' % nr_schemes,
            access_pattern = _damon.DamosAccessPattern(
                min_sz_bytes = 0,
                max_sz_bytes = _damo_schemes_input.text_to_bytes('max'),
                min_nr_accesses = 0,
                max_nr_accesses = 100,
                nr_accesses_unit = 'percent',
                min_age = 0,
                max_age = _damo_schemes_input.text_to_us('max'),
                age_unit = 'usec'),
            action = 'stat',
            quotas = _damon.DamosQuota(
                time_ms = 0,
                sz_bytes = 0,
                reset_interval_ms = _damo_schemes_input.ulong_max,
                weight_sz_permil = 0,
                weight_nr_accesses = 0,
                weight_age = 0),
            watermarks = _damon.DamosWatermarks(
                metric = _damo_schemes_input.text_to_damos_wmark_metric('none'),
                interval_us = 0,
                high = 0,
                mid = 0,
                low = 0),)
    ctx.schemes.append(scheme)
    _damon.apply_kdamonds(kdamonds)
    if _damon.update_schemes_tried_regions(kdamonds):
        print('could not update snap')




if __name__ == '__main__':
    main()
