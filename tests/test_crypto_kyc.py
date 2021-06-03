import brownie 
from brownie.convert import to_bytes


def test_submit_address(accounts, cryptostate):
    cryptostate.submitAddress(accounts[5], to_bytes('0xffff'), {'from': accounts[0]})
    
    assert cryptostate.address_operations(0) == accounts[5]
    assert cryptostate.wait_for_confirmations(accounts[5])
    assert not cryptostate.kyc_addrs(accounts[5])

    with brownie.reverts():
        cryptostate.submitAddress(accounts[6], to_bytes('0xfff'), {'from': accounts[5]})
        cryptostate.submitAddress(accounts[1], to_bytes('0xfff'), {'from': accounts[0]})
        cryptostate.submitAddress(accounts[5], to_bytes('0xfff'), {'from': accounts[0]})


def test_confirm_address(accounts, cryptostate):
    cryptostate.submitAddress(accounts[5], to_bytes('0xffff'), {'from': accounts[0]})

    cryptostate.confirmAddress(0, {'from': accounts[1]})

    assert cryptostate.kyc_addrs(accounts[5])
    assert not cryptostate.wait_for_confirmations(accounts[5])

    with brownie.reverts():
        cryptostate.confirmAddress(0, {'from': accounts[6]})
        cryptostate.confirmAddress(1, {'from': accounts[0]})
