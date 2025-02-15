# Offline Store

The Offline Store provider is a versatile component within Featureform, serving multiple key functions. It plays a central role in running transformations and storing data. Due to Featureform's virtual architecture, you can expect similar performance and cost characteristics from the Offline Store as you would without Featureform, making it a nearly seamless abstraction layer.

Here are the essential functions of the Offline Store:

1. **Source Primary Data Sets:** It serves as the source for primary data sets, which are essential for Featureform operations.

2. **Transform Data Sets:** The Offline Store executes transformations to build data sets registered through Featureform. This is where the real transformation work happens.

3. **Build Point-in-Time Correct Training Sets:** It constructs training sets while ensuring point-in-time correctness, a crucial aspect for training machine learning models. Featureform creates and runs the proper transformation to build the training set, but the offline store is the engine to run this transformation.

4. **Build Batch Features:** For batch features, it acts as the source of data to be materialized into the inference store, where the most recent values are stored. Featureform handles getting the features into the inference store.

5. **Maintain Historical Back-fill for Streaming Features:** In cases involving streaming features, the Offline Store maintains a log of historical feature values, allowing us to create point-in-time correct training sets. Featureform will handle keeping the inference store nad offline store in sync.

It's important to note that the term "Offline Store" can be slightly misleading, as it encompasses more than just a store for training data. It functions as both a data storage and transformation engine, playing a pivotal role in Featureform's operations.

## ETL-Based Offline Stores

Some transformation executors, such as Spark and Pandas on K8s, interact with file stores for reading and writing data. In such cases, the Offline Store is essentially registered with two components: the storage layer and the transformation layer.

## ELT-Based Offline Stores

Most SQL-based offline stores, like Snowflake, operate on an ELT (Extract, Load, Transform) paradigm. These systems have their storage integrated, and transformations are executed within the same database environment.
