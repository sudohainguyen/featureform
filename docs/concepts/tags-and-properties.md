# Setting Custom Tags and Properties

In Featureform, your ML data resources' metadata is stored comprehensively. Our metadata engine offers adaptability, enabling you to establish personalized tags and properties. These become particularly crucial when utilizing our Governance APIs within Featureform Enterprise.

Each registration call incorporates two parameters: tags and properties. tags takes the form of a Python list containing strings, while properties is a dictionary encompassing scalar values (strings and numbers). These attributes can be conveniently accessed, searched, and modified through the Feature Registry UI as well.
