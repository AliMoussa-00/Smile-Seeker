# APIs

this part is about the api's that will be used to send/get data to/from the **backend**





| route                                                       | methods                                                                                                                                                       |
| ----------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /api/doctors                                                | - **Get:** all the doctor instances<br/>- **Post:** create a doctor instance                                                                                  |
| /api/doctors/<doctor_id>                                    | **Get**: get the doctor object using ID
<br/>**Put**: update the doctor object
<br/>**Delete**: delete the doctor object                                      |
| /api/doctors/<doctor_id>/reviews                            | **Get**: get the reviews about a doctor                                                                                                                       |
| /api/doctors/<doctor_id>/appointments                       | **Get**: all the appointments of a doctor.                                                                                                                    |
| /api/doctors/<doctor_id>/<br/>appointments/<appointment_id> | **Put:** update an appointment object a doctor can accept decline an appointment                                                                              |
| /api/users                                                  | **Post:** create a user object                                                                                                                                |
| /api/user/<user_id>                                         | **Get:** get the user object
<br/>**Put:** update the user object
<br/>**Delete:** delete the user object                                                     |
| /api/users/<user_id>/appointments                           | **Get:** all the appointments of a user.
<br/>**Post:** make an appointment object.                                                                           |
| /api/users/<user_id>/<br/>appointments/<appoint_id>         | **Delete**: delete an appointment object                                                                                                                      |
| /api/reviews/<review_id>                                    | **Get:** a review by id.
<br/>**Put:** update a review.
<br/>**Delete:** delete a review                                                                      |
| /api/<doctor_id>/location                                   | **Get:** get the location of a doctor<br/>**Put:** update the location object<br/>**Post:** create a location object<br/>**Delete:** delete a location object |
| /api/auth/login                                             |                                                                                                                                                               |
| /api/auth/logout                                            |                                                                                                                                                               |
| /api/users/<user_id>/profile-picture                        |                                                                                                                                                               |
| /api/doctors/<doctor_id>/gallery                            |                                                                                                                                                               |
| /api/notifications                                          |                                                                                                                                                               |


