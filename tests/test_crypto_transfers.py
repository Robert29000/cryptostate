import brownie
from brownie.convert import to_bytes


def test_transfer(accounts, cryptostate):
    cryptostate.submitAddress(accounts[5], to_bytes('0xffff'), {'from': accounts[0]})
    cryptostate.submitAddress(accounts[6], to_bytes('0xffff'), {'from': accounts[1]})

    cryptostate.confirmAddress(0, {'from': accounts[1]})
    cryptostate.confirmAddress(1, {'from': accounts[2]})

    assert cryptostate.kyc_addrs(accounts[5])
    assert cryptostate.kyc_addrs(accounts[6])

    assert cryptostate.balances(accounts[5]) == 0
    assert cryptostate.balances(accounts[6]) == 0

    cryptostate.transfer(accounts[5], 10, {'from': accounts[0]})
    cryptostate.transfer(accounts[6], 100, {'from': accounts[0]})

    assert cryptostate.balances(accounts[5])  == 10
    assert cryptostate.balances(accounts[6])  == 100
    assert cryptostate.balances(accounts[0])  == 890
    
    cryptostate.transfer(accounts[5], 50, {'from': accounts[6]})

    assert cryptostate.balances(accounts[5])  == 60
    assert cryptostate.balances(accounts[6])  == 50



def test_transfer_reverts(accounts, cryptostate):
    cryptostate.submitAddress(accounts[5], to_bytes('0xffff'), {'from': accounts[0]})
    cryptostate.submitAddress(accounts[6], to_bytes('0xffff'), {'from': accounts[1]})

    cryptostate.confirmAddress(0, {'from': accounts[1]})

    with brownie.reverts():
        cryptostate.transfer(accounts[6], 100, {'from': accounts[0]})
        cryptostate.transfer(accounts[5], 1000, {'from': accounts[7]})
        cryptostate.transfer(accounts[5], 10000, {'from': accounts[2]})
        cryptostate.transfer(accounts[8], 1000, {'from': accounts[8]})