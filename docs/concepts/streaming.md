# Streaming Data: Real-time Updates

Certain features necessitate continuous updates through a data stream, surpassing the capabilities of scheduled batch processing or triggered executions. *Featureform Enterprise* offers an API tailored for streaming feature values. This not only ensures real-time relevance but also retains historical values to build point-in-time correct training datasets.

```python
@ff.entity
class User:
  last_purchase = ff.Stream(offline_store=snowflake, online_store=redis, type=ff.Float32)

client.write_feature(User.last_purchase, (user_id, new_value))
```

This example showcases how to leverage streaming functionality within Featureform. In this scenario, the feature `last_purchase` of the `User` entity is designated as a stream. The `offline_store` (here, snowflake) and `online_store` (here, redis) specify storage destinations. The data type, in this case, is set to `ff.Float32`. By utilizing `client.write_feature`, you can update the `last_purchase` feature in real time, enhancing the accuracy and timeliness of your data-driven processes.
