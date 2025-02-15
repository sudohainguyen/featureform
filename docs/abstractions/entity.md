# Entities

An **entity** serves as a collection of semantically related features and labels. Users define entities to map to the domain of their specific use cases. For instance, in the context of a ride-hailing service, entities could include "customers" and "drivers," grouping related features and labels associated with these respective entities.

Entities play vital roles in:

1. **Defining and Storing Features and Labels**: The `featureform` library provides an `entity` decorator that can be applied to classes. This decorator allows you to associate features and labels with the entity using Featureform data sets that you've defined earlier. A feature typically comprises at least two columns: an entity column (similar to an index or primary key) and a value column. Optionally, it can include a third column for timestamps, which becomes essential for constructing [point-in-time correct training sets](../concepts/point-in-time-correctness-historical-features-timeseries-data.md).

   For example, consider a "User" entity with an "age" feature and a "credit score" label associated with it:

   ```python
   import featureform as ff

   @ff.entity
   class User:
     age = ff.Feature(dataset[["user", "age"]], variant="simple", type=ff.Int, inference_store=redis)
     credit_score = ff.Label(dataset[["user", "credit_score"]], variant="simple", type=ff.Int)
   ```

2. **Building Training Sets by Joining Features and Labels by Their Entity**: To create a training set, you need to associate a label with a set of features based on their entity values. If both the label and features have timestamps, the feature value chosen is the one with a matching entity and a timestamp that is the closest (but earlier) to the timestamp of the label.

   In the case of our "User" entity example, we can create a training set like this:

   ```python
   ff.register_training_set(
     "credit_score_training_set", "v1",
     label=("credit_score", "simple"),
     features=[("age", "simple")],
   )
   ```

   Alternatively, if the "User" class is in scope, you can use a convenient syntax to avoid explicitly specifying name/variant tuples:

   ```python
   ff.register_training_set(
     "credit_score_training_set", "v1",
     label=User.credit_score,
     features=User.age,
   )
   ```

3. **Serving Features at Inference Time by Entity**: The inference store retains the most recent value of each feature, indexed by its entity column. To retrieve features, you can utilize the `features` method of a Featureform Client object.

   ```python
   f = client.features([("age", "simple")], entities={"user": "10323232"})
   ```

Entities provide a structured and organized approach to managing features and labels in Featureform, facilitating the creation of training sets and the retrieval of features during inference.
