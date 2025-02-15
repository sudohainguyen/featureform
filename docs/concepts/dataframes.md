# Exploring Resources with Dataframes

When it comes to working with data for machine learning, dataframes are ubiquitous. Featureform simplifies interaction with its sources and transformations, allowing you to fetch them into local memory as dataframes using the *client.dataframe()* API.

```python
@spark.df_transform(inputs=[upstream_data])
def transformation_name(upstream):
  ...
client.dataframe(transformation_name)
```

In scenarios where the dataset is sizable enough to exceed memory limits or when a sample suffices, you can include the *rows* parameter to restrict the number of pulled rows.

```python
client.dataframe(transformation_name, rows=10000)
```

Fetching training sets as dataframes is also feasible. In this case, Featureform's serving API equips the training set object with a *.dataframe()* method.

```python
client.training_set("name", "variant").dataframe()
```

These mechanisms offer an intuitive and efficient approach to delve into your data using the familiar Dataframe APIs.
