# Register and Serve Features, Labels, and Training Sets

Once you've created your primary data sets, you can define features, labels, and training sets based on them.

## Features

**Features** are a fundamental concept in Featureform. They serve as inputs to machine learning models, providing context or observations that the model uses to make inferences. Feature engineering is often where data scientists can have the most significant impact, improving model performance and reliability. Features are used in two primary contexts: building training sets and serving for inference.

### Anatomy of a Feature

A feature consists of a **value** and an associated [entity](../abstractions/entity.md) value. These features are defined based on registered data sets within Featureform. The entity effectively serves as a primary key or index for the feature values. While some features remain static (e.g., a product category), others change over time. For time-varying features, it's crucial to use point-in-time correct values in training sets to prevent data leakage and enhance model performance.

#### Features without a Timestamp

Some features remain relatively static, like a product's category. In such cases, you can define a feature by adding it to an [entity](../abstractions/entity.md). The feature's first parameter specifies the Featureform dataset, indicating the entity column followed by the value column in the form `dataset[[entity_col, value_col]]`. Optionally, you can set the [variant](../concepts/versioning-and-variants.md). You must also specify the feature's type, which can be one of the following: `ff.Int`, `ff.Int32`, `ff.Int64`, `ff.Float32`, `ff.Float64`, `ff.Timestamp`, `ff.String`. Since features are typically served for inference to your trained model, you need to specify the [inference store](../providers/inference-store.md) for materializing the feature.

Example:
```python
import featureform as ff

@ff.entity
class User:
  age = ff.Feature(dataset[["user", "age"]], variant="simple", type=ff.Int, inference_store=redis)
```

#### Features with a Timestamp

Some features change over time, like a user's highest-priced purchase. In such cases, the feature's value is associated with both the entity and a timestamp. You can access the feature's value as it existed at a specific timestamp, which is crucial for creating [point-in-time correct training sets](../concepts/point-in-time-correctness-historical-features-timeseries-data.md).

To define such a feature, add it to an [entity](../abstractions/entity.md). The feature's first parameter specifies the Featureform dataset, including the entity column, value column, and timestamp column in the form `dataset[[entity_col, value_col, timestamp_col]]`. Optionally, you can set the [variant](../concepts/versioning-and-variants.md). You must also specify the feature's type, which can be one of the following: `ff.Int`, `ff.Int32`, `ff.Int64`, `ff.Float32`, `ff.Float64`, `ff.Timestamp`, `ff.String`, `ff.Bool`. Since features are typically served for inference to your trained model, you need to specify the [inference store](../providers/inference-store.md). To maintain point-in-time correctness, only the most recent entity-feature pair is retained in the inference store.

Example:
```python
import featureform as ff

@ff.entity
class User:
  age = ff.Feature(dataset[["user", "top_item", "timestamp"]], variant="simple", type=ff.Int, inference_store=redis)
```

### Serving Features for Inference

Once a feature is defined and applied, it will be materialized into the inference store for serving. The Featureform client provides a `features` method to serve your features.

Example:
```python
client.features([("age", "simple")], entities={"user": id})
```

## Labels

**Labels** are a core component of a training set. During training, a model relies on a set of features to make an inference. This inference is then compared to a label, and the model is adjusted incrementally based on this comparison.

### Defining a Label

#### With a Timestamp

Some labels can change over time. For example, you might have a label indicating a user's most-listened-to song in the last month. You define it in a manner similar to a feature by specifying the dataset and columns for the entity, the value, and the timestamp. Optionally, you can set the variant and specify the type as one of: `ff.Int`, `ff.Int32`, `ff.Int64`, `ff.Float32`, `ff.Float64`, `ff.Timestamp`, `ff.String`, `ff.Bool`. Unlike a Feature, you should not specify an inference store since labels are never served for inference.

```python
import featureform as ff

@ff.entity
class User:
  top_song = ff.Label(dataset[["user", "top_song"]], variant="30days", type=ff.String)
```

#### Without a Timestamp

Some labels are set once per entity and remain static. For example, you might have a label indicating whether a user is a bot or not. You define it in a manner similar to a [feature](../abstractions/feature.md) by specifying the dataset and columns for the entity and the value. Optionally, you can set the variant and specify the type as one of: `ff.Int`, `ff.Int32`, `ff.Int64`, `ff.Float32`, `ff.Float64`, `ff.Timestamp`, `ff.String`, `ff.Bool`. Unlike a Feature, you should not specify an inference store since labels are never served for inference.



```python
import featureform as ff

@ff.entity
class User:
  is_bot = ff.Label(dataset[["user", "is_bot"]], variant="simple", type=ff.Bool)
```

### Retrieving Feature Values

You can retrieve the most recent value of a feature for a specified entity.

## Training Sets

Models require training, a process that typically involves feeding in a set of features with known labels. During training, the model makes inferences based on these features, and the labels are used to adjust the model's weights.

### Anatomy of a Training Set

A training set consists of one or more features paired with a single label. Below is an example of registering a training set named "fraud_training" with the [variant](../concepts/versioning-and-variants.md) "quickstart." It comprises the "fraudulent/quickstart" label and a single feature "avg_transactions/quickstart."

```python
@ff.entity
class User:
    avg_transactions = ff.Feature(
        average_user_transaction[["CustomerID", "TransactionAmount"]],
        variant="quickstart",
        type=ff.Float32,
        inference_store=redis,
        timestamp_column="timestamp",
    )
    fraudulent = ff.Label(
        transactions[["CustomerID", "IsFraud"]],
        variant="quickstart",
        type=ff.Bool,
        timestamp_column="timestamp",
    )

ff.register_training_set(
    "fraud_training",
    "quickstart",
    label=("fraudulent", "quickstart"),
    features=[("avg_transactions", "quickstart")],
)

client.apply()

# The training set's feature values will be point-in-time correct.
ts = client.training_set("fraud_training", "quickstart").dataframe()
```

### How a Label Gets Joined With Features into a Training Set

Training sets are constructed by pairing features and labels using their [entity](../abstractions/entity.md) key. The process involves looping through the labels and, for each feature, selecting the row with the same entity key as the label. To create [point-in-time correct training sets](../concepts/point-in-time-correctness-historical-features-timeseries-data.md), the feature value is obtained from the row with a timestamp closest to, but less than, the label timestamp. This ensures that the feature value aligns with the label's time.

### Working with Training Sets

#### Using Mini Batches

For larger training sets that do not fit into memory or when distributed Dataframes are not viable, you can iterate through them using mini-batches.

```python
import featureform as ff

client = ff.Client(host)
dataset = client.training_set(name, variant).repeat(5).shuffle(1000).batch(64)
for feature_batch, label_batch in dataset:
  # Run through a shuffled dataset 5 times in batches of 64
```

#### Using Dataframes

Every training set can be directly retrieved as a Dataframe. This approach is suitable for small datasets or when working with Dataframe-based training systems like Databricks. It offers ease and flexibility in handling training sets.

```python
ts = client.training_set("fraud_training", "quickstart").dataframe()
```
