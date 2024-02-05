import requests

# response = requests.post(
#     'http://127.0.0.1:5000/products/',
#     json={"header": "Some product", "description": "Some description", "owner": "some_owner"},
# )
# print(response.status_code)
# print(response.text)

# response = requests.get(
#     'http://127.0.0.1:5000/products/2/',
# )
# print(response.status_code)
# print(response.text)

# response = requests.get(
#     'http://127.0.0.1:5000/products/600/',
# )
# print(response.status_code)
# print(response.text)

# response = requests.patch(
#     'http://127.0.0.1:5000/products/2/',
#     json={"header": "Changed header", "owner": "some_other_owner"}
# )
# print(response.status_code)
# print(response.text)
#
# response = requests.get(
#     'http://127.0.0.1:5000/products/2/',
# )
# print(response.status_code)
# print(response.text)


# response = requests.delete(
#     "http://127.0.0.1:5000/products/2/",
# )
# print(response.status_code)
# print(response.text)

response = requests.get(
    "http://127.0.0.1:5000/products/2/",
)
print(response.status_code)
print(response.text)
