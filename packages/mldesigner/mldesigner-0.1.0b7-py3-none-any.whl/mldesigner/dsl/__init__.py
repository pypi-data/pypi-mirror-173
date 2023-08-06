# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

from mldesigner._exceptions import UserErrorException

from ._condition_output import _condition_output as condition_output

try:
    from azure.ai.ml.dsl._condition import condition
    from azure.ai.ml.dsl._do_while import do_while
    from azure.ai.ml.dsl._parameter_group_decorator import parameter_group
except ImportError as e:
    err_msg = f"Please install extra dependencies by running `pip install azure-ai-ml`, currently got {e}"
    raise UserErrorException(err_msg)

__all__ = ["do_while", "condition", "condition_output", "parameter_group"]  # pylint: disable=naming-mismatch
