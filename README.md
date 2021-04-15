# Introduction

Learning Resource is DRF API for a resource for learning foreign languages.

Using [Quiz API](/back/api/quiz_api/), administrator can create daily quizzes for other users.

Using [Test API](/back/api/test_api/), administrator can create tests for different areas (such as IT, Business, etc.) for other users.

Using [Homework API](/back/api/homework_api), administration can create homework for students, in response to which they can attach a file.
Later, the administrator can rate the answer to the homework.

To view the results, the [Info API](/back/api/info_api) is used, which can show the status of the tasks (completed, assigned, evaluated) and student statistics, containing information about completed tests and homeworks.

## Authorization

All API requests require the use of a generated API key.
To authenticate an API request, you should provide your API key in the `Authorization` header.


## Responses

All API endpoints return the JSON representation. However, if an invalid request is submitted, or some other error occurs, LearningResource returns a JSON response in the following format:

```javascript
{
  "message" : string,
}
```

## Status Codes

ShortenYourLink returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
