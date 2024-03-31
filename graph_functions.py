# Import necessary libraries
import streamlit as st  # Streamlit for creating web applications
import networkx as nx  # NetworkX for graph analysis and manipulation
import graphviz  # Graphviz for graph visualization
from networkx.algorithms.approximation import (all_pairs_node_connectivity, local_node_connectivity)  # Importing node connectivity algorithms
from networkx.algorithms import approximation as approx  # Importing network approximation algorithms

def output_nodes_and_edges(graph: nx.Graph):
    # Display the nodes of the graph
    st.write(graph.nodes)
    # Display the edges of the graph
    st.write(graph.edges)

def count_nodes(graph: nx.Graph):
    # Count the number of nodes in the graph
    num_nodes = len(graph.nodes)
    # Display the number of nodes
    st.write(f"The graph has {num_nodes} nodes.")
    # Alternative method using NetworkX function:
    # st.write(graph.number_of_nodes())

def count_edges(graph=nx.Graph):
    # Count the number of edges in the graph
    num_edges = len(graph.edges)
    # Display the number of edges
    st.write(f"The graph has {num_edges} edges.")
    # Alternative method using NetworkX function:
    # st.write(graph.number_of_edges())

def specific_node(graph: nx.Graph):
    # Allow the user to select a specific node from the graph
    node_select = st.selectbox("Select node", options=graph.nodes, key="node_select")
    # Retrieve the selected node from the graph
    node = graph.nodes[node_select]
    # Display the details of the selected node in JSON format
    st.json(node)

def specific_edge(graph=nx.Graph):
    # Divide the Streamlit app into two columns for selecting nodes
    node1_col, node2_col = st.columns(2)

    # Retrieve the node and edge lists from the session state
    node_list = st.session_state["node_list"]
    edge_list = st.session_state["p1_list"]

    # Create a list of node names for selection
    node_name_list = [node["name"] for node in node_list]

    # Allow the user to select the first node
    with node1_col:
        node1_select = st.selectbox(
            "Select the first node",
            options=node_name_list,
            key="node1_select"  # can be added
        )

    # Allow the user to select the second node
    with node2_col:
        node2_select = st.selectbox(
            "Select the second node",
            options=node_name_list,
            key="node2_select"  # can be added
        )

    # Retrieve and display the edge data between the selected nodes
    st.write(graph.get_edge_data(node1_select, node2_select, "None"))

def density_graph(graph: nx.Graph):
    # Calculate the density of the graph
    density = nx.density(graph)

    # Display the density information
    st.info(f"The density of the graph is {density}")

def is_empty(graph: nx.Graph):
    # Check if the graph is empty
    is_empty = nx.is_empty(graph)

    # Display the result based on whether the graph is empty or not
    if is_empty:
        st.info("The graph is empty.")
    else:
        st.info("The graph is not empty.")

def check_path(graph: nx.Graph):
    # Layout for arranging the selection boxes horizontally
    node1_col, node2_col = st.columns(2)

    # Selection box for the first node
    with node1_col:
        node1_select = st.selectbox("Select first node", options=graph.nodes, key="node1_select")

    # Selection box for the second node
    with node2_col:
        node2_select = st.selectbox("Select second node", options=graph.nodes, key="node2_select")

    # Check if both nodes are selected
    if node1_select and node2_select:
        # Check if there exists a path between the selected nodes
        if nx.has_path(graph, node1_select, node2_select):
            st.success(f"There is a path between node {node1_select} and node {node2_select}.")
        else:
            st.error(f"There is no path between node {node1_select} and node {node2_select}.")

def is_directed(graph: nx.Graph):
    # Check if the graph is directed
    is_directed = nx.is_directed(graph)

    # Display the directed information
    if is_directed:
        st.info("The graph is directed.")
    else:
        st.info("The graph is not directed")

def shows_shortest_paths(graph: nx.DiGraph):
    # Retrieve graph data from session state
    graph_dict_tree = st.session_state["graph_dict"]

    # Extract node and edge lists from the graph data
    node_list_tree = graph_dict_tree["nodes"]
    edge_list_tree = graph_dict_tree["edges"]

    # Initialize lists to store found nodes and edges related to the shortest paths
    node_list_tree_found = []
    edge_list_tree_found = []

    # Extract the names of nodes from the node list
    node_name_list_tree = [node["name"] for node in node_list_tree]

    # Present a selection box to choose the start node for calculating the shortest paths
    start_node_select_tree = st.selectbox(
        "Select the start node of the shortest paths",
        options=node_name_list_tree
    )

    end_node_select_tree = st.selectbox(
        "Select the end node of the shortest paths",
        options=node_name_list_tree
    )

    # Present a button to trigger the calculation of shortest paths when clicked
    is_tree_button = st.button("Calculate trees", use_container_width=True, type="primary")

    # If the button is clicked
    if is_tree_button:
        # Calculate the shortest paths using NetworkX's shortest_path function
        tree_list = nx.shortest_path(graph, source=start_node_select_tree, target=end_node_select_tree,
                                     weight="dist")
        # tree_list = nx.shortest_path(graph, source=start_node_select_tree, target=end_node_select_tree)
        # Check if any shortest paths exist from the selected start node
        if not tree_list:
            st.write(f"There is no tree starting from {start_node_select_tree}.")
        else:
            # Iterate through each tree in the list of shortest paths
            for tree in tree_list:
                st.write(f"The node {tree} is a member of the tree")
                # For each node in the tree, identify the corresponding node data from the original node list
                for tree_element in tree:
                    for node_element in node_list_tree:
                        if node_element["name"] == tree_element:
                            to_be_assigned_element = node_element
                            # Add the node to the list of found nodes if it's not already there
                            if to_be_assigned_element not in node_list_tree_found:
                                node_list_tree_found.append(node_element)

            # Iterate through each edge in the original edge list
            for edge_element in edge_list_tree:
                for source in node_list_tree_found:
                    for target in node_list_tree_found:
                        # Check if both source and sink nodes of the edge are in the list of found nodes
                        if edge_element["source"] == source["name"] and edge_element["target"] == \
                                target["name"]:
                            # Add the edge to the list of found edges
                            edge_list_tree_found.append(edge_element)

            # Display the graph without considering the weights of the edges
            show_graph_without_weights(node_list_tree_found, edge_list_tree_found)

def show_graph_without_weights(nodes, edges):
    # Implement visualization logic here (not included for brevity)

    # Define a function to set color based on node type
    def set_color(node_type):
        color = "Grey"
        if node_type == "Person":
            color = "Blue"
        elif node_type == "Node":
            color = "Green"
        return color

    import graphviz
    graph = graphviz.Digraph()

    # Add nodes to the graph with specified colors
    for node in nodes:
        node_name = node["name"]
        graph.node(node_name, color=set_color(node["type"]))

    # Add edges to the graph
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        label = edge["type"]
        graph.edge(source, target, label)

    # Display the graph using Streamlit's graphviz_chart
    st.graphviz_chart(graph)

def shortest_path(graph: nx.DiGraph):
    import graphviz

    # Divide the layout into two columns for node selection
    node1_col, node2_col = st.columns(2)

    # Display a selection box to choose the first node
    with node1_col:
        node1_select = st.selectbox("Select first node",
                                    options=graph.nodes,
                                    key="node1_select")

    # Display a selection box to choose the second node
    with node2_col:
        node2_select = st.selectbox("Select second node",
                                    options=graph.nodes,
                                    key="node2_select")

    try:
        # Attempt to find the shortest path between the selected nodes
        shortest_path_for_graph = nx.shortest_path(graph, node1_select, node2_select)

        # Display a success message with the shortest path
        st.success(f"The shortest path between {node1_select} and {node2_select} is {shortest_path_for_graph}")

        # Display the list of nodes in the shortest path
        st.write(shortest_path_for_graph)

        # Extract the subgraph containing the shortest path
        subgraph = graph.subgraph(shortest_path_for_graph)

        # Create a Graphviz object for visualization
        graphviz_graph = graphviz.Digraph()

        # Add edges to the Graphviz object
        for edge in subgraph.edges:
            graphviz_graph.edge(str(edge[0]), str(edge[1]))

        # Display the Graphviz visualization of the shortest path
        st.graphviz_chart(graphviz_graph)

    except nx.NetworkXNoPath:
        # If no path exists between the selected nodes, display an error message
        st.error(f"There is no path between {node1_select} and {node2_select}")

def product1_visual():
    # Define a function to set colors based on node types
    def set_color(node_type):
        color = "Red"
        if node_type == "Product 1":
            color = "Blue"
        elif node_type == "Process":
            color = "Yellow"
        elif node_type == "Resource":
            color = "Green"
        return color

    # Create a Graphviz object for visualization
    graph = graphviz.Digraph()

    # Extract node and edge data from the session state
    visual_dict = {
        "nodes": st.session_state["node_list"],
        "product 1": st.session_state["p1_list"],
    }
    st.session_state["visual_dict"] = visual_dict

    node_list = visual_dict["nodes"]
    edge_list = visual_dict["product 1"]

    # Add nodes to the Graphviz object with appropriate colors
    for node in node_list:
        node_name = node["name"]
        graph.node(node_name, node_name, color=set_color(node["type"]))

    # Add edges to the Graphviz object
    for edge in edge_list:
        source = edge["source"]
        target = edge["target"]
        relation = edge["type"]
        graph.edge(source, target, relation)

    # Display the Graphviz visualization
    st.graphviz_chart(graph)

def product2_visual():
    # Define a function to set colors based on node types
    def set_color(node_type):
        color = "Red"
        if node_type == "Product 1":
            color = "Blue"
        elif node_type == "Process":
            color = "Yellow"
        elif node_type == "Resource":
            color = "Green"
        return color

    # Create a Graphviz object for visualization
    graph = graphviz.Digraph()

    # Extract node and edge data from the session state
    visual_dict = {
        "nodes": st.session_state["node_list"],
        "product 2": st.session_state["p2_list"],
    }
    st.session_state["visual_dict"] = visual_dict

    node_list = visual_dict["nodes"]
    edge_list = visual_dict["product 2"]

    # Add nodes to the Graphviz object with appropriate colors
    for node in node_list:
        node_name = node["name"]
        graph.node(node_name, node_name, color=set_color(node["type"]))

    # Add edges to the Graphviz object
    for edge in edge_list:
        source = edge["source"]
        target = edge["target"]
        relation = edge["type"]
        graph.edge(source, target, relation)

    # Display the Graphviz visualization
    st.graphviz_chart(graph)

def resource_utilization1(graph):
    # Retrieve graph data from session state
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    # Extract node data from the graph data
    node_list = st.session_state["node_list"]
    node_name_list = []

    # Define tabs for different functionalities
    tab1, tab2 = st.tabs(["Resource Utilisation",
                          "Reachability"
                          ])
    with tab1:
        # Iterate through the node list to find resource nodes
        for node in node_list:
            if node["type"] == "Resource":
                node_name_list.append(node["name"])

        # Calculate resource utilisation metrics
        r = len(node_name_list)
        st.info("Resource Utilisation")
        st.write(f" Number of Resources in the system {r}")

        name_list = []
        c = 0

        for name in node_name_list:
            for edge in edge1_list:
                if name not in name_list and (name == edge["source"] or name == edge["target"]):
                    name_list.append(name)
                    c += 1

        st.write(f" Number of Resources utilised in the system {c}")

        if r == 0:
            st.write(f"Resource Utilisation is 0")
        else:
            x = (c / r) * 100
            st.write(f"Resource Utilisation is {x} percentage")

    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        node_name_list = []
        node_name_list1 = []

        # Extract product and resource node lists
        for node in node_list:
            if node["type"] == "Product 1":
                node_name_list.append(node["name"])

        for node in node_list:
            if node["type"] == "Resource":
                node_name_list1.append(node["name"])

        # Present selection boxes to choose product and resource nodes
        with node1_col:
            node1_select = st.selectbox("Select Product",
                                        options=node_name_list,
                                        key="node1_select")
        with node2_col:
            node2_select = st.selectbox("Select Resource",
                                        options=node_name_list1,
                                        key="node2_select")
        try:
            # Calculate the shortest path between the selected product and resource nodes
            shortest_path_for_graph = nx.shortest_path(graph, node1_select, node2_select)
            st.success(f"The Resource {node2_select} is utilised by {node1_select}")
            st.write(shortest_path_for_graph)
            subgraph = graph.subgraph(shortest_path_for_graph)
            graphviz_graph = graphviz.Digraph()
            st.write(subgraph.edges)

            # Create a subgraph for visualization
            for node in subgraph.nodes:
                graphviz_graph.node(str(node))

            # Add edges to the Graphviz object
            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))
            st.graphviz_chart(graphviz_graph)
        except nx.NetworkXNoPath:
            st.error(f"There is no path between {node1_select} and {node2_select}")

def resource_utilization2(graph):
    # Retrieve graph data from session state
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    # Extract node data from the graph data
    node_list = st.session_state["node_list"]
    node_name_list = []

    # Define tabs for different functionalities
    tab1, tab2 = st.tabs(["Resource Utilisation",
                          "Reachability"
                          ])
    with tab1:
        # Iterate through the node list to find resource nodes
        for node in node_list:
            if node["type"] == "Resource":
                node_name_list.append(node["name"])

        # Calculate resource utilisation metrics
        r = len(node_name_list)
        st.info("Resource Utilisation")
        st.write(f" Number of Resources in the system {r}")

        name_list = []
        c = 0

        for name in node_name_list:
            for edge in edge2_list:
                if name not in name_list and (name == edge["source"] or name == edge["target"]):
                    name_list.append(name)
                    c += 1

        st.write(f" Number of Resources utilised in the system {c}")

        if r == 0:
            st.write(f"Resource Utilisation is 0")
        else:
            x = (c / r) * 100
            st.write(f"Resource Utilisation is {x} percentage")

    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        node_name_list = []
        node_name_list1 = []

        # Extract product and resource node lists
        for node in node_list:
            if node["type"] == "Product 2":
                node_name_list.append(node["name"])

        for node in node_list:
            if node["type"] == "Resource":
                node_name_list1.append(node["name"])

        # Present selection boxes to choose product and resource nodes
        with node1_col:
            node11_select = st.selectbox("Select Product",
                                         options=node_name_list,
                                         key="node11_select")
        with node2_col:
            node22_select = st.selectbox("Select Resource",
                                         options=node_name_list1,
                                         key="node22_select")
        try:
            # Calculate the shortest path between the selected product and resource nodes
            shortest_path_for_graph = nx.shortest_path(graph, node11_select, node22_select)
            st.success(f"The Resource {node22_select} is utilised by {node11_select}")
            st.write(shortest_path_for_graph)
            subgraph = graph.subgraph(shortest_path_for_graph)
            graphviz_graph = graphviz.Digraph()
            st.write(subgraph.edges)

            # Create a subgraph for visualization
            for node in subgraph.nodes:
                graphviz_graph.node(str(node))

            # Add edges to the Graphviz object
            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))
            st.graphviz_chart(graphviz_graph)
        except nx.NetworkXNoPath:
            st.error(f"There is no path between {node11_select} and {node22_select}")

def recurring1(graph: nx.DiGraph):
    # Retrieve necessary data from the session state
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    # Get the list of nodes from the session state
    node_list = st.session_state["node_list"]

    # Prepare a list of node names excluding those belonging to Product 2
    node_name_list = []
    product_name = ["Product 2"]
    for node in node_list:
        if node["type"] not in product_name:
            node_name_list.append(node["name"])

    # Create tabs for different analysis methods
    tab1, tab2 = st.tabs(
        ["Strongly Connected Components",
         "DFS Method - Similar Production Structures"]
    )

    # Check if the graph is empty
    if len(node_list) == 0:
        st.error("Please create a graph")
        return

    # Analyze strongly connected components
    with tab1:
        recurring_components = list(nx.strongly_connected_components(graph))
        for component in recurring_components:
            st.write(component)

    # Analyze using the DFS method
    with tab2:
        node16_select = st.selectbox("Select Product",
                                     options=node_name_list,
                                     key="node16_select")
        # Call the DFS method to identify recurring components
        dfs(graph, node16_select, recurring_components)

        st.write("Identified Recurring Components:")
        for component in recurring_components:
            st.write(component)


def recurring2(graph: nx.DiGraph):
    # Retrieve graph data from the session state
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    # Retrieve node list from the session state
    node_list = st.session_state["node_list"]

    # Initialize an empty list to store node names
    node_name_list = []

    # Define the product name for filtering
    product_name = ["Product 1"]

    # Iterate through the node list and append node names not belonging to Product 1 to node_name_list
    for node in node_list:
        if node["type"] not in product_name :
            node_name_list.append(node["name"])

    # Create tabs for different analysis methods
    tab1, tab2 = st.tabs(
        ["Strongly Connected Components",
         "DFS Method - Similar Production Structures"]
    )

    # Check if the node list is empty
    if len(node_list) == 0:
        st.error("Please Create a Graph")
        return

    # Analyze recurring components using Strongly Connected Components
    with tab1:
        # Find strongly connected components
        recurring_components = list(nx.strongly_connected_components(graph))

        # Display the identified recurring components
        for component in recurring_components:
            st.write(component)

    # Analyze recurring components using DFS Method
    with tab2:
        # Select a product from the available options
        node17_select = st.selectbox("Select Product",
                                     options=node_name_list,
                                     key="node17_select")

        # Analyze recurring components using DFS Method
        dfs(graph, node17_select, recurring_components)

        # Display the identified recurring components
        st.write("Identified Recurring Components:")
        for component in recurring_components:
            st.write(component)


def dfs(graph, start_node, recurring_components):
    visited = set()  # Keep track of visited nodes
    stack = [start_node]  # Use a stack for DFS
    current_subgraph = []  # Track current sub-graph during traversal

    while stack:
        current_node = stack.pop()
        if current_node not in visited:
            visited.add(current_node)
            current_subgraph.append(current_node)  # Add current node to sub-graph

            # Explore neighbors of the current node
            for neighbor in graph[current_node]:
                stack.append(neighbor)
                dfs(graph, neighbor, recurring_components)  # Recursive DFS call

        # Check for recurring sub-graph at the end of a branch (leaf node or backtrack)
        if current_node not in visited and len(current_subgraph) > 1:  # Avoid single-node sub-graphs
            if tuple(current_subgraph) not in recurring_components:
                recurring_components.add(tuple(current_subgraph))  # Store as immutable tuple for hashable set
            current_subgraph.pop()  # Remove current node from sub-graph (backtrack)

    recurring_components = set()  # Initialize set to store recurring sub-graphs
    # dfs(graph, node16_select, recurring_components)  # Uncomment if this function is called elsewhere


def process_on_process1(graph: nx.DiGraph):
    # Extract necessary data from session state
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    # Retrieve node list from session state
    node_list = st.session_state["node_list"]

    # Display information message
    st.info("Reachability")

    # Initialize columns for node selection
    node1_col, node2_col = st.columns(2)

    # Initialize lists to store node names
    node_name_list = []
    node_name_list1 = []

    # Populate node_name_list with process nodes
    for node in node_list:
        if node["type"] == "Process":
            node_name_list.append(node["name"])

    # Populate node_name_list1 with process nodes
    for node in node_list:
        if node["type"] == "Process":
            node_name_list1.append(node["name"])

    # User selects first process
    with node1_col:
        node12_select = st.selectbox("Select Process",
                                     options=node_name_list,
                                     key="node12_select"
                                     )
    # User selects second process
    with node2_col:
        node23_select = st.selectbox("Select Process",
                                     options=node_name_list1,
                                     key="node23_select"
                                     )

    try:
        # Calculate shortest path between selected processes
        shortest_path_for_graph = nx.shortest_path(graph, node12_select, node23_select)
        # Display success message
        st.success(f"The Process {node12_select} will have an impact on {node23_select}")
        # Display shortest path
        st.write(shortest_path_for_graph)
        # Extract subgraph representing the shortest path
        subgraph = graph.subgraph(shortest_path_for_graph)
        # Initialize Graphviz graph object
        graphviz_graph = graphviz.Digraph()

        # Add nodes to the Graphviz object
        for node in subgraph.nodes:
            graphviz_graph.node(str(node))

        # Add edges to the Graphviz object
        for edge in subgraph.edges:
            graphviz_graph.edge(str(edge[0]), str(edge[1]))

        # Visualize the subgraph using Graphviz
        st.graphviz_chart(graphviz_graph)

    except nx.NetworkXNoPath:
        # Display error message if no path exists between selected processes
        st.error(f"There is no path between {node12_select} and {node23_select}")


def process_on_process2(graph: nx.DiGraph):
    # Extract necessary data from session state
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    # Retrieve node list from session state
    node_list = st.session_state["node_list"]

    # Create tabs for user interface
    tab1, tab2 = st.tabs(
        [
            "Process",
            "Reachability"
        ]
    )

    # Display process selection tab
    with tab1:
        pass

    # Display reachability analysis tab
    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        # Initialize lists to store node names
        node_name_list = []
        node_name_list1 = []

        # Populate node_name_list with process nodes
        for node in node_list:
            if node["type"] == "Process":
                node_name_list.append(node["name"])

        # Populate node_name_list1 with process nodes
        for node in node_list:
            if node["type"] == "Process":
                node_name_list1.append(node["name"])

        # User selects first process
        with node1_col:
            node14_select = st.selectbox("Select Process",
                                         options=node_name_list,
                                         key="node14_select"
                                         )
        # User selects second process
        with node2_col:
            node25_select = st.selectbox("Select Process",
                                         options=node_name_list1,
                                         key="node25_select"
                                         )

        try:
            # Calculate shortest path between selected processes
            shortest_path_for_graph = nx.shortest_path(graph, node14_select, node25_select)
            # Display success message
            st.success(f"The Process {node14_select} will have an impact on {node25_select}")
            # Display shortest path
            st.write(shortest_path_for_graph)
            # Extract subgraph representing the shortest path
            subgraph = graph.subgraph(shortest_path_for_graph)
            # Initialize Graphviz graph object
            graphviz_graph = graphviz.Digraph()

            # Add nodes to the Graphviz object
            for node in subgraph.nodes:
                graphviz_graph.node(str(node))

            # Add edges to the Graphviz object
            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))

            # Visualize the subgraph using Graphviz
            st.graphviz_chart(graphviz_graph)

        except nx.NetworkXNoPath:
            # Display error message if no path exists between selected processes
            st.error(f"There is no path between {node14_select} and {node25_select}")


def input_product_on_process1(graph: nx.DiGraph):
    # Extract necessary data from session state
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    # Retrieve node list from session state
    node_list = st.session_state["node_list"]
    node_name_list = []

    # Create tabs for user interface
    tab1, tab2 = st.tabs(
        [
            "Process Utilisation",
            "Reachability"
        ]
    )

    # Display process utilisation tab
    with tab1:
        # Populate node_name_list with process nodes
        for node in node_list:
            if node["type"] == "Process":
                node_name_list.append(node["name"])

        # Calculate number of processes in the system
        r = len(node_name_list)

        # Display process utilisation information
        st.info("Process Utilisation")
        st.write(f" Number of Processes in the system {r}")

        # Initialize list to store unique process names involved in product 1 edges
        name_list = []
        c = 0

        # Count processes performed in the system
        for name in node_name_list:
            for edge in edge1_list:
                if name not in name_list and (name == edge["source"] or name == edge["target"]):
                    name_list.append(name)
                    c += 1
        st.write(f" Number of Processes performed in the system {c}")

        # Calculate process utilisation percentage
        if r == 0:
            st.write(f"Process Utilisation is 0")
        else:
            x = (c / r) * 100
            st.write(f"Process Utilisation is {x} percentage")

    # Display reachability analysis tab
    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        node_name_list = []
        node_name_list1 = []

        # Populate node_name_list with input product nodes
        for node in node_list:
            if node["type"] == "Product 1":
                node_name_list.append(node["name"])

        # Populate node_name_list1 with process nodes
        for node in node_list:
            if node["type"] == "Process":
                node_name_list1.append(node["name"])

        # User selects input product
        with node1_col:
            node13_select = st.selectbox("Select Product",
                                         options=node_name_list,
                                         key="node13_select")
        # User selects process
        with node2_col:
            node24_select = st.selectbox("Select Process",
                                         options=node_name_list1,
                                         key="node24_select")

        try:
            # Calculate shortest path between selected product and process
            shortest_path_for_graph = nx.shortest_path(graph, node13_select, node24_select)
            # Display success message
            st.success(f"Based on the input product {node13_select} the following {node24_select} process "
                       f"will be executed")
            st.write(shortest_path_for_graph)
            # Extract subgraph representing the shortest path
            subgraph = graph.subgraph(shortest_path_for_graph)
            # Initialize Graphviz graph object
            graphviz_graph = graphviz.Digraph()

            # Add nodes to the Graphviz object
            for node in subgraph.nodes:
                graphviz_graph.node(str(node))

            # Add edges to the Graphviz object
            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))

            # Visualize the subgraph using Graphviz
            st.graphviz_chart(graphviz_graph)

        except nx.NetworkXNoPath:
            # Display error message if no path exists between selected product and process
            st.error(f"There is no path between {node13_select} and {node24_select}")

def input_product_on_process2(graph: nx.DiGraph):
    # Extract necessary data from session state
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    # Retrieve node list from session state
    node_list = st.session_state["node_list"]
    node_name_list = []

    # Create tabs for user interface
    tab1, tab2 = st.tabs(
        [
            "Process Utilisation",
            "Reachability"
        ]
    )

    # Display process utilisation tab
    with tab1:
        # Populate node_name_list with process nodes
        for node in node_list:
            if node["type"] == "Process":
                node_name_list.append(node["name"])

        # Calculate number of processes in the system
        r = len(node_name_list)

        # Display process utilisation information
        st.info("Process Utilisation")
        st.write(f" Number of Processes in the system {r}")

        # Initialize list to store unique process names involved in product 2 edges
        name_list = []
        c = 0

        # Count processes performed in the system
        for name in node_name_list:
            for edge in edge2_list:
                if name not in name_list and (name == edge["source"] or name == edge["target"]):
                    name_list.append(name)
                    c += 1
        st.write(f" Number of Processes performed in the system {c}")

        # Calculate process utilisation percentage
        if r == 0:
            st.write(f"Process Utilisation is 0")
        else:
            x = (c / r) * 100
            st.write(f"Process Utilisation is {x} percentage")

    # Display reachability analysis tab
    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        node_name_list = []
        node_name_list1 = []

        # Populate node_name_list with input product nodes
        for node in node_list:
            if node["type"] == "Product 2":
                node_name_list.append(node["name"])

        # Populate node_name_list1 with process nodes
        for node in node_list:
            if node["type"] == "Process":
                node_name_list1.append(node["name"])

        # User selects input product
        with node1_col:
            node15_select = st.selectbox("Select Product",
                                         options=node_name_list,
                                         key="node15_select")
        # User selects process
        with node2_col:
            node25_select = st.selectbox("Select Process",
                                         options=node_name_list1,
                                         key="node25_select")

        try:
            # Calculate shortest path between selected product and process
            shortest_path_for_graph = nx.shortest_path(graph, node15_select, node25_select)
            # Display success message
            st.success(f"Based on the input product {node15_select} the following {node25_select} process "
                       f"will be executed")
            st.write(shortest_path_for_graph)
            # Extract subgraph representing the shortest path
            subgraph = graph.subgraph(shortest_path_for_graph)
            # Initialize Graphviz graph object
            graphviz_graph = graphviz.Digraph()

            # Add nodes to the Graphviz object
            for node in subgraph.nodes:
                graphviz_graph.node(str(node))

            # Add edges to the Graphviz object
            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))

            # Visualize the subgraph using Graphviz
            st.graphviz_chart(graphviz_graph)

        except nx.NetworkXNoPath:
            # Display error message if no path exists between selected product and process
            st.error(f"There is no path between {node15_select} and {node25_select}")

