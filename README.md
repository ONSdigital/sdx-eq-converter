# sdx-eq-converter

[![Build Status](https://github.com/ONSdigital/sdx-eq-converter/workflows/Build/badge.svg)](https://github.com/ONSdigital/sdx-eq-converter) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/0d8f1899b0054322b9d0ec8f2bd62d86)](https://www.codacy.com/app/ons-sdc/sdx-eq-converter?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ONSdigital/sdx-eq-converter&amp;utm_campaign=Badge_Grade) [![codecov](https://codecov.io/gh/ONSdigital/sdx-eq-converter/branch/main/graph/badge.svg)](https://codecov.io/gh/ONSdigital/sdx-eq-converter)

The sdx-eq-converter service is used within the Office National of Statistics (ONS) for managing survey submissions in JSON
format. It is required as a temporary helper for transitioning between EQv2 and EQv3.

## Process

The sdx-eq-converter microservice receives JSON submissions via a PubSub subscription: `survey-subscription`. 
The submission is then written to a bucket: `survey-responses` which triggers a notification on `survey-trigger-topic`. 
If the survey fails to be written to the bucket then it is instead published to a quarantine PubSub topic: `quarantine-survey-topic`.

## Getting started
Install requirements:
```shell
$ make build
```

Testing:
ensure you have installed all requirements with above `make build` command then:
```shell
$ make test
```

Running:
ensure you have installed all requirements with above `make build` command then:
```shell
$ make start
```

## GCP

### Pubsub

sdx-eq-converter receives message from `survey-subscription`. This message contains the encrypted JSON and `tx_id`

**Message Structure Example**
```code
Message {
  data: b'eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraW...'
  ordering_key: ''
  attributes: {
    "tx_id": "7ef50b15-49f5-4ad3-bb08-911537d1417d"
  }
}
```

**Message Data field unencrypted**
(python dict)
```python
data : {
    "case_id": "bb9eaf11-a729-40b5-8d17-d112e018c0d5",
    "collection": {
        "exercise_sid": "664dbdf4-02fb-4d68-b0cf-7f7402df00e5",
        "instrument_id": "0011",
        "period": "201904"
    },
    "data": {
        "15": "No",
        "119": "150",
        "120": "152",
        "144": "200",
        "145": "124",
        "146": "This is a comment"
    },
    "flushed": False,
    "metadata": {
        "ref_period_end_date": "2018-11-29",
        "ref_period_start_date": "2019-04-01",
        "ru_ref": "15162882666F",
        "user_id": "UNKNOWN"
    },
    "origin": "uk.gov.ons.edc.eq",
    "started_at": "2019-04-01T14:00:24.224709",
    "submitted_at": "2019-04-01T14:10:26.933601",
    "survey_id": "017",
    "tx_id": "1027a13a-c253-4e9d-9e78-d0f0cfdd3988",
    "type": "uk.gov.ons.edc.eq:surveyresponse",
    "version": "0.0.1"
}       
```

    
**Quarantine Message**

sdx-eq-converter publishes to `quarantine-survey-submission`. The original message from `survey-submission` 
is published in addition to the error/validation message 

```code
Message {
  data: b'eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraW...'
  ordering_key: ''
  attributes: {
    "error": "required key not provided @ data['data']",
    "tx_id": "a79160b5-67de-460c-bda3-cc54b97c7c50"
  }
```

### License

Copyright (c) 2021 Crown Copyright (Office for National Statistics)

Released under MIT license, see [LICENSE](LICENSE) for details.