"""Entrypoint for the masterful.train package."""
import os
# Must be set before importing tensorflow.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_CPP_MAX_LOG_LEVEL'] = '0'
os.environ['TF_CPP_MAX_VLOG_LEVEL'] = '0'

import argparse
import sys
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
  tf.config.experimental.set_memory_growth(gpu, True)

# Register if not running locally. Registration
# only works by using the evironment variables.
import masterful
if 'backend' not in dir(masterful) or os.environ.get('NOOP_REGISTER',
                                                     None) == '1':
  masterful = masterful.activate()
import masterful.train.trainer as trainer


def _silence_logging():
  tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

  import logging

  logging.getLogger('tensorflow').setLevel(logging.ERROR)
  logging.getLogger('absl').setLevel(logging.ERROR)
  logging.getLogger().setLevel(logging.ERROR)

  from absl import logging as absl_logging
  absl_logging.set_verbosity(absl_logging.ERROR)


_silence_logging()


def main(override=None):
  """
  Main entrypoint for the standalone version of this package.
  """
  # This script only runs under Tensorflow 2.0
  assert tf.__version__.startswith("2")

  parser = argparse.ArgumentParser(prog="masterful-train")
  parser.add_argument("--config",
                      help="Training configuration YAML file",
                      type=str,
                      required=True)
  parser.add_argument(
      "--output_path",
      help="Overrides the output path in the configuration YAML",
      type=str)
  parser.add_argument("--cache_path",
                      help="Overrides the cache path in the configuration YAML",
                      type=str)
  parser.add_argument(
      "--batch_size",
      help="Overrides the meta-learned batch size for finer control",
      type=int,
      default=-1)
  parser.add_argument(
      "--regularization_params",
      help=
      "[EXPERIMENTAL] Overrides the regularization parameters for training.",
      type=str)
  args = parser.parse_args()

  import warnings
  with warnings.catch_warnings():
    if masterful.constants.MASTERFUL_VERBOSITY < 1:
      warnings.simplefilter("ignore")
    trainer.train_from_config(
        config_path=args.config,
        output_path=args.output_path,
        cache_path=args.cache_path,
        regularization_params_path=args.regularization_params,
        batch_size=args.batch_size,
    )
  sys.exit(0)


main()