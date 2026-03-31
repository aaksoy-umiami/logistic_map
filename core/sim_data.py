# This is pre-calculated predictability limit data in the shape of: metric,r_value,model_bias,ic_bias
# It is then loaded in the main app

import numpy as np

# Pre-calculated 4D surface (median, mean, mode)

PRECALC_SURFACE_MEDIAN = np.array([
    [np.int64(90), np.int64(79), np.int64(73), np.int64(69), np.int64(63), np.int64(57), np.int64(51), np.int64(42), np.int64(31), np.int64(17), np.int64(11)],  # r=3.70, Δr=0.0e+00
    [np.int64(73), np.int64(73), np.int64(73), np.int64(69), np.int64(63), np.int64(57), np.int64(53), np.int64(42), np.int64(26), np.int64(17), np.int64(11)],  # r=3.70, Δr=1.0e-10
    [np.int64(57), np.int64(57), np.int64(57), np.int64(57), np.int64(57), np.int64(59), np.int64(53), np.int64(42), np.int64(26), np.int64(17), np.int64(11)],  # r=3.70, Δr=3.2e-08
    [np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(42), np.int64(31), np.int64(17), np.int64(11)],  # r=3.70, Δr=1.0e-05
    [np.int64(71), np.int64(67), np.int64(62), np.int64(56), np.int64(52), np.int64(46), np.int64(43), np.int64(37), np.int64(27), np.int64(21), np.int64(17)],  # r=3.75, Δr=0.0e+00
    [np.int64(57), np.int64(57), np.int64(58), np.int64(56), np.int64(52), np.int64(48), np.int64(43), np.int64(37), np.int64(27), np.int64(21), np.int64(17)],  # r=3.75, Δr=1.0e-10
    [np.int64(46), np.int64(46), np.int64(46), np.int64(46), np.int64(46), np.int64(46), np.int64(43), np.int64(37), np.int64(28), np.int64(21), np.int64(17)],  # r=3.75, Δr=3.2e-08
    [np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(36), np.int64(28), np.int64(21), np.int64(17)],  # r=3.75, Δr=1.0e-05
    [np.int64(67), np.int64(63), np.int64(56), np.int64(52), np.int64(47), np.int64(40), np.int64(35), np.int64(27), np.int64(24), np.int64(17), np.int64(11)],  # r=3.80, Δr=0.0e+00
    [np.int64(61), np.int64(62), np.int64(57), np.int64(52), np.int64(47), np.int64(42), np.int64(35), np.int64(27), np.int64(23), np.int64(17), np.int64(11)],  # r=3.80, Δr=1.0e-10
    [np.int64(47), np.int64(47), np.int64(47), np.int64(47), np.int64(47), np.int64(40), np.int64(35), np.int64(27), np.int64(24), np.int64(17), np.int64(12)],  # r=3.80, Δr=3.2e-08
    [np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(27), np.int64(25), np.int64(17), np.int64(10)],  # r=3.80, Δr=1.0e-05
    [np.int64(1000), np.int64(1000), np.int64(49), np.int64(41), np.int64(37), np.int64(31), np.int64(28), np.int64(24), np.int64(21), np.int64(16), np.int64(10)],  # r=3.85, Δr=0.0e+00
    [np.int64(1000), np.int64(1000), np.int64(46), np.int64(41), np.int64(37), np.int64(31), np.int64(28), np.int64(24), np.int64(19), np.int64(16), np.int64(10)],  # r=3.85, Δr=1.0e-10
    [np.int64(37), np.int64(37), np.int64(37), np.int64(37), np.int64(37), np.int64(31), np.int64(28), np.int64(24), np.int64(22), np.int64(16), np.int64(10)],  # r=3.85, Δr=3.2e-08
    [np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(21), np.int64(16), np.int64(10)],  # r=3.85, Δr=1.0e-05
    [np.int64(62), np.int64(57), np.int64(53), np.int64(45), np.int64(33), np.int64(28), np.int64(24), np.int64(20), np.int64(17), np.int64(14), np.int64(9)],  # r=3.90, Δr=0.0e+00
    [np.int64(49), np.int64(49), np.int64(49), np.int64(45), np.int64(33), np.int64(28), np.int64(24), np.int64(20), np.int64(17), np.int64(14), np.int64(8)],  # r=3.90, Δr=1.0e-10
    [np.int64(30), np.int64(30), np.int64(30), np.int64(30), np.int64(30), np.int64(28), np.int64(24), np.int64(20), np.int64(17), np.int64(14), np.int64(8)],  # r=3.90, Δr=3.2e-08
    [np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(16), np.int64(14), np.int64(7)],  # r=3.90, Δr=1.0e-05
]).reshape(5, 4, 11)

PRECALC_SURFACE_MEAN = np.array([
    [np.int64(88), np.int64(79), np.int64(73), np.int64(69), np.int64(63), np.int64(57), np.int64(50), np.int64(39), np.int64(26), np.int64(17), np.int64(11)],  # r=3.70, Δr=0.0e+00
    [np.int64(73), np.int64(71), np.int64(73), np.int64(67), np.int64(63), np.int64(57), np.int64(50), np.int64(41), np.int64(26), np.int64(17), np.int64(11)],  # r=3.70, Δr=1.0e-10
    [np.int64(57), np.int64(57), np.int64(57), np.int64(57), np.int64(57), np.int64(57), np.int64(50), np.int64(41), np.int64(24), np.int64(17), np.int64(11)],  # r=3.70, Δr=3.2e-08
    [np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(50), np.int64(41), np.int64(26), np.int64(17), np.int64(11)],  # r=3.70, Δr=1.0e-05
    [np.int64(71), np.int64(66), np.int64(62), np.int64(56), np.int64(52), np.int64(46), np.int64(41), np.int64(36), np.int64(27), np.int64(21), np.int64(17)],  # r=3.75, Δr=0.0e+00
    [np.int64(57), np.int64(57), np.int64(57), np.int64(56), np.int64(52), np.int64(46), np.int64(43), np.int64(37), np.int64(26), np.int64(21), np.int64(17)],  # r=3.75, Δr=1.0e-10
    [np.int64(46), np.int64(46), np.int64(46), np.int64(46), np.int64(46), np.int64(46), np.int64(41), np.int64(36), np.int64(26), np.int64(21), np.int64(17)],  # r=3.75, Δr=3.2e-08
    [np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(27), np.int64(21), np.int64(17)],  # r=3.75, Δr=1.0e-05
    [np.int64(67), np.int64(62), np.int64(56), np.int64(51), np.int64(46), np.int64(39), np.int64(34), np.int64(27), np.int64(22), np.int64(16), np.int64(10)],  # r=3.80, Δr=0.0e+00
    [np.int64(61), np.int64(61), np.int64(57), np.int64(51), np.int64(45), np.int64(39), np.int64(34), np.int64(27), np.int64(22), np.int64(16), np.int64(10)],  # r=3.80, Δr=1.0e-10
    [np.int64(47), np.int64(47), np.int64(47), np.int64(47), np.int64(45), np.int64(39), np.int64(34), np.int64(27), np.int64(21), np.int64(16), np.int64(10)],  # r=3.80, Δr=3.2e-08
    [np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(27), np.int64(22), np.int64(16), np.int64(10)],  # r=3.80, Δr=1.0e-05
    [np.int64(1000), np.int64(57), np.int64(46), np.int64(41), np.int64(36), np.int64(31), np.int64(27), np.int64(24), np.int64(19), np.int64(13), np.int64(8)],  # r=3.85, Δr=0.0e+00
    [np.int64(1000), np.int64(1000), np.int64(45), np.int64(41), np.int64(37), np.int64(31), np.int64(27), np.int64(24), np.int64(21), np.int64(15), np.int64(8)],  # r=3.85, Δr=1.0e-10
    [np.int64(37), np.int64(37), np.int64(37), np.int64(37), np.int64(36), np.int64(31), np.int64(28), np.int64(24), np.int64(19), np.int64(13), np.int64(9)],  # r=3.85, Δr=3.2e-08
    [np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(19), np.int64(15), np.int64(8)],  # r=3.85, Δr=1.0e-05
    [np.int64(60), np.int64(54), np.int64(51), np.int64(41), np.int64(32), np.int64(28), np.int64(24), np.int64(20), np.int64(17), np.int64(14), np.int64(8)],  # r=3.90, Δr=0.0e+00
    [np.int64(49), np.int64(49), np.int64(48), np.int64(40), np.int64(32), np.int64(28), np.int64(24), np.int64(20), np.int64(16), np.int64(12), np.int64(8)],  # r=3.90, Δr=1.0e-10
    [np.int64(30), np.int64(30), np.int64(30), np.int64(30), np.int64(30), np.int64(28), np.int64(24), np.int64(20), np.int64(17), np.int64(14), np.int64(8)],  # r=3.90, Δr=3.2e-08
    [np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(17), np.int64(12), np.int64(8)],  # r=3.90, Δr=1.0e-05
]).reshape(5, 4, 11)

PRECALC_SURFACE_MODE = np.array([
    [np.int64(90), np.int64(82), np.int64(79), np.int64(73), np.int64(67), np.int64(57), np.int64(58), np.int64(50), np.int64(33), np.int64(17), np.int64(17)],  # r=3.70, Δr=0.0e+00
    [np.int64(73), np.int64(73), np.int64(71), np.int64(75), np.int64(63), np.int64(57), np.int64(53), np.int64(49), np.int64(31), np.int64(17), np.int64(11)],  # r=3.70, Δr=1.0e-10
    [np.int64(57), np.int64(57), np.int64(57), np.int64(57), np.int64(57), np.int64(55), np.int64(53), np.int64(44), np.int64(33), np.int64(17), np.int64(15)],  # r=3.70, Δr=3.2e-08
    [np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(51), np.int64(53), np.int64(31), np.int64(25), np.int64(13)],  # r=3.70, Δr=1.0e-05
    [np.int64(71), np.int64(67), np.int64(62), np.int64(58), np.int64(52), np.int64(48), np.int64(44), np.int64(39), np.int64(42), np.int64(20), np.int64(17)],  # r=3.75, Δr=0.0e+00
    [np.int64(57), np.int64(57), np.int64(58), np.int64(58), np.int64(52), np.int64(46), np.int64(44), np.int64(39), np.int64(23), np.int64(21), np.int64(17)],  # r=3.75, Δr=1.0e-10
    [np.int64(46), np.int64(46), np.int64(46), np.int64(46), np.int64(46), np.int64(47), np.int64(44), np.int64(38), np.int64(26), np.int64(20), np.int64(17)],  # r=3.75, Δr=3.2e-08
    [np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(35), np.int64(39), np.int64(31), np.int64(21), np.int64(17)],  # r=3.75, Δr=1.0e-05
    [np.int64(67), np.int64(62), np.int64(59), np.int64(52), np.int64(47), np.int64(42), np.int64(35), np.int64(27), np.int64(25), np.int64(17), np.int64(11)],  # r=3.80, Δr=0.0e+00
    [np.int64(61), np.int64(62), np.int64(57), np.int64(54), np.int64(47), np.int64(46), np.int64(35), np.int64(27), np.int64(27), np.int64(17), np.int64(12)],  # r=3.80, Δr=1.0e-10
    [np.int64(47), np.int64(47), np.int64(47), np.int64(47), np.int64(48), np.int64(43), np.int64(37), np.int64(27), np.int64(26), np.int64(17), np.int64(12)],  # r=3.80, Δr=3.2e-08
    [np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(32), np.int64(33), np.int64(27), np.int64(17), np.int64(12)],  # r=3.80, Δr=1.0e-05
    [np.int64(1000), np.int64(1000), np.int64(1000), np.int64(41), np.int64(37), np.int64(36), np.int64(28), np.int64(24), np.int64(22), np.int64(21), np.int64(10)],  # r=3.85, Δr=0.0e+00
    [np.int64(1000), np.int64(1000), np.int64(1000), np.int64(41), np.int64(37), np.int64(39), np.int64(29), np.int64(24), np.int64(22), np.int64(24), np.int64(10)],  # r=3.85, Δr=1.0e-10
    [np.int64(37), np.int64(37), np.int64(37), np.int64(37), np.int64(1000), np.int64(1000), np.int64(29), np.int64(24), np.int64(22), np.int64(19), np.int64(10)],  # r=3.85, Δr=3.2e-08
    [np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(24), np.int64(26), np.int64(22), np.int64(19), np.int64(10)],  # r=3.85, Δr=1.0e-05
    [np.int64(63), np.int64(59), np.int64(53), np.int64(45), np.int64(37), np.int64(30), np.int64(24), np.int64(22), np.int64(17), np.int64(14), np.int64(9)],  # r=3.90, Δr=0.0e+00
    [np.int64(49), np.int64(49), np.int64(49), np.int64(45), np.int64(40), np.int64(28), np.int64(24), np.int64(22), np.int64(19), np.int64(14), np.int64(9)],  # r=3.90, Δr=1.0e-10
    [np.int64(30), np.int64(30), np.int64(30), np.int64(30), np.int64(30), np.int64(28), np.int64(24), np.int64(22), np.int64(17), np.int64(14), np.int64(9)],  # r=3.90, Δr=3.2e-08
    [np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(20), np.int64(21), np.int64(19), np.int64(14), np.int64(9)],  # r=3.90, Δr=1.0e-05
]).reshape(5, 4, 11)

PRECALC_DATA = {
    'r_values': np.array([3.7, 3.75, 3.8, 3.85, 3.9]),
    'model_bias_values': np.array([0, 1e-10, 10**(-7.5), 1e-5]),
    'ic_bias_values': np.array([1e-13, 1e-12, 1e-11, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]),
    'surface': {
        'median': PRECALC_SURFACE_MEDIAN,
        'mean': PRECALC_SURFACE_MEAN,
        'mode': PRECALC_SURFACE_MODE
    }
}