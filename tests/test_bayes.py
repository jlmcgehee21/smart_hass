#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bayes` command line tool."""

import pytest

from smart_hass import bayes


@pytest.fixture
def static_bayes():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    proc = bayes.BayesProcessor({'platform': 'bayesian'},
                                True, None, None)
    return proc

def test_proc_render_condition(static_bayes):
    orig_cond = {'foo': 'bar', 'prob_given_true': 0.5}
    rendered_cond = static_bayes.render_condition(orig_cond)

    assert orig_cond == {'foo': 'bar', 'prob_given_true': 0.5}
    assert rendered_cond == {'foo': 'bar'}

def test_proc_proc_multiple(static_bayes):
    multi_yaml = [{'platform': 'foo'},
                  {'platform': 'bayesian'},
                  {'platform': 'bar'}]

    result = static_bayes.process_multiple(multi_yaml)
    assert result == [multi_yaml[1]]

def test_proc_proc_singular(static_bayes):
    result = static_bayes.process_singular({'platform': 'bayesian'})
    assert result == [{'platform': 'bayesian'}]

def test_proc_generate_sensor_combinations(static_bayes):
    observations = [{'entity_id': 'foo', 'below': 1},
                    {'entity_id': 'bar'},
                    {'entity_id': 'foo', 'above': 3},
                    {'entity_id': 'baz'}]

    result = list(static_bayes.generate_sensor_combinations(observations))

    target_result = [[{'entity_id': 'foo', 'below': 1}, {'entity_id': 'bar'},
                      {'entity_id': 'baz'}],
                     [{'entity_id': 'bar'}, {'entity_id': 'baz'}],
                     [{'entity_id': 'foo', 'above': 3}, {'entity_id': 'baz'}],
                     [{'entity_id': 'bar'}],
                     [{'entity_id': 'foo', 'above': 3}, {'entity_id': 'bar'}],
                     [{'entity_id': 'baz'}],
                     [{'entity_id': 'foo', 'above': 3}],
                     [{'entity_id': 'foo', 'below': 1}, {'entity_id': 'bar'}],
                     [{'entity_id': 'bar'}, {'entity_id': 'foo', 'above': 3},
                      {'entity_id': 'baz'}],
                     [{'entity_id': 'foo', 'below': 1}],
                     [{'entity_id': 'foo', 'below': 1}, {'entity_id': 'baz'}]]

    target_result = [sorted(res, key=lambda k: k['entity_id'])
                     for res in target_result]

    assert all(sorted(res, key=lambda k: k['entity_id']) in target_result
               for res in result)
    assert all(sorted(res, key=lambda k: k['entity_id']) in result
               for res in target_result)

def test_proc_filter_target(static_bayes):
    observations = [[{'entity_id': 'foo', 'below': 1},
                    {'entity_id': 'bar'},],
                    [{'entity_id': 'foo', 'above': 3},],
                    [{'entity_id': 'baz'}]]

    result = static_bayes.filter_target(observations,
                                        {'entity_id': 'foo', 'below': 1})

    assert list(result) == [[{'entity_id': 'foo', 'below': 1},
                             {'entity_id': 'bar'},]]

def test_probability_updates(static_bayes):
        """Test probability update function."""
        prob_true = [0.3, 0.6, 0.8]
        prob_false = [0.7, 0.4, 0.2]
        prior = 0.5

        for pt, pf in zip(prob_true, prob_false):
            prior = static_bayes.update_probability(prior, pt, pf)

        assert prior == 0.720000

        prob_true = [0.8, 0.3, 0.9]
        prob_false = [0.6, 0.4, 0.2]
        prior = 0.7

        for pt, pf in zip(prob_true, prob_false):
            prior = static_bayes.update_probability(prior, pt, pf)

        assert prior == 0.9130434782608695

def test_proc_sensors_from_parsed_yaml(static_bayes):
    multi_yaml = [{'platform': 'foo'},
                  {'platform': 'bayesian',
                   'entity_id': 'sensor1'},
                  {'platform': 'bar'},
                  {'platform': 'bayesian',
                   'entity_id': 'sensor2'},
                  ]

    result = static_bayes.sensors_from_parsed_yaml(multi_yaml, None)
    assert result == [{'platform': 'bayesian', 'entity_id': 'sensor1'},
                      {'platform': 'bayesian', 'entity_id': 'sensor2'}]

    result = static_bayes.sensors_from_parsed_yaml(multi_yaml, 0)
    assert result == [{'platform': 'bayesian', 'entity_id': 'sensor1'}]

    single_yaml = {'platform': 'bayesian', 'entity_id': 'sensor2'}
    result = static_bayes.sensors_from_parsed_yaml(single_yaml, None)
    assert result == [{'platform': 'bayesian', 'entity_id': 'sensor2'}]

    single_yaml = {'platform': 'foo'}
    result = static_bayes.sensors_from_parsed_yaml(single_yaml, None)
    assert result == []

    result = static_bayes.sensors_from_parsed_yaml('not a list or dict', None)
    assert result == []

