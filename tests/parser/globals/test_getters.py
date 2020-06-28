import pytest


def test_state_accessor(get_contract_with_gas_estimation_for_constants):
    state_accessor = """
y: HashMap[int128, int128]

@public
def oo():
    self.y[3] = 5

@public
def foo() -> int128:
    return self.y[3]

    """

    c = get_contract_with_gas_estimation_for_constants(state_accessor)
    c.oo(transact={})
    assert c.foo() == 5


# TODO: Either wait for this, or refactor test suite to use Brownie
#       (which doesn't suffer from this issue)
@pytest.mark.xfail(reason="https://github.com/ethereum/web3.py/issues/1634#issuecomment-650797252")
def test_getter_code(get_contract_with_gas_estimation_for_constants):
    getter_code = """
struct W:
    a: uint256
    b: int128[7]
    c: bytes[100]
    e: int128[3][3]
    f: uint256
    g: uint256
x: public(uint256)
y: public(int128[5])
z: public(bytes[100])
w: public(HashMap[int128, W])

@public
def __init__():
    self.x = as_wei_value(7, "wei")
    self.y[1] = 9
    self.z = b"cow"
    self.w[1].a = 11
    self.w[1].b[2] = 13
    self.w[1].c = b"horse"
    self.w[2].e[1][2] = 17
    self.w[3].f = 750
    self.w[3].g = 751
    """

    c = get_contract_with_gas_estimation_for_constants(getter_code)
    assert c.x() == 7
    assert c.y(1) == 9
    assert c.z() == b"cow"
    assert c.w(1)[0] == 11  # W.a
    assert c.w(1)[1][2] == 13  # W.b[2]
    assert c.w(1)[2] == b"horse"  # W.c
    assert c.w(2)[3][1][2] == 17  # W.e[1][2]
    assert c.w(3)[4] == 750  # W.f
    assert c.w(3)[5] == 751  # W.g
