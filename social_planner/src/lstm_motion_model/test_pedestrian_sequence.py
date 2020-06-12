import unittest
import numpy as np
import lstm_motion_model.pedestrian_sequence as ps

class TestDensePersonSequence(unittest.TestCase):

    def setUp(self):
        self.states = np.random.rand(7, 2)
        self.p = ps.DensePersonSequence(3, 11, self.states)

    def test_getitem_int_valid(self):
        self.assertTrue(np.array_equal(self.p[11], self.states[0]))
        self.assertTrue(np.array_equal(self.p[13], self.states[2]))
        self.assertTrue(np.array_equal(self.p[17], self.states[-1]))

    def test_getitem_int_index_error(self):
        self.assertRaises(IndexError, self.p.__getitem__, -1)
        self.assertRaises(IndexError, self.p.__getitem__, 0)
        self.assertRaises(IndexError, self.p.__getitem__, 10)
        self.assertRaises(IndexError, self.p.__getitem__, 18)

    def test_getitem_tuple_index_error(self):
        self.assertRaises(IndexError, self.p.__getitem__, (0, 0))
        self.assertRaises(IndexError, self.p.__getitem__, (12, 3))
        self.assertRaises(IndexError, self.p.__getitem__, (20, 3))
        self.assertRaises(IndexError, self.p.__getitem__, (20, 1))


class TestDenseCrowdSequence(unittest.TestCase):

    def setUp(self):
        self.person_ids = (2, 5, 1)
        self.start_frames = (5, 9, 15)
        self.lengths = (6, 3, 4)
        self.dims = 2
        self.states = []
        self.persons = []
        for args in zip(self.person_ids, self.start_frames, self.lengths):
            person_id, start_frame, length = args
            self.states.append(np.random.rand(length, self.dims))
            self.persons.append(ps.DensePersonSequence(
                person_id, start_frame, self.states[-1]))
        self.crowd = ps.DenseCrowdSequence(self.persons, 0.1)

    def test_getitem_slice_all(self):
        # Get the whole thing by slicing
        output_array = self.crowd[:]
        # Check the full output has the right shape
        expected_length = max(start + length for start, length in zip(self.start_frames, self.lengths))
        expected_shape = (expected_length,
                          len(self.persons),
                          self.dims)
        self.assertTupleEqual(output_array.shape, expected_shape)
        # Check a nan slice
        test_array = output_array[4, :, :]
        expected_shape = (len(self.persons), self.dims)
        self.assertTupleEqual(test_array.shape, expected_shape)
        self.assertTrue(np.isnan(test_array).all())
        # Check a valid slice
        self.assertTrue(np.array_equal(output_array[9, 0, :],
                                       self.states[0][4]))
        self.assertTrue(np.array_equal(output_array[9, 1, :],
                                       self.states[1][0]))
        self.assertTrue(np.isnan(output_array[9, 2, :]).all())

    def test_gettime_slice_valid(self):
        output_array = self.crowd[4:14]
        expected_shape = (14 - 4, 2, self.dims)
        self.assertTupleEqual(output_array.shape, expected_shape)

    def test_gettime_slice_invalid(self):
            self.assertIsNone(self.crowd[1:4])
            self.assertIsNone(self.crowd[19:30])
