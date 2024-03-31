# Define a metamodel dictionary containing node and edge types
metamodel_dict = {
    # Define node types
    "nodes": [
        {
            # Define a node type: Person
            "type": "Person",
            # Specify relationships associated with the Person node type
            "edges": ["Friends With", "Parent of", "Child of", "Sibling of", "Colleague of"],
        },
        {
            # Define a node type: Pet
            "type": "Pet",
            # Specify relationship associated with the Pet node type
            "edges": ["Owned by"]
        },
    ],
    # Define edge types
    "edges": ["Input for", "Outputs", "Executed by", "Connected to",]
}
