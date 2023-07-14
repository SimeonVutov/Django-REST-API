import requests

product_id = input('What is the product id: ')

try:
    product_id = int(product_id)
except:
    product_id = None
    print(f'This product id({product_id}) is not valid')

if product_id is not None:
    endpoint = f'http://localhost:8000/api/products/{product_id}/delete/'
    response = requests.delete(endpoint)

    print('Item was deleted'
          if response.status_code == 204
          else 'A problem occure')
