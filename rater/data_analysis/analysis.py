__author__ = 'anton'
import skll.metrics as metrics
import numpy
import random
import scipy.stats as stats
import math


class Rating:

    batch_id = 0

    rater_id = 0

    segment_id = 0

    rating = 0

    def __init__(self, batch_id, rater_id, segment_id, rating):
        self.batch_id = batch_id
        self.rater_id = rater_id
        self.segment_id = segment_id
        self.rating = rating


class Ratings:

    ids = []

    batch_hash = {}

    ratings = []

    def __init__(self, data_file):
        with open(data_file, 'r') as f:
            read_data = f.read()
            self.ratings = []
            for line in read_data.splitlines():
                rating_data = line.split("|")
                self.ratings.append(Rating(batch_id=int(rating_data[0]),
                                      rater_id=int(rating_data[1]),
                                      segment_id=int(rating_data[2]),
                                      rating=int(rating_data[3])))

            for i in [1, 2, 3, 4]:
                rater_ids = self.get_rater_ids(i)
                for id in rater_ids:
                    self.batch_hash[id] = i
                self.ids.extend(rater_ids)
                
    def get_rating_values(self, rater_id):
        values = []
        segments = []
        for rating_object in self.ratings:
            if rating_object.rater_id == rater_id and rating_object.segment_id not in segments:
                values.append(rating_object.rating)
                segments.append(rating_object.segment_id)

        return values

    def get_rating_values_for_batch(self, batch_id):
        values = []

        for id in self.get_rater_ids(batch_id):
            v = self.get_rating_values(id)
            if len(v) < 100:
                continue
            values.extend(v)

        return values

    def get_rating_values_for_batch_and_index(self, batch_id, i):
        values = []

        for id in self.get_rater_ids(batch_id):
            values.append(self.get_rating_values(id)[i])

        return values

    def get_normalized_rating_values(self, rater_id):
        values = self.get_rating_values(rater_id)
        mean = numpy.mean(values)
        std = numpy.std(values)
        return [float(v - mean)/std for v in values]

    def get_rater_ids(self, batch_id):
        values = []
        for rating_object in self.ratings:
            if rating_object.batch_id == batch_id and rating_object.rater_id not in values:
                values.append(rating_object.rater_id)

        return values[0:5]
                
    def print_kappa(self, method, one_off=False):
        mean_kappa_same = []
        mean_kappa_diff = []

        for i in range(0,50):

            checked_pairs = []
            checked_pairs_same = []
            checked_pairs_diff = []
            kappas_same = []
            kappas_diff = []

            # calculating agreement for pairs from the same batches and different batches
            while len(checked_pairs_same) < 20 or len(checked_pairs_diff) < 20:
                id1 = random.choice(self.ids)
                id2 = random.choice(self.ids)
                pair = sorted([id1, id2])
                if pair not in checked_pairs and id1 != id2:
                    values_first = self.get_rating_values(id1)
                    values_second = self.get_rating_values(id2)
                    if len(values_first) != len(values_second) or len(values_first) == 0:
                        continue

                    if method == 'standard':
                        kappa = metrics.kappa(values_first, values_second)
                    else:
                        kappa = metrics.kappa(values_first, values_second, method, one_off)

                    if self.batch_hash[id1] == self.batch_hash[id2]:
                        kappas_same.append(kappa)
                        checked_pairs_same.append(pair)
                    else:
                        kappas_diff.append(kappa)
                        checked_pairs_diff.append(pair)

                    checked_pairs.append(pair)

            mean_kappa_same.append(numpy.mean(kappas_same))
            mean_kappa_diff.append(numpy.mean(kappas_diff))

        print("Kappa same group: " + str(numpy.mean(mean_kappa_same)) + " different groups: " + str(numpy.mean(mean_kappa_diff)))
        print("Confidence same: " + str(stats.norm.interval(0.999, loc=numpy.mean(mean_kappa_same), scale=numpy.std(mean_kappa_same)/math.sqrt(50))) + " different: " + str(stats.norm.interval(0.999, loc=numpy.mean(mean_kappa_diff), scale=numpy.std(mean_kappa_diff)/math.sqrt(50))))

    def print_segments_with_highest_std(self):
        segment_stds = {}
        for i in range(0, 100):
            means = []
            for b in [1, 2, 3, 4]:
                v = self.get_rating_values_for_batch_and_index(b, i)
                means.append(numpy.mean(v))
            segment_stds[numpy.std(means)] = i

        for std in sorted(segment_stds.keys(), reverse=True):
            print(str(std) + " : " + str(segment_stds[std]))

    def print_segment_ratings(self, segment_id):
        segment_stds = {}
        for i in range(0, 100):
            means = []
            for b in [1, 2, 3, 4]:
                v = self.get_rating_values_for_batch_and_index(b, i)
                means.append(numpy.mean(v))
            segment_stds[numpy.std(means)] = i

        for b in [1, 2, 3, 4]:
            v = self.get_rating_values_for_batch_and_index(b, segment_id)
            print(str(b) + " : " + str(v) + " : " + str(numpy.mean(v)))

    def print_group_metrics(self, batch_ids):
        for i in batch_ids:
            rater_ids = self.get_rater_ids(i)
            v = []
            for id in rater_ids:
                annotator_values = self.get_rating_values(id)
                v.extend(annotator_values)
            print("Metrics for group " + str(i) + ": mean " + str(numpy.mean(v)) + " std " + str(numpy.std(v)))

    def print_std_for_slice(self, from_index, to_index):
        v = []
        for b in [1, 2, 3, 4]:
            for id in self.get_rater_ids(b):
                v.append(numpy.std(self.get_rating_values(id)[from_index:to_index]))

        print(numpy.mean(v))


r = Ratings('data.txt')

if True:
    print("Standard kappa")
    r.print_kappa('standard')

    print("Linear kappa without one off")
    r.print_kappa('linear')

    print("Linear kappa with one off")
    r.print_kappa('linear', True)


if False:
    print("Segments sorted by std:")
    r.print_segments_with_highest_std()

    print("self. of segment with highest std:")
    r.print_segment_ratings(30)

if True:
    print("Group metrics: ")
    r.print_group_metrics([1, 2, 3, 4, 5])

# stds for different segments
if True:
    print("Chronological evolution of std: ")
    r.print_std_for_slice(0, 20)
    r.print_std_for_slice(20, 40)
    r.print_std_for_slice(40, 60)
    r.print_std_for_slice(60, 80)
    r.print_std_for_slice(80, 100)