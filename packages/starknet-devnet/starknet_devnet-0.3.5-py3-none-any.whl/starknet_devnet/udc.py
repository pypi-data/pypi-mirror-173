"""UDC and its constants"""

from starkware.python.utils import to_bytes
from starkware.solidity.utils import load_nearby_contract
from starkware.starknet.services.api.contract_class import ContractClass
from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.starknet import Starknet


class UDC:
    """UDC wrapper class"""

    CONTRACT_CLASS: ContractClass = None  # loaded lazily

    # Precalculated
    # HASH = to_bytes(compute_class_hash(contract_class=UDC.get_contract_class()))
    HASH = 3484004124736344420122298338254154090450773688458934993781007232228755339881
    HASH_BYTES = to_bytes(HASH)

    # Precalculated to fixed address
    # ADDRESS = calculate_contract_address_from_hash(salt=10, class_hash=HASH,
    # constructor_calldata=[], deployer_address=0)
    ADDRESS = (
        1073880354184614071153542798898672284640862493126523554954769603345737026102
    )

    contract: StarknetContract = None

    def __init__(self, starknet_wrapper):
        self.starknet_wrapper = starknet_wrapper

    @classmethod
    def get_contract_class(cls):
        """Returns contract class via lazy loading."""
        if not cls.CONTRACT_CLASS:
            cls.CONTRACT_CLASS = ContractClass.load(
                load_nearby_contract("UDC_OZ_0.5.0")
            )
        return cls.CONTRACT_CLASS

    async def deploy(self):
        """Deploy token contract for charging fees."""
        starknet: Starknet = self.starknet_wrapper.starknet
        contract_class = UDC.get_contract_class()

        await starknet.state.state.set_contract_class(UDC.HASH_BYTES, contract_class)
        await starknet.state.state.deploy_contract(UDC.ADDRESS, UDC.HASH_BYTES)

        self.contract = StarknetContract(
            state=starknet.state,
            abi=contract_class.abi,
            contract_address=UDC.ADDRESS,
            deploy_call_info=None,
        )

        await self.starknet_wrapper.store_contract(
            UDC.ADDRESS, self.contract, contract_class
        )
