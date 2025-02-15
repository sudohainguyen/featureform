# Versioning and Variants

Managing versioning is crucial for effective ML resource management. Featureform empowers you to implement versioning across your data sources, transformations, features, labels, and training sets. Each of these resources is inherently immutable by default, ensuring you can confidently utilize versioned resources created by others without the risk of disruption due to upstream modifications.

For each resource, there exists a *variant* parameter that can be configured either manually, automatically, or through our *ff.set_run* API. The term "variant" is preferred over "version" as it accurately reflects the nature of ML feature versions—they are not necessarily "improved" versions compared to older ones. Instead, they represent diverse interpretations of the same concept, each potentially more suited for specific use cases.

## Auto-generated Variants

Should a variant not be explicitly set, Featureform generates one automatically by combining a randomly selected adjective and noun.

## Setting all Variants in a Run

While experimenting within a notebook, it's often desirable to assign the same variant to all resources. Achieving this is straightforward using the *ff.set_run(variant)* API. This action sets the provided string parameter as the variant for all subsequent resources. Any variant parameter within those subsequent resources would supersede this setting.
