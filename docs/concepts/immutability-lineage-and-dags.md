# Immutability, Lineage, and Directed Acyclic Graphs (DAGs)

In the Featureform ecosystem, our declarative API establishes a DAG that outlines the relationship between resources. Starting from primary sources, these resources undergo transformations and ultimately evolve into features and training sets. For enhanced visibility and insight, you can readily explore the lineage of features through both our dashboard and CLI interfaces.

Given the intricate interdependencies inherent in a DAG structure, modifications made to a transformation that lies upstream and influences numerous other transformations and features can potentially disrupt the entire DAG. To address this concern, Featureform takes a proactive approach by enforcing immutability as the default behavior for all resources. This protective measure ensures that modifications cannot inadvertently compromise the integrity of the DAG. Should you need to extend the graph, you have the option to introduce changes by altering the resource's name or variant.

This abstraction of immutability not only safeguards the integrity of the DAG but also contributes to a heightened level of stability when your system transitions into production environments.
