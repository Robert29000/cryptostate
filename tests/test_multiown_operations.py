import brownie
from brownie.convert import to_bytes



def test_submit_operation(accounts, multiownable):
    multiownable.submitOperation(to_bytes('0xffe5b'), {'from': accounts[0]})
    
    assert multiownable.operationCount() == 1
    assert multiownable.confirmations(0, accounts[0])
    assert not multiownable.confirmations(0, accounts[1])
    assert not multiownable.operations(0)[1]

    with brownie.reverts():
        multiownable.submitOperation(to_bytes('0xffe76'), {'from': accounts[5]})


def test_confirm_operation(accounts, multiownable):
    multiownable.submitOperation(to_bytes('0xbb'), {'from': accounts[0]})

    multiownable.confirmOperation(0, {'from': accounts[2]})

    assert multiownable.confirmations(0, accounts[0])
    assert multiownable.confirmations(0, accounts[2])
    assert not multiownable.confirmations(0, accounts[1])
    assert multiownable.operations(0)[1]


def test_confirm_operation_reverts(accounts, multiownable):
    multiownable.submitOperation(to_bytes('0xbae'), {'from': accounts[0]})

    with brownie.reverts():
        multiownable.confirmOperation(0, {'from': accounts[3]})
        multiownable.confirmOperation(2, {'from': accounts[0]})
        multiownable.confirmOperation(0, {'from': accounts[0]})
