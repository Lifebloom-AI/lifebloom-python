# Thread

Types:

```python
from lifebloom.types import APIResponse, ThreadState
```

Methods:

- <code title="post /thread">client.thread.<a href="./src/lifebloom/resources/thread.py">create</a>(\*\*<a href="src/lifebloom/types/thread_create_params.py">params</a>) -> None</code>

# InitializeThread

Types:

```python
from lifebloom.types import APIResponse
```

Methods:

- <code title="post /initializeThread">client.initialize_thread.<a href="./src/lifebloom/resources/initialize_thread.py">create</a>(\*\*<a href="src/lifebloom/types/initialize_thread_create_params.py">params</a>) -> None</code>

# Pets

Types:

```python
from lifebloom.types import (
    PetRetrieveResponse,
    PetUpdateResponse,
    PetFindByStatusResponse,
    PetFindByTagsResponse,
    PetUploadImageResponse,
)
```

Methods:

- <code title="post /pet/{petId}">client.pets.<a href="./src/lifebloom/resources/pets.py">create</a>(pet_id, \*\*<a href="src/lifebloom/types/pet_create_params.py">params</a>) -> None</code>
- <code title="get /pet/{petId}">client.pets.<a href="./src/lifebloom/resources/pets.py">retrieve</a>(pet_id) -> <a href="./src/lifebloom/types/pet_retrieve_response.py">object</a></code>
- <code title="put /pet">client.pets.<a href="./src/lifebloom/resources/pets.py">update</a>(\*\*<a href="src/lifebloom/types/pet_update_params.py">params</a>) -> <a href="./src/lifebloom/types/pet_update_response.py">object</a></code>
- <code title="delete /pet/{petId}">client.pets.<a href="./src/lifebloom/resources/pets.py">delete</a>(pet_id) -> None</code>
- <code title="get /pet/findByStatus">client.pets.<a href="./src/lifebloom/resources/pets.py">find_by_status</a>(\*\*<a href="src/lifebloom/types/pet_find_by_status_params.py">params</a>) -> <a href="./src/lifebloom/types/pet_find_by_status_response.py">PetFindByStatusResponse</a></code>
- <code title="get /pet/findByTags">client.pets.<a href="./src/lifebloom/resources/pets.py">find_by_tags</a>(\*\*<a href="src/lifebloom/types/pet_find_by_tags_params.py">params</a>) -> <a href="./src/lifebloom/types/pet_find_by_tags_response.py">PetFindByTagsResponse</a></code>
- <code title="post /pet/{petId}/uploadImage">client.pets.<a href="./src/lifebloom/resources/pets.py">upload_image</a>(pet_id, \*\*<a href="src/lifebloom/types/pet_upload_image_params.py">params</a>) -> <a href="./src/lifebloom/types/pet_upload_image_response.py">object</a></code>
