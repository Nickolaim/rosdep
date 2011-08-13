# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Willow Garage, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

def test_InvalidRosdepData():
    from rosdep.model import InvalidRosdepData
    try:
        raise InvalidRosdepData('hi')
    except InvalidRosdepData as ex:
        assert 'hi' in str(ex)

def test_RosdepDatabaseEntry():
    # not muich to test with container
    from rosdep.model import RosdepDatabaseEntry
    d = RosdepDatabaseEntry({'a': 1}, [], 'foo')
    assert d.rosdep_data == {'a': 1}
    assert d.stack_dependencies == []
    assert d.origin == 'foo'

def test_RosdepDatabase():
    from rosdep.model import RosdepDatabase

    db = RosdepDatabase()
    assert not db.is_loaded('foo')

    data = {'a': 1}
    db.set_stack_data('foo', data, [], 'origin1')
    assert db.is_loaded('foo')    
    entry = db.get_stack_data('foo')
    assert entry.rosdep_data == data
    assert entry.origin == 'origin1'
    assert entry.stack_dependencies == []
    # make sure data is copy
    data['a'] = 2
    assert entry.rosdep_data != data
    
    data = {'b': 2}
    db.set_stack_data('bar', data, ['foo'], 'origin2')
    assert db.is_loaded('bar')    
    entry = db.get_stack_data('bar')
    assert entry.rosdep_data == data
    assert entry.origin == 'origin2'
    assert entry.stack_dependencies == ['foo']

    # override entry for bar
    data = {'b': 3}
    assert db.is_loaded('bar')    
    db.set_stack_data('bar', data, ['baz', 'blah'], 'origin3')
    assert db.is_loaded('bar')    
    entry = db.get_stack_data('bar')
    assert entry.rosdep_data == data
    assert entry.origin == 'origin3'
    assert set(entry.stack_dependencies) == set(['baz', 'blah'])
    