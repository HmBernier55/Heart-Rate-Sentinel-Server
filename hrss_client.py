import requests

# ************************** Zac *********************************

url = 'http://vcm-29733.vm.duke.edu:5000'


# *****  `/api/new_patient` *****

out_data_np = {'patient_id': '3', 'attending_username': 'Doe.J',
               'patient_age': 24}
r_np = requests.post(url + '/api/new_patient', json=out_data_np)
print(r_np.status_code)
print(r_np.text)

# ***** `/api/heart_rate` *****

out_data_hr_email = {'patient_id': 3, 'heart_rate': 120}
r_hr_email = requests.post(url + '/api/heart_rate', json=out_data_hr_email)
print(r_hr_email.status_code)
print(r_hr_email.text)

# *****  `/api/heart_rate/<patient_id>` *****

pt_id_hr = '3'
r_hr_pt = requests.get(url + '/api/heart_rate/' + pt_id_hr)
print(r_hr_pt.status_code)
print(r_hr_pt.text)

# ***** `/api/heart_rate/average/<patient_id>` *****

pt_id_avg = '3'
r_hr_avg = requests.get(url + '/api/heart_rate/average/' + pt_id_avg)
print(r_hr_avg.status_code)
print(r_hr_avg.text)


# *****************************************************************
# *****************************************************************


# ************************** Hunter *********************************

# ***** `/api/new_attending` *****

out_data_na = {"attending_username": "Jane.M",
               "attending_email": "DrJane@my_hospital.com",
               "attending_phone": "123-456-7890"}
r_na = requests.post(url + "/api/new_attending",
                     json=out_data_na)
print(r_na.status_code)
print(r_na.text)

# ***** `/api/heart_rate/interval_average` *****

out_data_hr_internal = {"patient_id": 1,
                        "heart_rate_average_since": "2022-11-05 00:06:00"}
r_hr_internal = requests.post(url + "/api/heart_rate/"
                              "interval_average", json=out_data_hr_internal)
print(r_hr_internal.status_code)
print(r_hr_internal.text)

# ***** `/api/status/<patient_id>` *****

r_status = requests.get(url + "/api/status/1")
print(r_status.status_code)
print(r_status.text)

# ***** `/api/patients/<attending_username>`*****

r_att_pt = requests.get(url + "/api/patients/Doe.J")
print(r_att_pt.status_code)
print(r_att_pt.text)
