import pytest
from datetime import datetime
from testfixtures import LogCapture

# ************************** Zac *********************************


@pytest.mark.parametrize("pt_id, attending_username, pt_age",
                         [(3, 'Test.T', 52)],
                         ids=['Patient added to database'])
def test_add_patient(pt_id, attending_username, pt_age):
    from hrss_server import add_patient, init_server, pt_db
    init_server()
    original_len = len(pt_db)
    add_patient(pt_id, attending_username, pt_age)
    pt = pt_db[-1]
    assert pt['patient_id'] == pt_id
    assert pt['attending_username'] == attending_username
    assert pt['patient_age'] == pt_age
    pt_db.pop(-1)
    assert len(pt_db) == original_len


@pytest.mark.parametrize("att_username, att_email, att_phone",
                         [('Test.T', 'DrTest@my_hospital.com',
                           '919-555-1212')],
                         ids=['Attending added to database'])
def test_add_attending(att_username, att_email, att_phone):
    from hrss_server import add_attending, init_server, att_db
    init_server()
    original_len = len(att_db)
    add_attending(att_username, att_email, att_phone)
    att = att_db[-1]
    assert att['attending_username'] == att_username
    assert att['attending_email'] == att_email
    assert att['attending_phone'] == att_phone
    att_db.pop(-1)
    assert len(att_db) == original_len


@pytest.mark.parametrize("in_data, expected",
                         [({'attending_username': 'Smith.J',
                           'patient_age': 24},
                           ('Key patient_id is missing from POST data', 400)),
                          ({'patient_id': '3',
                            'attending_username': 'Doe.J',
                            'patient_age': '24'},
                          ('Patient successfully added', 200)),
                          ({'patient_id': 3,
                            'attending_username': 'Doe.J',
                            'patient_age': 24},
                          ('Patient successfully added', 200))],
                         ids=['Patient not added',
                              'Patient added numeric strings',
                              'Patient added ints'])
def test_add_new_patient_worker(in_data, expected):
    from hrss_server import add_new_patient_worker, init_server, pt_db
    init_server()
    result = add_new_patient_worker(in_data)
    # check numeric strings converted correctly
    if result[1] == 200:
        pt = pt_db[-1]
        assert type(pt['patient_id']) == int
        assert type(pt['attending_username']) == str
        assert type(pt['patient_age']) == int
    assert result == expected


@pytest.mark.parametrize("in_data, expected",
                         [([3, 'test', 24], 'POST data was not a dictionary'),
                          ({'attending_username': 'Smith.J',
                           'patient_age': 24},
                          'Key patient_id is missing from POST data'),
                          ({'patient_id': 3, 'patient_age': 24},
                          'Key attending_username is missing from POST data'),
                          ({'patient_id': 3, 'attending_username': 'Smith.J'},
                          'Key patient_age is missing from POST data'),
                          ({'patient_id': True,
                            'attending_username': 'Smith.J',
                            'patient_age': 24},
                           "Value of key patient_id is not of type(s) "
                           "[<class 'str'>, <class 'int'>]"),
                          ({'patient_id': 3,
                            'attending_username': 30,
                            'patient_age': 24},
                           "Value of key attending_username is not of type(s) "
                           "[<class 'str'>]"),
                          ({'patient_id': 3,
                            'attending_username': 'Smith.J',
                            'patient_age': False},
                           "Value of key patient_age is not of type(s) "
                           "[<class 'str'>, <class 'int'>]"),
                          ({'patient_id': '3a',
                            'attending_username': 'Smith.J',
                            'patient_age': 24},
                           'Key patient_id must be an integer or numeric '
                           'string'),
                          ({'patient_id': 3,
                            'attending_username': 'Smith.J',
                            'patient_age': '2a'},
                           'Key patient_age must be an integer or numeric '
                           'string'),
                          ({'patient_id': 1,
                            'attending_username': 'Smith.J',
                            'patient_age': '24'},
                           'Patient is already in database'),
                          ({'patient_id': '1',
                            'attending_username': 'Smith.J',
                            'patient_age': '24'},
                           'Patient is already in database'),
                          ({'patient_id': 3,
                            'attending_username': 'SmithJ',
                            'patient_age': 24},
                           'Key attending_username have format '
                           '"LastName.FirstInitial"'),
                          ({'patient_id': 3,
                            'attending_username': 'Smith..J',
                            'patient_age': 24},
                           'Key attending_username have format '
                           '"LastName.FirstInitial"'),
                          ({'patient_id': 3,
                            'attending_username': '.J',
                            'patient_age': 24},
                           'Key attending_username have format '
                           '"LastName.FirstInitial"'),
                          ({'patient_id': 3,
                            'attending_username': 'Smith.',
                            'patient_age': 24},
                           'Key attending_username have format '
                           '"LastName.FirstInitial"'),
                          ({'patient_id': 3,
                            'attending_username': 'Smith.John',
                            'patient_age': 24},
                           'Key attending_username have format '
                           '"LastName.FirstInitial"'),
                          ({'patient_id': 3,
                            'attending_username': 'Smith.K',
                            'patient_age': 24},
                           "Attending physician Smith.K not present in "
                           "physician database"),
                          ({'patient_id': '3',
                            'attending_username': 'Doe.J',
                            'patient_age': 24}, True),
                          ({'patient_id': 3,
                            'attending_username': 'Doe.J',
                            'patient_age': '24'}, True)],
                         ids=['Input not dictionary', 'Missing patient_id',
                              'Missing attending_username',
                              'Missing patient_age',
                              'Wrong patient_id type',
                              'Wrong attending username type',
                              'Wrong patient_age type',
                              'Patient_id non-numeric string',
                              'Patient age non-numeric string',
                              'Patient already in database',
                              'Patient already in database numeric string',
                              'Attending username no period',
                              'Attending username too many periods',
                              'Attending username last name empty',
                              'Attending username first initial empty',
                              'Attending username first initial too long',
                              'Attending username not in attending database',
                              'Patient_id numeric string',
                              'Patient_age numeric string'])
def test_validate_new_patient(in_data, expected):
    from hrss_server import validate_new_patient, init_server
    init_server()
    result = validate_new_patient(in_data)
    assert result == expected


@pytest.mark.parametrize("in_data, expected",
                         [({'patient_id': 1},
                           ('Key heart_rate is missing from POST data', 400)),
                          ({'patient_id': 1, 'heart_rate': 71},
                          ('Heart rate data successfully added', 200)),
                          ({'patient_id': '1', 'heart_rate': '71'},
                          ('Heart rate data successfully added', 200)),
                          ({'patient_id': 2, 'heart_rate': 150},
                          ('Heart rate data successfully added, tachycardic '
                           'email alert sent to assigned physician', 200))],
                         ids=['Heart rate not added', 'Heart rate added ints',
                              'Heart rate added numeric strings',
                              'Tachycardic heart rate added'])
def test_heart_rate_worker(in_data, expected):
    from hrss_server import heart_rate_worker, init_server, pt_db
    import datetime as dt
    init_server()
    result = heart_rate_worker(in_data)
    # check numeric strings converted correctly
    if result[1] == 200:
        pt = pt_db[-1]
        assert type(pt['heart_rate']) == list
        assert type(pt['heart_rate'][-1]) == int
        assert type(pt['heart_rate_timestamp']) == list
        assert isinstance(pt['heart_rate_timestamp'][-1], dt.date)
        assert type(pt['status']) == str
    assert result == expected


@pytest.mark.parametrize("in_data, expected",
                         [([1, 95], 'POST data was not a dictionary'),
                          ({'heart_rate': 95},
                          'Key patient_id is missing from POST data'),
                          ({'patient_id': 1},
                          'Key heart_rate is missing from POST data'),
                          ({'patient_id': True, 'heart_rate': 95},
                           "Value of key patient_id is not of type(s) "
                           "[<class 'str'>, <class 'int'>]"),
                          ({'patient_id': 1, 'heart_rate': True},
                           "Value of key heart_rate is not of type(s) "
                           "[<class 'str'>, <class 'int'>]"),
                          ({'patient_id': '1a', 'heart_rate': 95},
                           'Key patient_id must be an integer or numeric '
                           'string'),
                          ({'patient_id': 1, 'heart_rate': '95b'},
                           'Key heart_rate must be an integer or numeric '
                           'string'),
                          ({'patient_id': 3, 'heart_rate': 95},
                           'ID 3 not in patient database'),
                          ({'patient_id': '3', 'heart_rate': 95},
                           'ID 3 not in patient database'),
                          ({'patient_id': '2', 'heart_rate': 64}, True),
                          ({'patient_id': 2, 'heart_rate': '64'}, True)],
                         ids=['Input not dictionary', 'Missing patient_id',
                              'Missing heart_rate',
                              'Wrong patient_id type',
                              'Wrong heart_rate type',
                              'Patient_id non-numeric string',
                              'Heart_rate non-numeric string',
                              'Patient not in database',
                              'Patient not in database numeric string',
                              'Patient_id numeric string',
                              'Heart_rate numeric string'])
def test_validate_heart_rate(in_data, expected):
    from hrss_server import validate_heart_rate, init_server
    init_server()
    result = validate_heart_rate(in_data)
    assert result == expected


@pytest.mark.parametrize("pt_id, heart_rate, expected",
                         [(2, 105, True), (1, 90, False)],
                         ids=['Tachycaridc addition',
                              'Non-tachycardic addition'])
def test_add_heart_rate(pt_id, heart_rate, expected):
    from hrss_server import (add_heart_rate, find_pt, is_tachycardic,
                             init_server)
    init_server()
    pt = find_pt(pt_id)
    original_len = len(pt['heart_rate'])
    if is_tachycardic(pt['patient_age'], heart_rate):
        tachy_str = 'tachycardic'
    else:
        tachy_str = 'not tachycardic'
    dt = datetime.now()
    email_sent = add_heart_rate(pt_id, heart_rate)
    assert pt['heart_rate'][-1] == heart_rate
    time_delta = pt['heart_rate_timestamp'][-1] - dt
    assert time_delta.seconds < 0.05
    assert pt['status'] == tachy_str
    assert len(pt['heart_rate']) == len(pt['heart_rate_timestamp'])
    pt['heart_rate'].pop(-1)
    pt['heart_rate_timestamp'].pop(-1)
    assert len(pt['heart_rate']) == original_len
    assert len(pt['heart_rate_timestamp']) == original_len
    assert email_sent == expected


@pytest.mark.parametrize("att_username, expected",
                         [('Smith.J', {'attending_username': 'Smith.J',
                                       'attending_email': 'DrSmith@my_hospital'
                                                          '.com',
                                       'attending_phone': '919-555-1212'}),
                          ('Smith.K', False)],
                         ids=['Attending in database',
                              'Attending not in database'])
def test_find_attending(att_username, expected):
    from hrss_server import find_attending, init_server
    init_server()
    result = find_attending(att_username)
    assert result == expected


@pytest.mark.parametrize("pt_id, expected",
                         [(1, {'patient_id': 1,
                               'attending_username': 'Smith.J',
                               'patient_age': 20,
                               'heart_rate': [60, 70, 80, 90, 100, 110],
                               'heart_rate_timestamp':
                               [datetime.strptime(d, '%m/%d/%y %H:%M:%S') for d
                                in ['11/04/22 23:50:05', '11/04/22 23:55:05',
                                    '11/05/22 00:00:05', '11/05/22 00:05:05',
                                    '11/05/22 00:10:05', '11/05/22 00:15:05']],
                               'status': 'tachycardic'}),
                          (3, False)],
                         ids=['Patient in database',
                              'Patient not in database'])
def test_find_pt(pt_id, expected):
    from hrss_server import find_pt, init_server
    init_server()
    result = find_pt(pt_id)
    assert result == expected


@pytest.mark.parametrize("pt_age, heart_rate, expected",
                         [(1, 152, True), (1, 151, False),
                          (2, 138, True), (3, 137, False),
                          (4, 134, True), (6, 133, False),
                          (7, 131, True), (10, 130, False),
                          (11, 120, True), (14, 119, False),
                          (15, 101, True), (20, 100, False)],
                         ids=['Under 2 tachycardic', 'Under 2 normal',
                              '2-4 tachycardic', '2-4 normal',
                              '4-7 tachycardic', '4-7 normal',
                              '7-11 tachycardic', '7-11 normal',
                              '11-15 tachycardic', '11-15 normal',
                              '>=15 tachycardic', '>=15 normal'])
def test_is_tachycardic(pt_age, heart_rate, expected):
    from hrss_server import is_tachycardic
    result = is_tachycardic(pt_age, heart_rate)
    assert result == expected


@pytest.mark.parametrize("to_email, pt_id, heart_rate, hr_dt, expected",
                         [('DrSmith@my_hospital', 1, 110, datetime.now(),
                          400),
                          ('DrSmith@my_hospital.com', 1, 110, datetime.now(),
                          200)],
                         ids=['Email not sent', 'Email succesfully sent'])
def test_email_tachy_driver(to_email, pt_id, heart_rate, hr_dt, expected):
    from hrss_server import email_tachy_driver
    _, result_code, email_data = email_tachy_driver(to_email, pt_id,
                                                    heart_rate, hr_dt)
    assert result_code == expected
    assert email_data['from_email'] == 'tachycardic-alert@hospital.com'
    assert email_data['to_email'] == to_email
    assert email_data['subject'] == f'Patient {pt_id} tachycardic'
    assert email_data['content'] == f'Patient {pt_id} classified as ' +\
                                    'tachycardic with heart rate of ' +\
                                    f'{heart_rate} at {hr_dt}'


@pytest.mark.parametrize("email_data, expected",
                         [(['test', 'test', 'test', 'test'],
                           'POST data was not a dictionary'),
                          ({'to_email': 'test', 'subject': 'test',
                            'content': 'test'},
                          'Key from_email is missing from POST data'),
                          ({'from_email': 'test', 'subject': 'test',
                            'content': 'test'},
                          'Key to_email is missing from POST data'),
                          ({'from_email': 'test', 'to_email': 'test',
                            'content': 'test'},
                          'Key subject is missing from POST data'),
                          ({'from_email': 'test', 'to_email': 'test',
                            'subject': 'test'},
                          'Key content is missing from POST data'),
                          ({'from_email': 1, 'to_email': 'test',
                            'subject': 'test', 'content': 'test'},
                           "Value of key from_email is not of type(s) "
                           "[<class 'str'>]"),
                          ({'from_email': 'test', 'to_email': 2,
                            'subject': 'test', 'content': 'test'},
                           "Value of key to_email is not of type(s) "
                           "[<class 'str'>]"),
                          ({'from_email': 'test', 'to_email': 'test',
                            'subject': True, 'content': 'test'},
                           "Value of key subject is not of type(s) "
                           "[<class 'str'>]"),
                          ({'from_email': 'test', 'to_email': 'test',
                            'subject': 'test', 'content': False},
                           "Value of key content is not of type(s) "
                           "[<class 'str'>]"),
                          ({'from_email': 'test_test.com',
                            'to_email': 'test@test_test.com',
                            'subject': 'test', 'content': 'test'},
                           'Emails must be of the form '
                           '<name>@<domain>.<suffix>'),
                          ({'from_email': 'test@test_test.com',
                            'to_email': 'test@test_test',
                            'subject': 'test', 'content': 'test'},
                           'Emails must be of the form '
                           '<name>@<domain>.<suffix>'),
                          ({'from_email': 'test@test_test.com',
                            'to_email': 'test@test_test.com',
                            'subject': 'test', 'content': 'test'}, True)],
                         ids=['Input not dictionary', 'Missing from_email',
                              'Missing to_email', 'Missing subject',
                              'Missing content', 'Wrong to_email type',
                              'Wrong from_email type', 'Wrong subject type',
                              'Wrong content type',
                              'Invalid to_email format',
                              'Invalid from_email format',
                              'Valid email data'])
def test_validate_email_data(email_data, expected):
    from hrss_server import validate_email_data
    result = validate_email_data(email_data)
    assert result == expected


@pytest.mark.parametrize("email, expected",
                         [('DrSmith@my_hospital.com', True),
                          ('DrSmithmy_hospital.com', False),
                          ('DrSmith@my_hospitalcom', False),
                          ('DrSmith@my_hospital.', False),
                          ('@my_hospital.com', False),
                          ('DrSmith@.com', False)],
                         ids=['Valid email', 'Invalid email no @',
                              'Invalid email .', 'Invalid email no suffix',
                              'Invalid email no name',
                              'Invalid email no domain'])
def test_check_email_format(email, expected):
    from hrss_server import check_email_format
    result = check_email_format(email)
    assert result == expected


@pytest.mark.parametrize("pt_id, expected",
                         [('1', ([60, 70, 80, 90, 100, 110], 200)),
                          ('2', ([65, 75, 85, 95], 200)),
                          ('3', ('ID 3 not in patient database', 400))],
                         ids=['Patient 1 in database',
                              'Patient 2 in database',
                              'Patient not in database'])
def test_get_pt_heart_rate_worker(pt_id, expected):
    from hrss_server import get_pt_heart_rate_worker
    result = get_pt_heart_rate_worker(pt_id)
    assert result == expected


@pytest.mark.parametrize("pt_id, expected",
                         [('1a', 'Patient ID in request must be a numeric '
                          'string'),
                          ('3', 'ID 3 not in patient database'),
                          ('1', True)],
                         ids=['ID non-numeric string',
                              'ID not in database',
                              'ID in database and numeric stirng'])
def test_validate_pt_id(pt_id, expected):
    from hrss_server import validate_pt_id
    result = validate_pt_id(pt_id)
    assert result == expected


@pytest.mark.parametrize("pt_id, expected",
                         [('1', (85, 200)),
                          ('2', (80, 200)),
                          ('3', ('ID 3 not in patient database', 400)),
                          ('4', ('No heart rate measurements for patient 4',
                                 400))],
                         ids=['Patient 1 in database',
                              'Patient 2 in database',
                              'Patient not in database',
                              'Patient with no heart rate measurements'])
def test_get_avg_heart_rate_worker(pt_id, expected):
    from hrss_server import (get_avg_heart_rate_worker, init_server,
                             add_patient)
    init_server()
    if pt_id == '4':
        add_patient(int(pt_id), 'Test.T', 46)
    result = get_avg_heart_rate_worker(pt_id)
    assert result == expected


@pytest.mark.parametrize("in_list, expected",
                         [([1, 1, 1], 1),
                          ([1, 2, 4, 6], 3),
                          ([60, 72, 83, 97, 101, 112], 87)],
                         ids=['Same value', 'Avg converted to int',
                              'Values in heart rate range'])
def test_int_average(in_list, expected):
    from hrss_server import int_average
    result = int_average(in_list)
    assert result == expected


@pytest.mark.parametrize("pt_id, message",
                         [(1, 'New patient registered to database with ID 1'),
                          (2, 'New patient registered to database with ID 2')],
                         ids=['Successful logging patient 1',
                              'Successful logging patient 2'])
def test_log_new_pt(pt_id, message):
    from hrss_server import log_new_pt
    with LogCapture() as log_c:
        log_new_pt(pt_id)
    log_c.check(('root', 'INFO', message))


@pytest.mark.parametrize("att_username, att_email, message",
                         [('Smith.J', 'DrSmith@my_hospital.com',
                           'New attending physician registered with username '
                           'Smith.J and email DrSmith@my_hospital.com'),
                          ('Doe.J', 'DrDoe@my_hospital.com',
                           'New attending physician registered with username '
                           'Doe.J and email DrDoe@my_hospital.com')],
                         ids=['Successful logging attending 1',
                              'Successful logging attending 2'])
def test_log_new_att(att_username, att_email, message):
    from hrss_server import log_new_att
    with LogCapture() as log_c:
        log_new_att(att_username, att_email)
    log_c.check(('root', 'INFO', message))


@pytest.mark.parametrize("pt_id, heart_rate, att_email, message",
                         [(1, 120, 'DrSmith@my_hospital.com',
                           'Tachycardic heart rate of 120 bpm detected in '
                           'patient with ID 1. Sending alert to '
                           'DrSmith@my_hospital.com'),
                          (2, 101, 'DrDoe@my_hospital.com',
                           'Tachycardic heart rate of 101 bpm detected in '
                           'patient with ID 2. Sending alert to '
                           'DrDoe@my_hospital.com')],
                         ids=['Successful tachy logging patient 1',
                              'Successful tachy logging patient 2'])
def test_log_tachycardic(pt_id, heart_rate, att_email, message):
    from hrss_server import log_tachycardic
    with LogCapture() as log_c:
        log_tachycardic(pt_id, heart_rate, att_email)
    log_c.check(('root', 'INFO', message))


# *****************************************************************
# *****************************************************************


# ************************** Hunter *********************************
@pytest.mark.parametrize("in_data, expected",
                         [(["attending_username", "Bernier.H",
                            "attending_email", "DrBernier@my_hospital.com",
                            "attending_phone", "123-456-7890"],
                           "POST data was not a dictionary"),
                          ({"attending_username": "Bernier.H",
                            "attending_address": "123 Main St.",
                            "attending_phone": "123-456-7890"},
                           "Key attending_email is missing from POST data"),
                          ({"attending_username": "Bernier.H",
                            "attending_email": "DrBernier@my_hospital.com",
                            "attending_phone": 1234567890},
                           "Key attending_phone's value has the wrong"
                           " data type"),
                          ({"attending_username": "Smith.J",
                            "attending_email": "DrSmith@my_hospital.com",
                            "attending_phone": "919-555-1212"},
                           "Attending is already in the database"),
                          ({"attending_username": "Bernier.H",
                            "attending_email": "DrBernier@my_hospital.com",
                            "attending_phone": "123-456-7890"},
                           True)])
def test_validate_new_attending(in_data, expected):
    from hrss_server import validate_new_attending
    answer = validate_new_attending(in_data)
    assert answer == expected


@pytest.mark.parametrize("in_data, expected_message, expected_code",
                         [({"attending_username": "Bernier.Hunter",
                            "attending_address": "123 Main St.",
                            "attending_phone": "123-456-7890"},
                           "Key attending_email is missing from POST data",
                           400),
                          ({"attending_username": "Bernier.Hunter",
                            "attending_email": "DrBernier@my_hospital.com",
                            "attending_phone": "123-456-7890"},
                           "Attending successfully added", 200)])
def test_new_attending_worker(in_data, expected_message, expected_code):
    from hrss_server import new_attending_worker, validate_new_attending
    answer_message, answer_code = new_attending_worker(in_data)
    assert answer_message == expected_message, answer_code == expected_code


@pytest.mark.parametrize("in_data, expected",
                         [(["patient_id", 1,
                            "heart_rate_average_since",
                            "2018-03-09 11:00:36"],
                           "POST data was not a dictionary"),
                          ({"patient_id": 1},
                           "Key heart_rate_average_since is missing"
                           " from POST data"),
                          ({"patient_id": 1.1,
                            "heart_rate_average_since":
                            "2018-03-09 11:00:36"},
                           "Key patient_id's value has the wrong data type"),
                          ({"patient_id": 1,
                            "heart_rate_average_since":
                            20180309110036},
                           "Key heart_rate_average_since's value has"
                           " the wrong data type"),
                          ({"patient_id": "1f",
                            "heart_rate_average_since":
                            "2018-03-09 11:00:36"},
                           "Key patient_id must be an integer or"
                           " numeric string"),
                          ({"patient_id": "5",
                            "heart_rate_average_since":
                            "2018-03-09 11:00:36"},
                           "ID 5 not in patient database"),
                          ({"patient_id": "1",
                            "heart_rate_average_since":
                            "2018-03-09 11:00:36"},
                           True),
                          ({"patient_id": 1,
                            "heart_rate_average_since":
                            "2018-03-09 11:00:36"},
                           True)])
def test_validate_heart_rate_internal_avg(in_data, expected):
    from hrss_server import validate_heart_rate_internal_avg, find_pt
    answer = validate_heart_rate_internal_avg(in_data)
    assert answer == expected


@pytest.mark.parametrize("in_data, expected",
                         [({"patient_id": 1,
                            "heart_rate_average_since":
                            "2022-11-05 00:06:00"},
                           75),
                          ({"patient_id": 1,
                            "heart_rate_average_since":
                            "2022-11-04 11:00:00"},
                           "There have been no heart rates posted"
                           " before this time")])
def test_internal_avg_hr(in_data, expected):
    from hrss_server import internal_avg_hr, find_pt, init_server
    init_server()
    answer = internal_avg_hr(in_data)
    assert answer == expected


@pytest.mark.parametrize("in_data, expected_message, expected_code",
                         [({"patient_id": 1.1,
                            "heart_rate_average_since":
                            "2018-03-09 11:00:36"},
                           "Key patient_id's value has the wrong data type",
                           400),
                          ({"patient_id": 1,
                            "heart_rate_average_since":
                            "2022-11-04 11:00:00"},
                           "There have been no heart rates posted"
                           " before this time",
                           400),
                          ({"patient_id": 1,
                            "heart_rate_average_since":
                            "2022-11-05 00:06:00"},
                           75,
                           200)])
def test_internal_avg_hr_worker(in_data, expected_message, expected_code):
    from hrss_server import (internal_avg_hr_worker,
                             validate_heart_rate_internal_avg,
                             internal_avg_hr, init_server)
    init_server()
    answer_message, answer_code = internal_avg_hr_worker(in_data)
    assert answer_message == expected_message, answer_code == expected_code


@pytest.mark.parametrize("patient_id, expected",
                         [("1",
                           {"heart_rate": 110,
                            "status": "tachycardic",
                            "timestamp": "2022-11-05 00:15:05"}),
                          ("2",
                           {"heart_rate": 95,
                            "status": "not tachycardic",
                            "timestamp": "2022-11-05 00:05:05"})])
def test_create_status_dict(patient_id, expected):
    from hrss_server import create_status_dict, init_server, find_pt
    init_server()
    answer = create_status_dict(patient_id)
    assert answer == expected


@pytest.mark.parametrize("patient_id, expected_message, expected_code",
                         [("1f",
                           "Patient ID in request must be a numeric string",
                           400),
                          ("5",
                           "ID 5 not in patient database",
                           400),
                          ("1",
                           {"heart_rate": 110,
                            "status": "tachycardic",
                            "timestamp": "2022-11-05 00:15:05"},
                           400)])
def test_get_pt_status_worker(patient_id, expected_message, expected_code):
    from hrss_server import (get_pt_status_worker, init_server, validate_pt_id,
                             create_status_dict)
    init_server()
    answer_message, answer_code = get_pt_status_worker(patient_id)
    assert answer_message == expected_message, answer_code == expected_code


@pytest.mark.parametrize("att_username, expected",
                         [("Bernier.H",
                           "Attending Bernier.H is not in the database"),
                          ("SmithJ",
                           'Key attending_username have'
                           ' format "LastName.FirstInitial"'),
                          ("Smith.JB",
                           'Key attending_username have'
                           ' format "LastName.FirstInitial"'),
                          (".J",
                           'Key attending_username have'
                           ' format "LastName.FirstInitial"'),
                          ("Smith.J",
                           True)])
def test_validate_attending(att_username, expected):
    from hrss_server import validate_attending, init_server, find_attending
    init_server()
    answer = validate_attending(att_username)
    assert answer == expected


@pytest.mark.parametrize("att_username, expected",
                         [("Smith.J",
                           [{"patient_id": 1,
                             "last_heart_rate": 110,
                             "last_time": "2022-11-05 00:15:05",
                             "status": "tachycardic"},
                            {"patient_id": 2,
                             "last_heart_rate": 95,
                             "last_time": "2022-11-05 00:05:05",
                             "status": "not tachycardic"}]),
                          ("Doe.J",
                           [])])
def test_create_attending_dict(att_username, expected):
    from hrss_server import create_attending_dict, init_server
    init_server()
    answer = create_attending_dict(att_username)
    assert answer == expected


@pytest.mark.parametrize("att_username, expected_message, expected_code",
                         [("Bernier.H",
                           "Attending Bernier.H is not in the database",
                           400),
                          ("Smith.J",
                           [{"last_heart_rate": 110,
                             "last_time": "2022-11-05 00:15:05",
                             "patient_id": 1,
                             "status": "tachycardic"},
                            {"last_heart_rate": 95,
                             "last_time": "2022-11-05 00:05:05",
                             "patient_id": 2,
                             "status": "not tachycardic"}],
                           200),
                          ("Doe.J",
                           [],
                           200)])
def test_get_pt_att_worker(att_username, expected_message, expected_code):
    from hrss_server import (get_pt_att_worker, init_server,
                             validate_attending, create_attending_dict)
    init_server()
    answer_message, answer_code = get_pt_att_worker(att_username)
    assert answer_message == expected_message, answer_code == expected_code
