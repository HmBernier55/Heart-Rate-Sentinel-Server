# Heart Rate Sentinel Server Assignment
### **_Author:_**
Hunter Bernier and Zac Spalding
## **_License:_**
MIT License
## **_Purpose:_**
The code within this repository builds a simple centralized heart rate sentinel server. The server was built to receive GET and POST requests that contain patient heart rate information from mock patient heart rate monitors. The server will allow the following API routes:
1. POST Requests:
    * `/api/new_attending`
    * `/api/new_patient`
    * `/api/heart_rate`
    * `/api/heart_rate/interval_average`
2. GET Requests:
    * `/api/status/<patient_id>`
    * `/api/heart_rate/<patient_id>`
    * `/api/heart_rate/average/<patient_id>`
    * `/api/patients/<attending_username>`
## **_Details Regarding Each Route:_**
1. `POST /api/new_attending`
    * Takes a JSON input as follows:
        ```
        {
            "attending_username": <attending_username_string>
            "attending_email": <attending_email_string>
            "attending_phone": <attending_phone_string>
        }
        ```
        where
        * `<attending_username_string>` is a string in the format "LastName.FirstInitial" such as `"Jane.M"`
        * `<attending_email_string>` is a string containing an e-mail address
        * `<attending_phone_string` is a string containing a 10 digit phone number with the dashes such as `919-555-1212`
    * This route adds a new attending to the attending database on the server
2. `POST /api/new_patient`
    * Takes a JSON input as follows:
        ```
        {
            "patient_id": <patient_id>
            "attending_username": <attending_username_string>
            "patient_age": <patient_age>
        }
        ```
        where
        * `<patient_id>` is the patient medical record number
        * `<attending_username_string>` is a string following the "LastName.FirstInitial" format from the `/api/new_attending` route
        * `<patient_age>` is the patient's age in years
    * This route adds a new patient to the patient database on the server
3. `POST /api/heart_rate`
    * Takes a JSON input as follows:
        ```
        {
            "patient_id": <patient_id>
            "heart_rate": <heart_rate>
        }
        ```
        where
        * `<patient_id>` is the patient medical record number
        * `<heart_rate>` is the patient heart rate being recorded
    * This route:
        1. Stores the given heart rate measurement in the record for the specified patient
        2. The current date and time of when the heart rate was measured is stored with the heart rate measurement
        3. If the heart rate is tachycardic for the specified patient and patient age, an e-mail is sent to the attending physician. The e-mail includes the patient id number, the heart rate, and the date and time of when the heart rate was taken
4. `POST /api/heart_rate/interval_average`
    * Takes a JSON input as follows:
        ```
        {
            "patient_id": <patient_id>
            "heart_rate_average_since": <time_stamp_string>
        }
        ```
        where
        * `<patient_id>` is the patient medical record number
        * `<time_stamp_string>` is a string containing a date and time with the format of `"<Year>-<Month>-<Day> <Hour>:<Minute>:<Second>"`
    * This route calculates the average of all the heart rates that have been posted for the specified patient since the given date and time
5. `GET /api/status/<patient_id>`
    * This route returns a dictionary in a JSON string containing the latest heart rate for the specified patient, whether the patient is currently tachycardic based on the most recently posted heart rate, and the date and time of when the most recent heart rate was measured
    * The return dictionary should look like:
        ```
        {
            "heart_rate": <heart_rate_integer>
            "status": <status_string>
            "timestamp": <time_stamp_string>
        }
        ```
        where
        * `<heart_rate_integer>` is the most recent heart rate
        * `<status_string>` is either `"tachycardic"` or `"not tachycardic"` based on the most recent heart rate
        * `<time_stamp_string>` is the date and time of when the most recent heart rate was measured with the format `"<Year>-<Month>-<Day> <Hour>:<Minute>:<Second>"`
6. `GET /api/heart_rate/<patient_id>`
    * This route returns a list of all the previous heart rate measurements for the specified patient
7. `GET /api/heart_rate/average/<patient_id>`
    * This route returns the patient's average heart rate of all the measurements that are stored for the specified patient
8. `GET /api/patients/<attending_username>`
    * This route returns a list of dictionaries that contain information on all patients of the specified attending physician.
    * The patient dictionaries are of the following format:
        ```
        {
            "patient_id": <patient_id>
            "last_heart_rate": <heart_rate_integer>
            "last_time": <time_stamp_string>
            "status": <status_string>
        }
        ```
        where
        * `<patient_id>` is the patient medical record number
        * `<heart_rate_integer>` is the most recent heart rate measured
        * `<time_stamp_string>` is the date and time of the most recent heart rate measurement in the format `"<Year>-<Month>-<Day> <Hour>:<Minute>:<Second>"`
        * `<status_string>` is either `"tachycardic"` or `"not tachycardic"` based on the most recent heart rate
    * If no patients exist for the specified physician, an empty list is returned
## **_How to Run the Program:_**
* The heart rate sentinel server is hosted on a virtual machine and can receive requests to access the above API routes. See section *_How to Use the Program_* for instructions on how to access the server.
* The heart rate sentinel server can also be hosted locally on your machine. To do so, first clone this respository to your desired file location. Then create a Python virtual environment and install all packages found in the `requirements.txt` file. In this directiory, type `python hrss_server.py` to start the server. The server will be hosted locally at `http://127.0.0.1:5000`. Details on how to send requests to the server are found in the *_How to Use the Program_* section.

## **_How to Use the Program:_**
* The heart rate sentinel server can be accessed by sending requests to the following URL: `http://vcm-29733.vm.duke.edu:5000`. From the server routes above, GET requests can be sent to `http://vcm-29733.vm.duke.edu:5000/<route>` (for example, `http://vcm-29733.vm.duke.edu:5000/api/heart_reate/<patient_id>`) via a browser (typing this as a web address) or via a Python script using the `requests` package. POST requests can also be sent using this package. See `hrss_client.py` for an example of how to send requests to the server.
* If hosting the server locally, follow the instructions above for the URL `http://127.0.0.1:5000`. Make sure you have followed the instructions above to get the server running before trying to make requests to your locally hosted server.
* All server routes specified above will return either a message (POST) detailing the success/failure of the request or a JSON string (GET) containing the requested information and an accompanying status code indicating success (200) or failure (400) of the request. The JSON strings can then be converted to Python data types using the `json` package. See the server routes in *_Details Regarding Each Route_* for more information about what each route returns.

## **_Details Regarding the Virtual Machine:_**
* The HRSS server is hosted on a virtual machine owned by Duke university. This hosting is supported by Duke through the class BME 547. The server can be accessed on the virtual machine with following the URL: 
```
http://vcm-29733.vm.duke.edu:5000
```

## **_Details Regarding the E-mail Server:_**
* An email is sent to the attending physician assigned to a patient whenever that patient's heart rate measurements are updated with a tachycardic heart rate. Tachycardic heart rates are classified with criteria on [tachycardia from Wikipedia](https://en.wikipedia.org/wiki/Tachycardia)
* The sending of emails for the code is simulated by making POST requests to an email server hosted on a virtual machine at Duke University. These post requests are made within the `/api/heart_rate` route when a tachycardic heart rate is posted. Posts requests are made to the following URL.
    ```
    http://vcm-7631.vm.duke.edu:5007/hrss/send_email
    ```
* The POST request sends the following dictionary:
    ```
    {
        "from_email": <from_email_string>
        "to_email": <to_email_string>
        "subject": <subject_string>
        "content": <content_string>
    }
    ```
    where
    * `<from_email_string>` is the e-mail address from which the message is being sent 
        * (`tachycardic-alert@hospital.com` in this code)
    * `<to_email_string>` is the e-mail address to which the message is being sent 
        * (email address of the attending physician for the patient)
    * `<subject_string>` is the subject of the e-mail 
        * ("Patient `<patient_id>` tachycardic")
    * `<content_string>` is the content of the e-mail  
        * ("Patient `<patient_id>` classified as tachycardic with heart rate of `<heart_rate>` at `<date and time of heart rate>`" in this code)