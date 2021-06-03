import brownie


def test_add_owner(accounts, multiownable):
    multiownable.addOwner(accounts[4], {'from': accounts[0]})

    assert multiownable.isOwner(accounts[4])
    assert multiownable.owners(3) == accounts[4]

    with brownie.reverts():
        multiownable.addOwner(accounts[5], {'from': accounts[7]})
        multiownable.addOwner(accounts[4], {'from': accounts[0]})
        multiownable.addOwner(accounts[3], {'from': accounts[9]})


def test_remove_owner(accounts, multiownable):
    multiownable.removeOwner(accounts[1], {'from': accounts[0]})

    assert not multiownable.isOwner(accounts[1])
    assert multiownable.owners(1) == accounts[2]
    assert multiownable.owners(0) == accounts[0]
    assert multiownable.required() == 2

    multiownable.removeOwner(accounts[2], {'from': accounts[0]})
    assert multiownable.owners(0) == accounts[0]
    assert multiownable.required() == 1


def test_remove_owner_reverts(accounts, multiownable):
    with brownie.reverts():
        multiownable.removeOwner(accounts[1], {'from': accounts[4]})
        multiownable.removeOwner(accounts[5], {'from': accounts[4]})

    multiownable.removeOwner(accounts[1], {'from': accounts[0]})
    multiownable.removeOwner(accounts[2], {'from': accounts[0]})

    with brownie.reverts():
        multiownable.removeOwner(accounts[0], {'from': accounts[0]})


def test_replace_owner(accounts, multiownable):
    multiownable.replaceOwner(accounts[1], accounts[5], {'from': accounts[0]})

    assert not multiownable.isOwner(accounts[1])
    assert multiownable.isOwner(accounts[5])
    assert multiownable.owners(1) == accounts[5]

    with brownie.reverts():
        multiownable.replaceOwner(accounts[5], accounts[2], {'from': accounts[0]})
        multiownable.replaceOwner(accounts[2], accounts[7], {'from': accounts[9]})
        multiownable.replaceOwner(accounts[4], accounts[6], {'from': accounts[0]})


def test_requirement_change(accounts, multiownable):
    multiownable.changeRequirement(1, {'from': accounts[0]})

    assert multiownable.required() == 1

    with brownie.reverts():
        multiownable.changeRequirement(0, {'from': accounts[0]})
        multiownable.changeRequirement(5, {'from': accounts[0]})
        multiownable.changeRequirement(2, {'from': accounts[4]})
