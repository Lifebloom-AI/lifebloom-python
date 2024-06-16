# Shared Types

```python
from lifebloom.types import Order
```

# Thread

Methods:

- <code title="post /thread">client.thread.<a href="./src/lifebloom/resources/thread.py">completion</a>() -> None</code>
- <code title="post /initializeThread">client.thread.<a href="./src/lifebloom/resources/thread.py">initialize_thread</a>() -> None</code>

# Pets

Types:

```python
from lifebloom.types import APIResponse, Pet, PetFindByStatusResponse, PetFindByTagsResponse
```

Methods:

- <code title="post /pet">client.pets.<a href="./src/lifebloom/resources/pets.py">create</a>(\*\*<a href="src/lifebloom/types/pet_create_params.py">params</a>) -> <a href="./src/lifebloom/types/pet.py">Pet</a></code>
- <code title="get /pet/{petId}">client.pets.<a href="./src/lifebloom/resources/pets.py">retrieve</a>(pet_id) -> <a href="./src/lifebloom/types/pet.py">Pet</a></code>
- <code title="put /pet">client.pets.<a href="./src/lifebloom/resources/pets.py">update</a>(\*\*<a href="src/lifebloom/types/pet_update_params.py">params</a>) -> <a href="./src/lifebloom/types/pet.py">Pet</a></code>
- <code title="delete /pet/{petId}">client.pets.<a href="./src/lifebloom/resources/pets.py">delete</a>(pet_id) -> None</code>
- <code title="get /pet/findByStatus">client.pets.<a href="./src/lifebloom/resources/pets.py">find_by_status</a>(\*\*<a href="src/lifebloom/types/pet_find_by_status_params.py">params</a>) -> <a href="./src/lifebloom/types/pet_find_by_status_response.py">PetFindByStatusResponse</a></code>
- <code title="get /pet/findByTags">client.pets.<a href="./src/lifebloom/resources/pets.py">find_by_tags</a>(\*\*<a href="src/lifebloom/types/pet_find_by_tags_params.py">params</a>) -> <a href="./src/lifebloom/types/pet_find_by_tags_response.py">PetFindByTagsResponse</a></code>
- <code title="post /pet/{petId}">client.pets.<a href="./src/lifebloom/resources/pets.py">update_by_id</a>(pet_id, \*\*<a href="src/lifebloom/types/pet_update_by_id_params.py">params</a>) -> None</code>
- <code title="post /pet/{petId}/uploadImage">client.pets.<a href="./src/lifebloom/resources/pets.py">upload_image</a>(pet_id, \*\*<a href="src/lifebloom/types/pet_upload_image_params.py">params</a>) -> <a href="./src/lifebloom/types/api_response.py">APIResponse</a></code>

# Store

Types:

```python
from lifebloom.types import StoreInventoryResponse
```

Methods:

- <code title="post /store/order">client.store.<a href="./src/lifebloom/resources/store/store.py">create_order</a>(\*\*<a href="src/lifebloom/types/store_create_order_params.py">params</a>) -> <a href="./src/lifebloom/types/shared/order.py">Order</a></code>
- <code title="get /store/inventory">client.store.<a href="./src/lifebloom/resources/store/store.py">inventory</a>() -> <a href="./src/lifebloom/types/store_inventory_response.py">StoreInventoryResponse</a></code>

## Order

Methods:

- <code title="get /store/order/{orderId}">client.store.order.<a href="./src/lifebloom/resources/store/order.py">retrieve</a>(order_id) -> <a href="./src/lifebloom/types/shared/order.py">Order</a></code>
- <code title="delete /store/order/{orderId}">client.store.order.<a href="./src/lifebloom/resources/store/order.py">delete_order</a>(order_id) -> None</code>
