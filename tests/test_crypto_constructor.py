import brownie 


def test_constructor(accounts, cryptostate):

    assert cryptostate.kyc_addrs(accounts[0])
    assert cryptostate.kyc_addrs(accounts[1]) 
    assert cryptostate.kyc_addrs(accounts[2])
    assert not cryptostate.kyc_addrs(accounts[4])

    assert cryptostate.balances(accounts[0]) == 1000
    assert cryptostate.balances(accounts[1]) == 2000
    assert cryptostate.balances(accounts[2]) == 5000


def test_constructor_reverts(accounts, CryptoState):
    owners = [ accounts[0], accounts[1], accounts[2], accounts[3]]
    supplies = [ 1000, 5000, 4000]
    with brownie.reverts():
        CryptoState.deploy("Token", "Tkn", 18, owners, supplies, 2, {'from': accounts[0]})
        supplies.push(10000)
        CryptoState.deploy("Token", "Tkn", 18, owners, supplies, 5, {'from': accounts[0]})