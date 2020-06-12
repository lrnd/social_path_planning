import numpy as np
import matplotlib.pyplot as plt
import pickle


class SelfPickling():
    @classmethod
    def load(cls, filepath):
        """Load SparseCrowdSequence from filepath"""
        try:
            with open(filepath, 'rb') as f:
                loaded = pickle.load(f)
        except UnicodeDecodeError as e:
            with open(filepath, 'rb') as f:
                loaded = pickle.load(f, encoding='latin1')
        except Exception as e:
            print('Unable to load data ', filepath, ':', e)
            raise
        if not isinstance(loaded, cls):
            raise ValueError('File does not contain object of type: {}'
                             .format(cls.__name__))
        return loaded

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f, protocol=2)


class SparsePersonSequence():
    '''Timestamped motion sequence of a single person'''
    def __init__(self, person_id, timestamps, states):
        self.person_id = int(person_id)
        self.timestamps = np.array(timestamps, dtype=float)  # seconds
        self.states = np.array(states, dtype=float)

        if len(self.timestamps.shape) != 1:
            raise ValueError('timestamps has bad shape')
        if len(self.states.shape) != 2:
            raise ValueError('states has bad shape')
        if len(self.timestamps) == 0:
            raise ValueError('timestamps has zero length')
        if len(self.states) == 0:
            raise ValueError('states has zero length')
        if self.timestamps.shape[0] != self.states.shape[0]:
            raise ValueError('Expected timestamps and states to have same '
                             'length but they do not')
        if not all(np.isfinite(self.timestamps)):
            raise ValueError('All timestamps must be finite')
        if not all(np.isfinite(self.states.reshape(-1))):
            raise ValueError('All states must be finite')

    def __len__(self):
        return len(self.timestamps)

    def __getitem__(self, item):
        return self.timestamps[item], self.states[item, :]

    def start_time(self):
        return self.timestamps[0]

    def end_time(self):
        return self.timestamps[-1]

    # TODO: Split person on large gaps in time


class SparseCrowdSequence(SelfPickling):
    """Timestamped sequence of multiple pedestrians"""

    def __init__(self, persons=[]):
        if not isinstance(persons, list):
            raise TypeError('Argument persons should be a list')
        if any([not(isinstance(p, SparsePersonSequence)) for p in persons]):
            raise TypeError('All elements of persons should be type: {}'
                            .format(SparsePersonSequence.__name__))
        self.persons = persons

    def plot(self):
        for p in self.persons:
            plt.plot(p.states[:, 0], p.states[:, 1])
        plt.show()

    def start_time(self):
        return min([p.start_time() for p in self.persons])

    def end_time(self):
        return max([p.end_time() for p in self.persons])

    def to_dense_crowd_sequence(self, delta_t):
        timestamps = np.arange(self.start_time(), self.end_time(), delta_t)
        dense_persons = []
        for person in self.persons:
            valid_times = np.logical_and(
                timestamps >= person.start_time(),
                timestamps < person.end_time())
            if any(valid_times):
                start_frame = valid_times.nonzero()[0][0]
                states = np.full((valid_times.sum(), person.states.shape[1]),
                                 np.nan)
                for dim in range(states.shape[1]):
                    states[:, dim] = np.interp(
                        timestamps[valid_times],
                        person.timestamps,
                        person.states[:, dim])
                dense_persons.append(DensePersonSequence(
                    person.person_id, start_frame, states))
            else:
                print('Ignoring brief pedestrian sequence')
        return DenseCrowdSequence(dense_persons, delta_t)


class DensePersonSequence():
    '''Motion sequence of a single person'''
    def __init__(self, person_id, start_frame, states):
        self.person_id = int(person_id)
        self.start_frame = int(start_frame)
        self.states = np.array(states, dtype=float)
        if len(self.states.shape) != 2:
            ValueError('states should have 2 dimensions')

    @property
    def stop_frame(self):
        return self.start_frame + self.states.shape[0]

    def crop_and_split(self, lower_bounds, upper_bounds):
        lower_bounds = np.array(lower_bounds)
        upper_bounds = np.array(upper_bounds)
        if lower_bounds.shape != (self.states.shape[-1],):
            raise ValueError('Expected shape of lower_bounds to be {}, got {}'
                             .format((self.states.shape[-1],),
                                     lower_bounds.shape))
        if upper_bounds.shape != (self.states.shape[-1],):
            raise ValueError('Expected length of upper_bounds to be {}, got {}'
                             .format((self.states.shape[-1],),
                                     upper_bounds.shape))

        above_lower = (self.states >= lower_bounds).all(axis=-1)
        below_upper = (self.states <= upper_bounds).all(axis=-1)
        inside_bounds = np.logical_and(above_lower, below_upper)
        edges = np.diff(inside_bounds.astype(int), prepend=0, append=0)
        # +1 will be start of sequence
        # -1 will be (after) end of sequence
        start_frames = (edges == 1).nonzero()[0]
        stop_frames = (edges == -1).nonzero()[0]
        return [DensePersonSequence(self.person_id,
                                    self.start_frame + start,
                                    self.states[start:stop])
                for start, stop in zip(start_frames, stop_frames)]

    def __getitem__(self, key):
        if isinstance(key, tuple):
            if len(key) == 1:
                key0 = key[0]
                key1 = slice(None)
            elif len(key) == 2:
                key0, key1 = key
            else:
                raise IndexError('Wrong number of indicies')
        else:
            key0 = key
            key1 = slice(None)
        if isinstance(key1, int):
            len_key1 = 1
        else:
            len_key1 = ((2 if key1.stop is None else key1.stop)
                        - (0 if key1.start is None else key1.start))
        if isinstance(key0, int):
            # Integer index will access one row of states offset by
            # the start_frame
            # For out of bounds index numpy should raise IndexError
            if key0 < self.start_frame or key0 >= self.stop_frame:
                raise IndexError('Index out of range')
            return self.states[key0 - self.start_frame, key1]
        elif isinstance(key0, slice):
            # Slice access doesn't allow steps
            # Completely out of bounds ranges raise IndexError however...
            key0 = slice(
                self.start_frame if key0.start is None else key0.start,
                self.stop_frame if key0.stop is None else key0.stop,
                1 if key0.step is None else key0.step)
            if key0.step != 1:
                raise IndexError('{} does not support slice steps other than 1'
                                 .format(self.__class__))
            if key0.start >= key0.stop:
                raise IndexError('Empty or backwards slice')
            if key0.start >= self.stop_frame or key0.stop <= self.start_frame:
                raise IndexError('Out of bounds')
            # ...partially out of bounds ranges will return array of requested
            # size, padded with NaNs where out of bounds
            # First determine the overlap between desire and reality
            valid_start = max(key0.start, self.start_frame)
            valid_stop = min(key0.stop, self.stop_frame)
            # Allocate nan array of desired size
            output_array = np.full(
                (key0.stop - key0.start, len_key1), np.nan)
            # Populate with valid data from overlap region
            output_array[valid_start - key0.start:valid_stop - key0.start, key1] =\
                self.states[valid_start - self.start_frame:
                            valid_stop - self.start_frame, :]
            return output_array


class DenseCrowdSequence(SelfPickling):
    """Motion sequence of multiple pedestrians at fixed framerate"""

    def __init__(self, persons, delta_t):
        if not isinstance(persons, list):
            raise TypeError('Argument persons should be a list')
        if any([not(isinstance(p, DensePersonSequence)) for p in persons]):
            raise TypeError('All elements of persons should be type: {}'
                            .format(DensePersonSequence.__name__))
        self.persons = persons
        self.delta_t = delta_t

    @property
    def start_frame(self):
        return min([p.start_frame for p in self.persons])

    @property
    def stop_frame(self):
        return max([p.stop_frame for p in self.persons])

    def plot(self):
        for p in self.persons:
            plt.plot(p.states[:, 0], p.states[:, 1])
        plt.show()

    def crop_and_split(self, lower_bounds, upper_bounds):
        lower_bounds = np.array(lower_bounds)
        upper_bounds = np.array(upper_bounds)
        expected_shape = (2,)
        if lower_bounds.shape != expected_shape:
            raise ValueError('Expected shape of lower_bounds to be {}, got {}'
                             .format(expected_shape, lower_bounds.shape))
        if upper_bounds.shape != expected_shape:
            raise ValueError('Expected length of upper_bounds to be {}, got {}'
                             .format(expected_shape, upper_bounds.shape))

        self.persons = [p for person in self.persons
                        for p in person.crop_and_split(
                            lower_bounds, upper_bounds)]

    def __len__(self):
        return self.stop_frame - self.start_frame

    def __getitem__(self, key):
        if isinstance(key, int):
            key = slice(key, key + 1, 1)
        elif isinstance(key, slice):
            if not (key.step is None or key.step == 1):
                raise IndexError('step size other than 1 not handled')
            key = slice(
                0 if key.start is None else key.start,
                self.stop_frame if key.stop is None else key.stop, 1)

        person_arrays = []
        skips = 0
        for p in self.persons:
            try:
                person_arrays.append(p[key])
            except IndexError:
                skips += 1
        if skips:
            print('Skipped {} people due to invalid index'.format(skips))
        if person_arrays:
            return np.stack(person_arrays, axis=1)
        else:
            return None
