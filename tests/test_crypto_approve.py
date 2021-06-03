import brownie
from brownie.convert import to_bytes


def test_approve(accounts, cryptostate):
    cryptostate.submitAddress(accounts[5], to_bytes('0xffff'), {'from': accounts[0]})
    cryptostate.submitAddress(accounts[6], to_bytes('0xffff'), {'from': accounts[1]})

    cryptostate.confirmAddress(0, {'from': accounts[1]})
    cryptostate.confirmAddress(1, {'from': accounts[2]})

    cryptostate.transfer(accounts[5], 200, {'from': accounts[0]})
    cryptostate.transfer(accounts[6], 100, {'from': accounts[0]})

    cryptostate.approve(accounts[6], 50, {'from': accounts[5]})
    cryptostate.approve(accounts[0], 70, {'from': accounts[5]})

    assert cryptostate.allowed(accounts[5], accounts[6]) == 50
    assert cryptostate.allowed(accounts[5], accounts[0]) == 70

    cryptostate.approve(accounts[0], 0, {'from': accounts[5]})

    assert cryptostate.allowed(accounts[5], accounts[0]) == 0

    cryptostate.approve(accounts[0], 100, {'from': accounts[5]})

    assert cryptostate.allowed(accounts[5], accounts[0]) == 100


def test_approve_reverts(accounts, cryptostate):
    cryptostate.submitAddress(accounts[5], to_bytes('0xffff'), {'from': accounts[0]})
    cryptostate.submitAddress(accounts[6], to_bytes('0xffff'), {'from': accounts[1]})

    cryptostate.confirmAddress(0, {'from': accounts[1]})
    cryptostate.confirmAddress(1, {'from': accounts[2]})

    cryptostate.transfer(accounts[5], 200, {'from': accounts[0]})
    cryptostate.transfer(accounts[6], 100, {'from': accounts[0]})

    cryptostate.approve(accounts[6], 50, {'from': accounts[5]})

    with brownie.reverts():
        cryptostate.approve(accounts[7], 10, {'from': accounts[5]})
        cryptostate.approve(accounts[0], 100, {'from': accounts[9]})
        cryptostate.approve(accounts[6], 70, {'from': accounts[5]})


def test_transfer_from(accounts, cryptostate):
    cryptostate.submitAddress(accounts[5], to_bytes('0xffff'), {'from': accounts[0]})
    cryptostate.submitAddress(accounts[6], to_bytes('0xffff'), {'from': accounts[1]})

    cryptostate.confirmAddress(0, {'from': accounts[1]})
    cryptostate.confirmAddress(1, {'from': accounts[2]})

    cryptostate.transfer(accounts[5], 200, {'from': accounts[0]})
    cryptostate.transfer(accounts[6], 100, {'from': accounts[0]})

    cryptostate.approve(accounts[6], 50, {'from': accounts[5]})
    cryptostate.approve(accounts[0], 70, {'from': accounts[5]})

    cryptostate.transferFrom(accounts[5], accounts[2], 10, {'from': accounts[6]})

    assert cryptostate.allowed(accounts[5], accounts[6]) == 40
    assert cryptostate.balances(accounts[5]) == 190
    assert cryptostate.balances(accounts[2]) == 5010
    assert cryptostate.balances(accounts[6]) == 100

    cryptostate.transferFrom(accounts[5], accounts[1], 60, {'from': accounts[0]})

    assert cryptostate.allowed(accounts[5], accounts[0]) == 10
    assert cryptostate.balances(accounts[5]) == 130
    assert cryptostate.balances(accounts[2]) == 5010
    assert cryptostate.balances(accounts[1]) == 2060
    assert cryptostate.balances(accounts[0]) == 700


def test_transfer_from_reverts(accounts, cryptostate):
    cryptostate.submitAddress(accounts[5], to_bytes('0xffff'), {'from': accounts[0]})
    cryptostate.submitAddress(accounts[6], to_bytes('0xffff'), {'from': accounts[1]})

    cryptostate.confirmAddress(0, {'from': accounts[1]})
    cryptostate.confirmAddress(1, {'from': accounts[2]})

    cryptostate.transfer(accounts[5], 200, {'from': accounts[0]})
    cryptostate.transfer(accounts[6], 100, {'from': accounts[0]})

    cryptostate.approve(accounts[6], 50, {'from': accounts[5]})
    cryptostate.approve(accounts[0], 70, {'from': accounts[5]})

    with brownie.reverts():
        cryptostate.transferFrom(accounts[5], accounts[0], 10, {'from': accounts[8]})
        cryptostate.transferFrom(accounts[5], accounts[3], 40, {'from': accounts[6]})
        cryptostate.transferFrom(accounts[5], accounts[1], 60, {'from': accounts[6]})
        cryptostate.transferFrom(accounts[8], accounts[1], 60, {'from': accounts[6]})