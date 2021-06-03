import brownie

def test_constructor_require(accounts, MultiOwnable):
    owners = [ accounts[0], accounts[1], accounts[2] ]
    multi = MultiOwnable.deploy(owners, 2, {'from': accounts[0]})

    assert multi.isOwner(accounts[0])
    assert multi.isOwner(accounts[1])
    assert multi.isOwner(accounts[2])

    assert multi.required() == 2

    with brownie.reverts():
        MultiOwnable.deploy(owners, 0, {'from': accounts[0]})
        MultiOwnable.deploy(owners, 4, {'from': accounts[0]})
        MultiOwnable.deploy({}, 2, {'from': accounts[0]})