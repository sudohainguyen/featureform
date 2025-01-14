# Overview of Infrastructure Providers

Featureform is designed around a Virtual Feature Store architecture, which manages metadata and orchestrates various infrastructure providers. This approach allows data scientists to interact with their data using the Featureform framework while ensuring that data continues to be stored and processed in a manner consistent with existing infrastructure. Featureform supports four primary provider abstractions:

## 1. Offline Stores

Offline Stores are responsible for storing and transforming data sets and training sets. They play a crucial role in feature creation and data transformation.

## 2. Inference Stores

Inference Stores act as caches for the most recent feature values. They are used for real-time model inference, enabling fast and efficient access to feature data.

## 3. Vector Databases

Vector Databases are a specialized type of Inference Store designed for performing nearest neighbor operations. They are primarily used with embeddings to support applications such as similarity searches.

## 4. Object/File Stores

Object and File Stores work in tandem with specific Offline Stores (e.g., Spark) to serve as their storage layer. They play a critical role in storing and managing data used by these providers.

Featureform's generic interface for each of these providers allows for flexibility in managing heterogeneous infrastructure, making it possible to handle various use cases without requiring custom code for each scenario. This extensible architecture also enables the addition of new providers to meet evolving needs.
