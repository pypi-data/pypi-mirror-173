import unittest
import pydarm
import numpy as np
import h5py
import os
from pydarm.FIR import (FIRfilter, createFIRfilter,
                        correctFIRfilter, two_tap_zero_filter_response,
                        check_td_vs_fd, check_td_vs_fd_response)


class TestFIRfilter(unittest.TestCase):

    def setUp(self):
        self.window = np.array([6.747975786659215006e-03,
                                2.767078112501164186e-02,
                                7.377080623487733413e-02,
                                1.551839702572553048e-01,
                                2.768990448483386047e-01,
                                4.345680722833729082e-01,
                                6.125095782158316293e-01,
                                7.853264037228884220e-01,
                                9.232791494417179612e-01,
                                1.000000000000000000e+00,
                                1.000000000000000000e+00,
                                9.232791494417179612e-01,
                                7.853264037228884220e-01,
                                6.125095782158316293e-01,
                                4.345680722833729082e-01,
                                2.768990448483386047e-01,
                                1.551839702572553048e-01,
                                7.377080623487733413e-02,
                                2.767078112501164186e-02,
                                6.747975786659215006e-03])

    def tearDown(self):
        del self.window

    def test_FIRfilter(self):
        test_filter = FIRfilter(fNyq=10, dur=1, highpass_fcut=10, lowpass_fcut=None,
                                latency=None, window_type='dpss', freq_res=3.0)
        self.assertEqual(len(test_filter.window), len(self.window))
        for n in range(len(self.window)):
            self.assertAlmostEqual(np.real(test_filter.window[n]),
                                   np.real(self.window[n]))


class TestCreateFIRfilter(unittest.TestCase):

    def setUp(self):
        self.FIRPars = FIRfilter(fNyq=10, dur=1, highpass_fcut=10, lowpass_fcut=None,
                                 latency=None, window_type='dpss', freq_res=3.0)
        self.config = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
coupled_cavity_optical_gain = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency = 4.468
detuned_spring_Q = 52.14
sensing_sign = 1
is_pro_spring = True
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
whitening_mode_names = mode1, mode1
omc_meas_p_trans_amplifier_uncompensated   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
omc_meas_p_whitening_uncompensated_mode1   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1, 1
omc_filter_file = test/H1OMC_1239468752.txt
omc_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_filter_noncompensating_modules =
omc_filter_gain = 1, 1
omc_front_end_trans_amplifier_compensation = ON, ON
omc_front_end_whitening_compensation_mode1 = ON, ON
'''
        self.known_Cfir = np.array(
            [-1227.5838658444798, 3076.9909960599016,
             8947.14656965102, -44153.12903009791,
             41690.73653592548, 100767.29509196931,
             -304463.1208524438, 201108.6390562277,
             475074.27072160656, -1368003.356637503,
             1709874.866117381, -1187997.4667580684,
             315569.9399449083, 208373.70618745242,
             -228827.46425164823, 62660.986752700665,
             23681.058343631747, -19301.994938787342,
             2292.852371773494, 954.6954319571059])

    def tearDown(self):
        del self.FIRPars
        del self.config
        del self.known_Cfir

    def test_createFIRfilter(self):
        C = pydarm.sensing.SensingModel(self.config)
        Cf = C.compute_sensing(self.FIRPars.freq_array)
        test_Cfir = createFIRfilter(self.FIRPars, Cf)[0]

        for n in range(len(self.known_Cfir)):
            self.assertAlmostEqual(np.real(test_Cfir[n]) /
                                   np.real(self.known_Cfir[n]),
                                   1.0)


class TestCorrectFIRfilter(unittest.TestCase):

    def setUp(self):
        self.FIRPars = FIRfilter(fNyq=10, dur=1, highpass_fcut=10, lowpass_fcut=None,
                                 latency=None, window_type='dpss', freq_res=3.0)
        self.config = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
coupled_cavity_optical_gain = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency = 4.468
detuned_spring_Q = 52.14
sensing_sign = 1
is_pro_spring = True
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
omc_meas_p_trans_amplifier_uncompensated   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
whitening_mode_names = mode1, mode1
omc_meas_p_whitening_uncompensated_mode1   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1, 1
omc_filter_file = test/H1OMC_1239468752.txt
omc_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_filter_noncompensating_modules =
omc_filter_gain = 1, 1
omc_front_end_trans_amplifier_compensation = ON, ON
omc_front_end_whitening_compensation_mode1 = ON, ON
'''
        self.known_Corfir = np.array(
            [-169801.88070366555-219.1204830342667j,
             -957689.5963380174-34613.22973139465j,
             -4098624.0961085237-351429.94821935653j,
             -21990666.91293493-3485607.618296178j,
             26602599.411241055-548641.5068307472j,
             11374028.314446637+243703.54819104425j,
             6989957.85280983+5347.050013464119j,
             4675314.739251457-196822.09592547035j,
             4268072.935259017-178027.61932502355j,
             4018006.170981767-172823.8165376102j])

    def tearDown(self):
        del self.FIRPars
        del self.config
        del self.known_Corfir

    def test_correctFIRfilter(self):
        C = pydarm.sensing.SensingModel(self.config)
        Cf = C.compute_sensing(self.FIRPars.freq_array)
        test_Cfir = createFIRfilter(self.FIRPars, Cf)[0]
        test_Corfir = correctFIRfilter(self.FIRPars, test_Cfir, Cf,  [2, 4, 7, 9])
        test_Corfir = np.delete(test_Corfir, 0)

        self.assertEqual(len(test_Corfir), len(self.known_Corfir))
        for n in range(len(test_Corfir)):
            self.assertAlmostEqual(
                np.abs(test_Corfir[n])/np.abs(self.known_Corfir[n]), 1)
            self.assertAlmostEqual(
                np.angle(test_Corfir[n], deg=True) -
                np.angle(self.known_Corfir[n], deg=True), 0)


class Testtwo_tap_zero_filter(unittest.TestCase):

    def setUp(self):
        self.known_two_tap_zero_filt = np.array(
            [0.999999999999999889+0.000000000000000000j,
             0.944065144524670274-0.242141032019198316j,
             0.791790257603250391-0.430462197742083885j,
             0.584088546831189381-0.528606912083167346j,
             0.372528221948197957-0.528347694598477635j,
             0.201488911932644205-0.449462235973869528j,
             0.094304975193611695-0.329261396976028187j,
             0.048712779360778842-0.206416348868232596j,
             0.042948901676579269-0.105952738743734842j,
             0.049370136034108433-0.031598975501051528j])

    def tearDown(self):
        del self.known_two_tap_zero_filt

    def test_two_tap_zero_filt(self):
        test_ttzf = two_tap_zero_filter_response([1, 2], 1, np.linspace(1, 100, 10))

        for n in range(len(test_ttzf)):
            self.assertAlmostEqual(np.abs(test_ttzf[n]),
                                   np.abs(self.known_two_tap_zero_filt[n]), places=6)
            self.assertAlmostEqual(np.angle(test_ttzf[n], deg=True),
                                   np.angle(self.known_two_tap_zero_filt[n], deg=True),
                                   places=6)


class Testcheck_td_vs_fd(unittest.TestCase):

    def setUp(self):
        self.FIRPars = FIRfilter(fNyq=10, dur=1, highpass_fcut=10, lowpass_fcut=None,
                                 latency=None, window_type='hann', freq_res=3.0)
        self.config = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
coupled_cavity_optical_gain = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency = 4.468
detuned_spring_Q = 52.14
sensing_sign = 1
is_pro_spring = True
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
whitening_mode_names = mode1, mode1
omc_meas_p_trans_amplifier_uncompensated   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
omc_meas_p_whitening_uncompensated_mode1   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1, 1
omc_filter_file = test/H1OMC_1239468752.txt
omc_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_filter_noncompensating_modules =
omc_filter_gain = 1, 1
omc_front_end_trans_amplifier_compensation = ON, ON
omc_front_end_whitening_compensation_mode1 = ON, ON
'''
        self.known_freq_array = np.array(
            [0., 0.125, 0.25, 0.375, 0.5, 0.625, 0.75,
             0.875, 1., 1.125, 1.25, 1.375, 1.5, 1.625,
             1.75, 1.875, 2., 2.125, 2.25, 2.375, 2.5,
             2.625, 2.75, 2.875, 3., 3.125, 3.25, 3.375,
             3.5, 3.625, 3.75, 3.875, 4., 4.125, 4.25,
             4.375, 4.5, 4.625, 4.75, 4.875, 5., 5.125,
             5.25, 5.375, 5.5, 5.625, 5.75, 5.875, 6.,
             6.125, 6.25, 6.375, 6.5, 6.625, 6.75, 6.875,
             7., 7.125, 7.25, 7.375, 7.5, 7.625, 7.75,
             7.875, 8., 8.125, 8.25, 8.375, 8.5, 8.625,
             8.75, 8.875, 9., 9.125, 9.25, 9.375, 9.5,
             9.625, 9.75, 9.875, 10.])

    def tearDown(self):
        del self.FIRPars
        del self.config
        del self.known_freq_array

    def test_check_td_vs_fd(self):
        C = pydarm.sensing.SensingModel(self.config)
        Cf = C.compute_sensing(self.FIRPars.freq_array)
        test_Cfir = createFIRfilter(self.FIRPars, Cf)
        test_ctvf = check_td_vs_fd(test_Cfir[0], Cf, fNyq=10,
                                   delay_samples=self.FIRPars.delay_samples,
                                   filename="res_corr_fd_comparison.png",
                                   plot_title="Residual corrections comparison.")
        test_freq = test_ctvf[0][0]

        # Note that the 0th element == 0 so we test differently 
        for n in range(len(test_freq)):
            if n == 0:
                self.assertAlmostEqual(test_freq[n], self.known_freq_array[n])
            else:
                self.assertAlmostEqual(test_freq[n] / self.known_freq_array[n],
                                       1, places=6)


class TestCheckTdVsFdResponse(unittest.TestCase):

    def setUp(self):
        self.FIRPars = FIRfilter(fNyq=10, dur=1, highpass_fcut=10, lowpass_fcut=None,
                                 latency=None, window_type='hann', freq_res=3.0)
        self.config = '''
[metadata]
[interferometer]
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
coupled_cavity_optical_gain = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency = 4.468
detuned_spring_Q = 52.14
sensing_sign = 1
is_pro_spring = True
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
whitening_mode_names = mode1, mode1
omc_meas_p_trans_amplifier_uncompensated   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
omc_meas_p_whitening_uncompensated_mode1   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1, 1
omc_filter_file = test/H1OMC_1239468752.txt
omc_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_filter_noncompensating_modules =
omc_filter_gain = 1, 1
omc_front_end_trans_amplifier_compensation = ON, ON
omc_front_end_whitening_compensation_mode1 = ON, ON

[digital]
digital_filter_file    = test/H1OMC_1239468752.txt
digital_filter_bank    = LSC_DARM1, LSC_DARM2
digital_filter_modules = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain    = 400,1

[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x    = OFF, ON, ON, ON
darm_feedback_y    = OFF, OFF, OFF, OFF

[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
suspension_file = test/H1susdata_O3.mat
tst_driver_uncompensated_Z_UL = 129.7e3
tst_driver_uncompensated_Z_LL = 90.74e3
tst_driver_uncompensated_Z_UR = 93.52e3
tst_driver_uncompensated_Z_LR = 131.5e3
tst_driver_uncompensated_P_UL = 3.213e3, 31.5e3
tst_driver_uncompensated_P_LL = 3.177e3, 26.7e3
tst_driver_uncompensated_P_UR = 3.279e3, 26.6e3
tst_driver_uncompensated_P_LR = 3.238e3, 31.6e3
tst_driver_DC_gain_VpV_HV = 40
tst_driver_DC_gain_VpV_LV = 1.881
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
uim_delay = 0
pum_delay = 0
tst_delay = 0

[pcal]
pcal_filter_file           = test/H1CALEY_1123041152.txt
pcal_filter_bank           = PCALY_TX_PD
pcal_filter_modules_in_use = 6,8
pcal_filter_gain           = 1.0
pcal_dewhiten               = 1.0, 1.0
pcal_incidence_angle        = 8.8851
pcal_etm_watts_per_ofs_volt = 0.13535
ref_pcal_2_darm_act_sign    = -1.0
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat
'''
        self.known_freq_array = np.array(
            [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75,
             3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75,
             6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25, 8.5, 8.75,
             9.0, 9.25, 9.5, 9.75, 10.0])

    def tearDown(self):
        del self.FIRPars
        del self.config
        del self.known_freq_array

    def test_check_td_vs_fd(self):
        freq = self.FIRPars.freq_array
        freq = np.delete(freq, 0)
        darm = pydarm.darm.DARMModel(self.config)
        InvC = 1/darm.sensing.compute_sensing(freq)
        TST_filt = darm.actuation.xarm.compute_actuation_single_stage(freq, stage='TST')
        PUM_filt = darm.actuation.xarm.compute_actuation_single_stage(freq, stage='PUM')
        UIM_filt = darm.actuation.xarm.compute_actuation_single_stage(freq, stage='UIM')
        dig_filt = darm.digital.compute_response(freq)
        R = darm.compute_response_function(freq)

        # TODO: this function emits a lot of warnings. Experts need to look at
        # this more carefully
        test_ctvf = check_td_vs_fd_response(InvC,
                                            None,
                                            TST_filt,
                                            PUM_filt,
                                            UIM_filt,
                                            None,
                                            dig_filt,
                                            R,
                                            invsens_fNyq=10,
                                            invsens_highpass_fNyq=10,
                                            act_fNyq=10,
                                            D_fNyq=10,
                                            R_fNyq=10,
                                            invsens_delay=None,
                                            invsens_highpass_delay=None,
                                            act_delay=None,
                                            act_highpass_delay=None,
                                            time_delay=1.0/16384,
                                            filename="td_vs_fd_response.png",
                                            plot_title="Response Function",
                                            legend=['DARM model', 'FIR filters'])
        test_freq = test_ctvf[0]
        test_ratio_mag = test_ctvf[1]
        test_ratio_pha = test_ctvf[2]

        # TODO: need to add test_ratio_mag and test_ratio_pha here.
        # Evan is concerned these don't look good right now - they are not
        # close to 1 in magnitude and 0 degrees phase
        for n in range(len(test_freq)):
            self.assertAlmostEqual(test_freq[n], self.known_freq_array[n])


class TestGDS_FIR_filter_generation(unittest.TestCase):
    def setUp(self):
        # Maddie test
        # Set up for control chain FIR filter generation
        self.FIRpars = FIRfilter(fNyq=1024, dur=3.5, highpass_fcut=10.5, lowpass_fcut=None,
                                 latency=None, window_type='dpss', freq_res=4.0)

        # Load in known transfer function and resulting FIR filter
        h5f = h5py.File('./test/FIR_unit_test_coeffs.h5', 'r')
        self.known_FIR_filter = h5f['FIR_filter'][:]
        self.known_tf = h5f['transfer_function'][:]

    def tearDown(self):
        del self.FIRpars
        del self.known_FIR_filter
        del self.known_tf

    def test_GDS_FIR_filter_generation(self):
        # Generate test FIR filter from frequency domain transfer function
        [test_FIR_filter, model] = createFIRfilter(self.FIRpars, self.known_tf)
        # FIXME: (Arif) Scipy and FIRtools have much different results under 10 Hz.
        # I changed the range and places. My local test could take higher places.
        for n in range(300, len(self.known_FIR_filter)-300):
            self.assertAlmostEqual(abs((self.known_FIR_filter[n] / test_FIR_filter[n])
                                       - 1), 0, places=3)


class TestFilterGeneration(unittest.TestCase):

    def setUp(self):
        self.arm_length = 3994.4698
        self.fcc = 410.6
        self.fs = 4.468
        self.fs_squared = 19.963024
        self.srcQ = 52.14
        self.ips = 1.0
        os.environ['CAL_DATA_ROOT'] = './test'

    def tearDown(self):
        del self.arm_length
        del self.fcc
        del self.fs
        del self.fs_squared
        del self.srcQ
        del self.ips
        del os.environ['CAL_DATA_ROOT']

    def test_FilterGeneration(self):
        config = './example_model_files/H1_20190416.ini'
        FG = pydarm.FIR.FilterGeneration(config)
        self.assertEqual(self.arm_length, FG.arm_length)
        self.assertEqual(self.fcc, FG.fcc)
        self.assertEqual(self.fs, FG.fs)
        self.assertEqual(self.fs_squared, FG.fs_squared)
        self.assertEqual(self.srcQ, FG.srcQ)
        self.assertEqual(self.ips, FG.ips)


class TestGDS(unittest.TestCase):

    def setUp(self):
        self.GDS_file = h5py.File('./test/GDS_test.h5', 'r')
        self.ctrl_corr_td = self.GDS_file['ctrl_corr_filter'][:]
        os.environ['CAL_DATA_ROOT'] = './test'

    def tearDown(self):
        del self.GDS_file
        del self.ctrl_corr_td
        del os.environ['CAL_DATA_ROOT']

    def test_GDS(self):
        config = './example_model_files/H1_20190416.ini'
        FG = pydarm.FIR.FilterGeneration(config)
        FG.GDS(ctrl_window_type='dpss', res_window_type='dpss',
               make_plot=False, output_filename='./test/GDS.npz',
               plots_directory='./examples/GDS_plots')
        gds = np.load('./test/GDS.npz')
        ctrl_td = gds['ctrl_corr_filter']
        for n in range(1000, len(self.ctrl_corr_td)-1000):
            self.assertAlmostEqual(abs((self.ctrl_corr_td[n] / ctrl_td[n])
                                       - 1), 0, places=3)


class TestDCS(unittest.TestCase):

    def setUp(self):
        self.DCS_file = h5py.File('./test/DCS_test.h5', 'r')
        self.known_act_tst = self.DCS_file['actuation_tst'][:]
        os.environ['CAL_DATA_ROOT'] = './test'

    def tearDown(self):
        del self.DCS_file
        del self.known_act_tst
        del os.environ['CAL_DATA_ROOT']

    def test_DCS(self):
        config = './example_model_files/H1_20190416.ini'
        FG = pydarm.FIR.FilterGeneration(config)
        FG.DCS(act_window_type='dpss', invsens_window_type='dpss',
               make_plot=False, output_filename='./test/DCS.npz',
               plots_directory='examples/DCS_plots')
        gds = np.load('./test/DCS.npz')
        act_tst = gds['actuation_tst']
        for n in range(1000, len(self.known_act_tst)-1000):
            self.assertAlmostEqual(abs((self.known_act_tst[n] / act_tst[n])
                                       - 1), 0, places=3)


if __name__ == '__main__':
    unittest.main()
