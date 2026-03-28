import pytest
from messenger.control import Control, canRead, canWrite
from messenger.messages import Messages
from . import control

# TEST basic functionality of get_message()
# just my practice setting up test functions
def test_get_message_success():
    #create message object and get the messages.txt data
    manager = Messages('messages.txt')
    #get a mock message(from messages.txt) )we'll use for testing
    mock_msg = type('obj', (object,), {'get_id': lambda self: 1})()
    manager._messages = [mock_msg]

    # call get_messages using the mock_msg and verify expected results
    assert manager.get_message(1) == mock_msg


def test_get_message_failure():
    manager = Messages('messages.txt')
    mock_msg = type('obj', (object,), {'get_id': lambda self: 1})()
    manager._messages = [mock_msg]

    # calling for a message that doesn't exist, should return none
    assert manager.get_message(2) is None


# TEST security of reading and user permissions
# user >= object

def test_no_read_up_level():
    # user has 'Secret' clearance (Value 1)
    # message is Top Secret (Value 2)
    user = type('User', (object,), {'value': 1})()
    msg = type('Msg', (object,), {'value': 2})()
    assert control.canRead(user, msg) is False

def test_no_read_up_level_1():
    # user has no clearance (Value 0)
    # message is Top Secret (Value 2)
    user = type('User', (object,), {'value': 0})()
    msg = type('Msg', (object,), {'value': 2})()
    assert control.canRead(user, msg) is False


def test_can_read_same_level():
    # user has 'Secret' clearance (Value1)
    # message has 'Secret' clearance (Value1)
    user = type('User', (object,), {'value': 1})()
    msg = type('Msg', (object,), {'value': 1})()
    assert control.canRead(user, msg) is True

def test_can_read_down_level():
    # user has 'Top Secret' clearance (Value2)
    # message is 'Secret' clearance (Value1)
    user = type('User', (object,), {'value': 2})()
    msg = type('Msg', (object,), {'value': 1})()
    assert control.canRead(user, msg) is True

#TEST security of writing and user permission
# user <= object

def test_can_write_same_level():
    # user has 'Secret' clearance (value2)
    # message is 'Secret' clearance (value2)
    user = type('User', (object,), {'value': 2})()
    msg = type('Msg', (object,), {'value': 2})()
    assert control.canWrite(user, msg) is True

def test_can_write_up_level():
    # user has 'Secret' clearance (value1)
    # message is 'Top Secret' clearance (value2)
    user = type('User', (object,), {'value': 1})()
    msg = type('Msg', (object,), {'value': 2})()
    assert control.canWrite(user, msg) is True

def test_no_write_down():
    # user has 'Secret' clearance (value1)
    # message is no clearance (value0)
    user = type('User', (object,), {'value': 1})()
    msg = type('Msg', (object,), {'value': 0})()
    assert control.canWrite(user, msg) is False

#TEST for control class
def test_read_secret_as_secret():
    assert canRead(Control.Secret, Control.Secret) is True

def test_read_public_as_secret():
    assert canRead(Control.Secret, Control.Public) is True

def test_read_secret_as_public():
    assert canRead(Control.Public, Control.Secret) is False

def test_write_public_as_public():
    assert canWrite(Control.Public, Control.Public) is True

def test_write_secret_as_public():
    assert canWrite(Control.Public, Control.Secret) is True

def test_write_public_as_secret():
    assert canWrite(Control.Secret, Control.Public) is False