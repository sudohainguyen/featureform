# Run in command line with:
# python3 -m featureform apply quickstart.py -host <hostname:port>
import featureform as ff

user = ff.register_user("test")
user.make_default_owner()
postgres = ff.register_postgres(
    name="postgres",
    host="quickstart-postgres",
    port="5432",
    user="postgres",
    password="password",
    database="postgres",
    description="Postgres",
    team="Featureform Success Team",
)
table = postgres.register_table(
    name="transactions",
    variant="v1",
    table="Transactions",
    description="Transactions file from Kaggle",
)


@postgres.sql_transformation(variant="v1")
def user_transaction_count():
    """the number of transactions for each user"""
    return 'SELECT CustomerID as user_id, COUNT(*) as user_transaction_count FROM {{transactions.v1}} GROUP BY user_id' #Removed timestamp since it doesnt make sense to group by user and timestamp unless its binned


@postgres.sql_transformation(variant="v1")
def average_user_transaction():
    """the average transaction amount for a user """
    return "SELECT CustomerID as user_id, avg(TransactionAmount) " \
           "as avg_transaction_amt from {{transactions.v1}} GROUP BY user_id"


@postgres.sql_transformation(variant="v1")
def user_has_fraud():
    """if the user has had a fraudulent transaction """
    return 'SELECT CustomerID as user_id, SUM(CASE WHEN ISFRAUD=TRUE THEN 1 ELSE 0 END) as has_fraud from {{transactions.v1}} GROUP BY user_id'


entity = ff.register_entity("user")
redis = ff.register_redis(
    name="redis5",
    host="quickstart-redis",
    port=6379,
)

user_transaction_count.register_resources(
    entity=entity,
    entity_column="user_id",
    inference_store=redis,
    features=[
        {"name": "transaction_count", "variant": "v1", "column": "user_transaction_count", "type": "int64"},
    ],
)

average_user_transaction.register_resources(
    entity=entity,
    entity_column="user_id",
    inference_store=redis,
    features=[
        {"name": "average_transaction", "variant": "v1", "column": "avg_transaction_amt", "type": "float32"},
    ],
)

user_has_fraud.register_resources(
    entity=entity,
    entity_column="user_id",
    inference_store=redis,
    labels=[
        {"name": "has_fraud", "variant": "v1", "column": "has_fraud", "type": "bool"},
    ],
)

ff.register_training_set("fraud_training", "v1", label=("has_fraud", "v1"), features=[("transaction_count", "v1"), ("average_transaction", "v1")])