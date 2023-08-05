"""Manages the federated communication and training of models.

Federated algorithm plugins can also be imported from this package.
"""
import importlib as _importlib
import inspect as _inspect
import pkgutil as _pkgutil
from typing import List

from bitfount.config import (
    BITFOUNT_FEDERATED_PLUGIN_PATH as _BITFOUNT_FEDERATED_PLUGIN_PATH,
)
from bitfount.federated import algorithms
from bitfount.federated.aggregators.aggregator import Aggregator
from bitfount.federated.aggregators.secure import SecureAggregator
from bitfount.federated.algorithms.base import BaseAlgorithmFactory
from bitfount.federated.algorithms.column_avg import ColumnAverage
from bitfount.federated.algorithms.compute_intersection_rsa import (
    ComputeIntersectionRSA,
)
from bitfount.federated.algorithms.model_algorithms.evaluate import ModelEvaluation
from bitfount.federated.algorithms.model_algorithms.federated_training import (
    FederatedModelTraining,
)
from bitfount.federated.algorithms.model_algorithms.inference import ModelInference
from bitfount.federated.algorithms.model_algorithms.train_and_evaluate import (
    ModelTrainingAndEvaluation,
)
from bitfount.federated.algorithms.private_sql_query import PrivateSqlQuery
from bitfount.federated.algorithms.sql_query import SqlQuery
from bitfount.federated.authorisation_checkers import IdentityVerificationMethod
from bitfount.federated.early_stopping import FederatedEarlyStopping
from bitfount.federated.exceptions import (
    AggregatorError,
    BitfountTaskStartError,
    DecryptError,
    EncryptError,
    EncryptionError,
    MessageHandlerNotFoundError,
    MessageRetrievalError,
    PodConnectFailedError,
    PodNameError,
    PodRegistrationError,
    PrivateSqlError,
    SecureShareError,
)
from bitfount.federated.helper import combine_pod_schemas
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.modeller import _Modeller
from bitfount.federated.pod import Pod
from bitfount.federated.pod_keys_setup import PodKeys
from bitfount.federated.privacy.differential import DPModellerConfig, DPPodConfig
from bitfount.federated.protocols.model_protocols.federated_averaging import (
    FederatedAveraging,
)
from bitfount.federated.protocols.psi import PrivateSetIntersection
from bitfount.federated.protocols.results_only import ResultsOnly
from bitfount.federated.roles import Role
from bitfount.federated.secure import SecureShare
from bitfount.federated.shim import BackendTensorShim
from bitfount.federated.transport import MAXIMUM_GRPC_MESSAGE_SIZE_BYTES
from bitfount.federated.transport.config import (
    PRODUCTION_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.federated.types import AggregatorType, AlgorithmType, ProtocolType
from bitfount.utils import _get_module_from_file

_logger = _get_federated_logger(__name__)

__all__: List[str] = [
    "Aggregator",
    "AggregatorError",
    "AggregatorType",
    "AlgorithmType",
    "BackendTensorShim",
    "BitfountModelReference",
    "BitfountTaskStartError",
    "ColumnAverage",
    "DPModellerConfig",
    "DPPodConfig",
    "DecryptError",
    "EncryptError",
    "EncryptionError",
    "FederatedAveraging",
    "FederatedEarlyStopping",
    "FederatedModelTraining",
    "IdentityVerificationMethod",
    "MAXIMUM_GRPC_MESSAGE_SIZE_BYTES",
    "MessageHandlerNotFoundError",
    "MessageRetrievalError",
    "MessageServiceConfig",
    "ModelEvaluation",
    "ModelInference",
    "ModelTrainingAndEvaluation",
    "_Modeller",
    "Pod",
    "PodConnectFailedError",
    "PodKeys",
    "PodNameError",
    "PodRegistrationError",
    "PrivateSetIntersection",
    "PrivateSqlError",
    "PrivateSqlQuery",
    "ProtocolType",
    "PRODUCTION_MESSAGE_SERVICE_URL",
    "ResultsOnly",
    "Role",
    "ComputeIntersectionRSA",
    "SecureAggregator",
    "SecureShare",
    "SecureShareError",
    "SqlQuery",
    "combine_pod_schemas",
]

# Import all concrete implementations of BaseAlgorithmFactory in the algorithms
# subdirectory as well as algorithms plugins

for _module_info in _pkgutil.walk_packages(
    path=algorithms.__path__ + [str(_BITFOUNT_FEDERATED_PLUGIN_PATH / "algorithms")],
):
    try:
        _module = _importlib.import_module(f"{algorithms.__name__}.{_module_info.name}")
    # Also catches `ModuleNotFoundError` which subclasses `ImportError`
    # Try to import the module from the plugin directory if it's not found in the
    # algorithms directory
    except ImportError:
        try:
            _module = _get_module_from_file(
                _BITFOUNT_FEDERATED_PLUGIN_PATH
                / "algorithms"
                / f"{_module_info.name}.py",
            )
        except ImportError:
            _logger.debug(f"Error importing module {_module_info.name}")
    finally:
        for _, cls in _inspect.getmembers(_module, _inspect.isclass):
            if issubclass(cls, BaseAlgorithmFactory) and not _inspect.isabstract(cls):
                globals().update({cls.__name__: getattr(_module, cls.__name__)})
                __all__.append(cls.__name__)
            # There are too many false positives if we don't restrict classes to those
            # that inherit from BaseAlgorithmFactory for it to be a useful log message
            elif (
                issubclass(cls, BaseAlgorithmFactory)
                and cls.__name__ != "BaseAlgorithmFactory"
            ):
                _logger.debug(
                    f"Found class {cls.__name__} in module {_module_info.name} which "
                    f"did not fully implement BaseAlgorithmFactory. Skipping."
                )


# See top level `__init__.py` for an explanation
__pdoc__ = {}
for _obj in __all__:
    __pdoc__[_obj] = False
