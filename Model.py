metamodel_dict = {
    "nodes": [
        {
            "type": "Person",
            "edges": ["Friends With", "Parent of", "Child of", "Sibling of", "Colleague of"],
        },
        {
            "type": "pets",
            "edges": ["owned by"]
        },
    ],
    "edges": ["Input for", "Outputs", "Executed by", "Connected to",]
}
