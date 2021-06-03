import pytest

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # выполнять откат цепи после завершения каждого теста, чтобы обеспечить надлежащую изоляцию
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def multiownable(MultiOwnable, accounts):
    owners = [ accounts[0], accounts[1], accounts[2] ]
    return MultiOwnable.deploy(owners, 2, {'from': accounts[0]})


@pytest.fixture(scope="module")
def cryptostate(CryptoState, accounts):
    owners = [accounts[0], accounts[1], accounts[2]]
    initialSupplies = [ 1000, 2000, 5000 ]
    return CryptoState.deploy("Digital", "DG", 18, owners, initialSupplies, 2, {'from': accounts[0]})