"""
RPC types
"""

from enum import Enum
from typing import Union, List
from typing_extensions import Literal, TypedDict

from starkware.starknet.services.api.feeder_gateway.response_objects import BlockStatus


Felt = str

BlockHash = Felt
BlockNumber = int
BlockTag = Literal["latest", "pending"]

Signature = List[Felt]


class BlockHashDict(TypedDict):
    """TypedDict class for BlockId with block hash"""

    block_hash: BlockHash


class BlockNumberDict(TypedDict):
    """TypedDict class for BlockId with block number"""

    block_number: BlockNumber


BlockId = Union[BlockHashDict, BlockNumberDict, BlockTag]

TxnStatus = Literal["PENDING", "ACCEPTED_ON_L2", "ACCEPTED_ON_L1", "REJECTED"]

RpcBlockStatus = Literal["PENDING", "ACCEPTED_ON_L2", "ACCEPTED_ON_L1", "REJECTED"]


def rpc_block_status(block_status: BlockStatus) -> RpcBlockStatus:
    """
    Convert gateway BlockStatus to RpcBlockStatus
    """
    block_status_map = {
        "PENDING": "PENDING",
        "ABORTED": "REJECTED",
        "REVERTED": "REJECTED",
        "ACCEPTED_ON_L2": "ACCEPTED_ON_L2",
        "ACCEPTED_ON_L1": "ACCEPTED_ON_L1",
    }
    return block_status_map[block_status]


TxnHash = Felt
Address = Felt
NumAsHex = str

# Pending transactions will not be supported since it
# doesn't make much sense with the current implementation of devnet
TxnType = Literal["DECLARE", "DEPLOY", "INVOKE", "L1_HANDLER"]


def rpc_txn_type(transaction_type: str) -> TxnType:
    """
    Convert gateway transaction type to RPC TxnType
    """
    txn_type_map = {
        "DEPLOY": "DEPLOY",
        "DECLARE": "DECLARE",
        "INVOKE_FUNCTION": "INVOKE",
        "L1_HANDLER": "L1_HANDLER",
    }
    if transaction_type not in txn_type_map:
        raise RpcError(
            code=-1,
            message=f"Current implementation does not support {transaction_type} transaction type",
        )
    return txn_type_map[transaction_type]


class RpcError(Exception):
    """
    Error message returned by rpc
    """

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


class RpcErrorCode(Enum):
    """
    Constants used in JSON-RPC protocol
    https://www.jsonrpc.org/specification
    """

    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
