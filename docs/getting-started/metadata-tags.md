# Metadata Tags

Featureform allows users to apply metadata tags to resources to logically group them together. Metadata tags can either be a list (`tags`), a set of key-value pairs (`properties`), or both, and are applicable to all resource types:

* Providers
* Sources
* Entities
* Features
* Labels
* Training Sets
* Models
* Users

## Example Config

In this example, we'll add tags and properties to all the resources included in the [Docker Quickstart](../deployment/quickstart-docker.md):

{% code title="providers.py" %}

```python
import featureform as ff

postgres = ff.register_postgres(
    name="postgres-quickstart",
    host="host.docker.internal",
    port="5432",
    user="postgres",
    password="password",
    database="postgres",
    tags=["primary_training_data"],
    properties={"next_key_rotation": "2023-05-31"},
)

redis = ff.register_redis(
    name="redis-quickstart",
    host="host.docker.internal",
    port=6379,
    tags=["primary_inference_store"],
)

transactions = postgres.register_table(
    name="transactions",
    table="Transactions",
    tags=["pii_data"],
)


@postgres.sql_transformation(tags=["avg_aggregation"])
def average_user_transaction():
    return (
        "SELECT CustomerID as user_id, avg(TransactionAmount) "
        "as avg_transaction_amt from {{transactions.default}} GROUP BY user_id"
    )


user = ff.register_entity("user", tags=["transactions_pk"])

# Register a column from our transformation as a feature
average_user_transaction.register_resources(
    entity=user,
    entity_column="user_id",
    inference_store=redis,
    features=[
        {
            "name": "avg_transactions",
            "column": "avg_transaction_amt",
            "type": "float32",
            "tags": ["transactions_v1", "pii_data"],
            "properties": {"ready_for_training": "yes"},
        },
    ],
)
# Register label from our base Transactions table
transactions.register_resources(
    entity=user,
    entity_column="customerid",
    labels=[
        {
            "name": "fraudulent",
            "column": "isfraud",
            "type": "bool",
            "tags": ["transactions_v1", "pii_data"],
            "properties": {"ready_for_training": "yes"},
        },
    ],
)

ff.register_training_set(
    "fraud_training", label="fraudulent", features=["avg_transactions"], tags=["transactions_v1", "pii_data"]
)
```

{% endcode %}

Then, we'll use the Featureform CLI to register these resources with the applied metadata tags.

```bash
featureform apply providers.py
```

## Updating Tags

Currently, we can update metadata tags that have already been applied to resources:

* `tags`: adding a new tag to a previously registered resource will append it to the list
* `properties`: adding a new key-value pair to a previously registered resource will add the pair to the set; if an pair contains an existing key, then the new value will overwrite the old value
