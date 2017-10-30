import click
import itertools
import json
from functools import reduce
import operator
import select
import sys
import textwrap
import yaml


OPERATORS = {True: operator.gt, False: operator.le}

class BayesProcessor():
    def __init__(self, parsed_yaml, true_false, sensor_ind, target_entity):
        self.sensors = self.sensors_from_parsed_yaml(parsed_yaml, sensor_ind)
        self.compare_func = OPERATORS[true_false]
        self.summaries = []
        self.target_entity = target_entity

    def sensors_from_parsed_yaml(self, parsed_yaml, sensor_ind):
        yaml_parsers = {list: self.process_multiple,
                        dict: self.process_singular}

        bayesian_sensors = yaml_parsers.get(type(parsed_yaml),
                                            lambda x: [])(parsed_yaml)

        if sensor_ind is not None:
            sensors = [bayesian_sensors[sensor_ind]]
        else:
            sensors = bayesian_sensors

        return sensors

    @staticmethod
    def process_multiple(yaml):
        return [item for item in yaml if item['platform'] == 'bayesian']

    @staticmethod
    def process_singular(yaml):
        return [item for item in [yaml] if item['platform'] == 'bayesian']

    def proc_sensors(self, summarize):
        for sensor_dict in self.sensors:
            self.summaries.append({
                'name': sensor_dict['name'],
                'total_cases': 0,
                'total_matching': 0
            })

            observations = sensor_dict['observations']
            combos = self.generate_sensor_combinations(observations)
            target_combos = self.filter_target(combos, self.target_entity)

            true_conds = (comb for comb in target_combos
                          if self.process_all_combos(sensor_dict, comb))

            matching_cases = [
                list(self.render_condition(i) for i in list(cond))
                for cond in true_conds
            ]

            if not summarize:
                self.summaries[-1]['matching_cases'] = matching_cases

    @staticmethod
    def generate_sensor_combinations(observation_list):
        comb_gen = (itertools.combinations(observation_list, i + 1)
                    for i in range(len(observation_list) - 1))

        all_combs = itertools.chain(*comb_gen)

        # Is not possible to observe the same entity in multiple states.
        distinct_combs = (sorted(list({comb['entity_id']: comb
                          for comb in combs}.values()),
                          key=lambda k: k['entity_id'])
                          for combs in all_combs)

        distinct_combs = (list(x)
                          for x in set(tuple(tuple(y.items()) for y in x)
                                       for x in distinct_combs))
        return (list(dict(obs) for obs in comb) for comb in distinct_combs)

    @staticmethod
    def filter_target(combos, target):
        if target is not None:
            combos = (comb for comb in combos
                      if any(all(item in obs.items()
                      for item in target.items())
                      for obs in comb))

        return combos

    def process_all_combos(self, sensor, distinct_combs):
        prob = reduce(self.__process_combo, distinct_combs, sensor['prior'])

        result = self.compare_func(
            round(prob, 2), sensor['probability_threshold'])

        if result:
            self.summaries[-1]['total_matching'] += 1

        return result

    def __process_combo(self, prior, comb):
        prob_true = comb['prob_given_true']
        prob_false = comb.get('prob_given_false', 1 - prob_true)

        self.summaries[-1]['total_cases'] += 1
        return self.update_probability(prior, prob_true, prob_false)

    @staticmethod
    def render_condition(cond):
        cond = cond.copy()
        cond.pop('prob_given_true', None)
        cond.pop('prob_given_false', None)
        cond.pop('platform', None)

        return cond

    @staticmethod
    def update_probability(prior, prob_true, prob_false):
        """Update probability using Bayes' rule."""
        numerator = prob_true * prior
        denominator = numerator + prob_false * (1 - prior)

        probability = numerator / denominator
        return probability


if __name__ == '__main__':
    main()
