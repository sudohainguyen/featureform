# Data Infrastructure Provider

Featureform functions as a Virtual Feature Store, strategically positioned atop your existing data infrastructure. It acts orchestrator, conducting your infrastructure to construct and serve the features you define. Importantly, this approach means your data remains within your infrastructure—it's not stored in Featureform. Moreover, transformations occur using the same language and performance capabilities as if Featureform were not in the picture. To operate in this framework, you need to register and configure your data infrastructure.

Our data infrastructure providers come in two flavors: **Offline Stores** and **Inference Stores**.

## Offline Stores

Offline stores play a pivotal role in executing your transformations to create features and training sets. These training sets are also stored and served from the offline store. In non-streaming scenarios, inference store data is crafted within the Offline Store before being materialized into the Inference Store.

Offline Stores consist of a storage layer and an execution layer. While some providers like Snowflake combine these elements, others like Spark require connection to a separate storage layer such as S3 or HDFS.

## Inference Stores

Featureform is also able to orchestrate an inference store. The inference store typically offers lower-latency access and serves as a cache for the most recent feature values for use in real-time ML use-cases. In streaming scenarios, it undergoes continuous updates, while in batch processing, updates follow a user-defined schedule.

### Vector Databases (Vector DBs)

A noteworthy subset of inference stores is Vector Databases. These specialized stores support a Nearest Neighbor operation, making them core for use cases involving embeddings.

This data infrastructure provider abstraction ensures your data remains under your control while leveraging the capabilities of Featureform to streamline feature creation, management, and collaboration.
