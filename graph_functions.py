import streamlit as st
import networkx as nx
import graphviz
import community
from networkx.algorithms.approximation import (all_pairs_node_connectivity, local_node_connectivity)
from networkx.algorithms import approximation as approx


def output_nodes_and_edges(graph: nx.Graph):
    st.write(graph.nodes)
    st.write(graph.edges)


def count_nodes(graph: nx.Graph):
    num_nodes = len(graph.nodes)
    st.write(f"the Graph has", num_nodes, "of nodes")
    # st.write(graph.number_of_nodes())


def count_edges(graph=nx.Graph):
    num_edges = len(graph.edges)
    st.write(f"the Graph has", num_edges, "of edges")
    # st.write(graph.number_of_edges())


def specific_node(graph: nx.Graph):
    node_select = st.selectbox("Select node", options=graph.nodes, key="node_select")
    node = graph.nodes[node_select]
    st.json(node)


def specific_edge(graph=nx.Graph):
    node1_col, node2_col = st.columns(2)
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge_list = graph_dict["product 1"]

    node_list = st.session_state["node_list"]
    node_name_list = []
    for node in node_list:
        node_name_list.append(node["name"])
    with node1_col:
        node1_select = st.selectbox(
            "select the first node",
            options=node_name_list,
            key="node1_select"  # can be added
        )
    with node2_col:
        node2_select = st.selectbox(
            "select the second node",
            options=node_name_list,
            key="node2_select"  # can be added
        )
    st.write(graph.get_edge_data(node1_select, node2_select, "None"))


def density_graph(graph: nx.Graph):
    density = nx.density(graph)
    st.info(f"The density of graph is {density}")


def is_empty(graph: nx.Graph):
    is_empty = nx.is_empty(graph)
    if is_empty:
        st.info("The graph is empty.")
    else:
        st.info("The graph is not empty.")


def check_path(graph: nx.Graph):
    node1_col, node2_col = st.columns(2)
    with node1_col:
        node1_select = st.selectbox("Select first node", options=graph.nodes, key="node1_select")
    with node2_col:
        node2_select = st.selectbox("Select second node", options=graph.nodes, key="node2_select")
    if node1_select and node2_select:
        if nx.has_path(graph, node1_select, node2_select):
            st.success(f"There is a path between node {node1_select} and node {node2_select}.")
        else:
            st.error(f"There is no path between node {node1_select} and node {node2_select}.")


def is_directed(graph: nx.Graph):
    is_directed = nx.is_directed(graph)
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


# Function to display the graph without considering edge weights
def show_graph_without_weights(nodes, edges):
    # Implement visualization logic here (not included for brevity)

    def set_color(node_type):
        color = "Grey"
        if node_type == "Person":
            color = "Blue"
        elif node_type == "Node":
            color = "Green"
        return color

    import graphviz
    graph = graphviz.Digraph()
    for node in nodes:
        node_name = node["name"]
        graph.node(node_name, color=set_color(node["type"]))
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        label = edge["type"]
        graph.edge(source, target, label)
    st.graphviz_chart(graph)


def shortest_path(graph: nx.DiGraph):
    import graphviz
    node1_col, node2_col = st.columns(2)
    with node1_col:
        node1_select = st.selectbox("Select first node",
                                    options=graph.nodes,
                                    key="node1_select")
    with node2_col:
        node2_select = st.selectbox("Select second node",
                                    options=graph.nodes,
                                    key="node2_select")
    try:
        shortest_path_for_graph = nx.shortest_path(graph, node1_select, node2_select)
        st.success(f"The shortest path between {node1_select} "
                   f"and {node2_select} is {shortest_path_for_graph}")
        st.write(shortest_path_for_graph)
        subgraph = graph.subgraph(shortest_path_for_graph)
        graphviz_graph = graphviz.Digraph()
        st.write(subgraph.edges)

        for node in subgraph.nodes:
            graphviz_graph.node(str(node))
            # Add edges to the Graphviz object

        for edge in subgraph.edges:
            graphviz_graph.edge(str(edge[0]), str(edge[1]))
        st.graphviz_chart(graphviz_graph)
    except nx.NetworkXNoPath:
        st.error(f"There is no path between {node1_select} and {node2_select}")


def product1_visual():
    # with st.expander("Visualise the Graph of Product 1"):
    def set_color(node_type):
        color = "Red"
        if node_type == "Product 1":
            color = "Blue"
        elif node_type == "Process":
            color = "Yellow"
        elif node_type == "Resource":
            color = "Green"
        return color

    graph = graphviz.Digraph()

    visual_dict = {
        "nodes": st.session_state["node_list"],
        "product 1": st.session_state["p1_list"],
    }
    st.session_state["visual_dict"] = visual_dict

    node_list = visual_dict["nodes"]
    edge_list = visual_dict["product 1"]

    for node in node_list:
        node_name = node["name"]
        graph.node(node_name, node_name, color=set_color(node["type"]))
    for edge in edge_list:
        source = edge["source"]
        target = edge["target"]
        relation = edge["type"]
        graph.edge(source, target, relation)
    st.graphviz_chart(graph)


def product2_visual():
    def set_color(node_type):
        color = "Red"
        if node_type == "Product 1":
            color = "Blue"
        elif node_type == "Process":
            color = "Yellow"
        elif node_type == "Resource":
            color = "Green"
        return color

    graph = graphviz.Digraph()

    visual_dict = {
        "nodes": st.session_state["node_list"],
        "product 2": st.session_state["p2_list"],
    }
    st.session_state["visual_dict"] = visual_dict

    node_list = visual_dict["nodes"]
    edge_list = visual_dict["product 2"]
    for node in node_list:
        node_name = node["name"]
        graph.node(node_name, node_name, color=set_color(node["type"]))
    for edge in edge_list:
        source = edge["source"]
        target = edge["target"]
        relation = edge["type"]
        graph.edge(source, target, relation)
    st.graphviz_chart(graph)


def resource_utilization1(graph):
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    node_list = st.session_state["node_list"]
    node_name_list = []

    tab1, tab2 = st.tabs(["Resource Utilisation",
                          "Reachability"
                          ])
    with tab1:
        for node in node_list:
            if node["type"] == "Resource":
                node_name_list.append(node["name"])
        # st.write(node_name_list)
        r = len(node_name_list)

        st.info("Resource Utilisation")

        st.write(f" Number of Resources in the system {r}")

        name_list = []
        name_list2 = []
        c = 0

        for name in node_name_list:
            for edge in edge1_list:
                if name not in name_list and (name == edge["source"] or name == edge["target"]):
                    name_list.append(name)
                    c = c + 1
                # elif name in name_list and (name != edge["source"] or name != edge["target"]):
                #   name_list2.append(name)
            # st.write(name_list2)
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

        for node in node_list:
            if node["type"] == "Product 1":
                node_name_list.append(node["name"])
        # st.write(node_name_list)

        for node in node_list:
            if node["type"] == "Resource":
                node_name_list1.append(node["name"])

        with node1_col:
            node1_select = st.selectbox("Select Product",
                                        options=node_name_list,
                                        key="node1_select")
        with node2_col:
            node2_select = st.selectbox("Select Resource",
                                        options=node_name_list1,
                                        key="node2_select")
        try:
            shortest_path_for_graph = nx.shortest_path(graph, node1_select, node2_select)
            st.success(f"The Resource {node2_select} is utilised by {node1_select}")
            st.write(shortest_path_for_graph)
            subgraph = graph.subgraph(shortest_path_for_graph)
            graphviz_graph = graphviz.Digraph()
            st.write(subgraph.edges)

            for node in subgraph.nodes:
                graphviz_graph.node(str(node))
                # Add edges to the Graphviz object

            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))
            st.graphviz_chart(graphviz_graph)
        except nx.NetworkXNoPath:
            st.error(f"There is no path between {node1_select} and {node2_select}")


def resource_utilization2(graph):
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    node_list = st.session_state["node_list"]
    node_name_list = []

    tab1, tab2 = st.tabs(["Resource Utilisation",
                          "Reachability"
                          ])
    with tab1:
        for node in node_list:
            if node["type"] == "Resource":
                node_name_list.append(node["name"])

        r = len(node_name_list)

        st.info("Resource Utilisation")

        st.write(f" Number of Resources in the system {r}")

        name_list = []
        c = 0

        for name in node_name_list:
            for edge in edge2_list:
                if name not in name_list and (name == edge["source"] or name == edge["target"]):
                    name_list.append(name)
                    c = c + 1

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

        for node in node_list:
            if node["type"] == "Product 2":
                node_name_list.append(node["name"])
        # st.write(node_name_list)

        for node in node_list:
            if node["type"] == "Resource":
                node_name_list1.append(node["name"])

        with node1_col:
            node11_select = st.selectbox("Select Product",
                                         options=node_name_list,
                                         key="node11_select")
        with node2_col:
            node22_select = st.selectbox("Select Resource",
                                         options=node_name_list1,
                                         key="node22_select")
        try:
            shortest_path_for_graph = nx.shortest_path(graph, node11_select, node22_select)
            st.success(f"The Resource {node22_select} is utilised by {node11_select}")
            st.write(shortest_path_for_graph)
            subgraph = graph.subgraph(shortest_path_for_graph)
            graphviz_graph = graphviz.Digraph()
            st.write(subgraph.edges)

            for node in subgraph.nodes:
                graphviz_graph.node(str(node))
                # Add edges to the Graphviz object

            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))
            st.graphviz_chart(graphviz_graph)
        except nx.NetworkXNoPath:
            st.error(f"There is no path between {node11_select} and {node22_select}")


def recurring1(graph: nx.DiGraph):
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    node_list = st.session_state["node_list"]

    node_name_list = []

    for node in node_list:
        node_name_list.append(node["name"])

    tab1, tab2 = st.tabs(
        ["Strongly Connected Components",
         "DFS Method - Similar Production Structures"]
    )

    with tab1:
        recurring_components = list(nx.strongly_connected_components(graph))

        # st.write(recurring_components)

        for component in recurring_components:
            st.write(component)

    with tab2:
        node16_select = st.selectbox("Select Product",
                                     options=node_name_list,
                                     key="node16_select")

        dfs(graph,node16_select, recurring_components)

        st.write("Identified Recurring Components:")
        for component in recurring_components:
            st.write(component)


def recurring2(graph: nx.DiGraph):
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    node_list = st.session_state["node_list"]

    node_name_list = []
    product_name = ["Product 1"]
    for node in node_list:
        if node["type"] not in product_name :
            node_name_list.append(node["name"])

    tab1, tab2 = st.tabs(
        ["Strongly Connected Components",
         "DFS Method - Similar Production Structures"]
    )

    with tab1:
        recurring_components = list(nx.strongly_connected_components(graph))

        # st.write(recurring_components)

        for component in recurring_components:
            st.write(component)

    with tab2:
        node17_select = st.selectbox("Select Product",
                                     options=node_name_list,
                                     key="node17_select")

        dfs(graph, node17_select, recurring_components)

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

          for neighbor in graph[current_node]:
            stack.append(neighbor)
            dfs(graph, neighbor, recurring_components)  # Recursive DFS call

        # Check for recurring sub-graph at the end of a branch (leaf node or backtrack)
        if current_node not in visited and len(current_subgraph) > 1:  # Avoid single-node sub-graphs
          if current_subgraph not in recurring_components:
            recurring_components.add(tuple(current_subgraph))  # Store as immutable tuple for hashable set
          current_subgraph.pop()  # Remove current node from sub-graph (backtrack)

    recurring_components = set()
    #dfs(graph, node16_select, recurring_components)



def process_on_process1(graph: nx.DiGraph):

    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    node_list = st.session_state["node_list"]

    tab1, tab2 = st.tabs(
        [
            "Process",
            "Reachability"
        ]
    )

    with tab1:
        pass

    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        node_name_list = []
        node_name_list1 = []

        for node in node_list:
            if node["type"] == "Process":
                node_name_list.append(node["name"])
        # st.write(node_name_list)

        for node in node_list:
            if node["type"] == "Process":
                node_name_list1.append(node["name"])

        with node1_col:
            node12_select = st.selectbox("Select Process",
                                         options=node_name_list,
                                         key="node12_select"
                                         )
        with node2_col:
            node23_select = st.selectbox("Select Process",
                                         options=node_name_list1,
                                         key="node23_select"
                                         )
        try:
            shortest_path_for_graph = nx.shortest_path(graph, node12_select, node23_select)
            st.success(f"The Process {node12_select} will have an impact on {node23_select}")
            st.write(shortest_path_for_graph)
            subgraph = graph.subgraph(shortest_path_for_graph)
            graphviz_graph = graphviz.Digraph()
            st.write(subgraph.edges)

            for node in subgraph.nodes:
                graphviz_graph.node(str(node))
                # Add edges to the Graphviz object

            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))
            st.graphviz_chart(graphviz_graph)
        except nx.NetworkXNoPath:
            st.error(f"There is no path between {node12_select} and {node23_select}")

def process_on_process2(graph: nx.DiGraph):

    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    node_list = st.session_state["node_list"]

    tab1, tab2 = st.tabs(
        [
            "Process",
            "Reachability"
        ]
    )

    with tab1:
        pass

    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        node_name_list = []
        node_name_list1 = []

        for node in node_list:
            if node["type"] == "Process":
                node_name_list.append(node["name"])
        # st.write(node_name_list)

        for node in node_list:
            if node["type"] == "Process":
                node_name_list1.append(node["name"])

        with node1_col:
            node14_select = st.selectbox("Select Process",
                                         options=node_name_list,
                                         key="node14_select"
                                         )
        with node2_col:
            node25_select = st.selectbox("Select Process",
                                         options=node_name_list1,
                                         key="node25_select"
                                         )
        try:
            shortest_path_for_graph = nx.shortest_path(graph, node14_select, node25_select)
            st.success(f"The Process {node14_select} will have an impact on {node25_select}")
            st.write(shortest_path_for_graph)
            subgraph = graph.subgraph(shortest_path_for_graph)
            graphviz_graph = graphviz.Digraph()
            st.write(subgraph.edges)

            for node in subgraph.nodes:
                graphviz_graph.node(str(node))
                # Add edges to the Graphviz object

            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))
            st.graphviz_chart(graphviz_graph)
        except nx.NetworkXNoPath:
            st.error(f"There is no path between {node14_select} and {node25_select}")

def input_product_on_process1(graph: nx.DiGraph):
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    node_list = st.session_state["node_list"]
    node_name_list = []

    tab1, tab2 = st.tabs(
        [
            "Process Utilisation",
            "Reachability"
        ]
    )

    with tab1:

        for node in node_list:
            if node["type"] == "Process":
                node_name_list.append(node["name"])

        r = len(node_name_list)

        st.info("Process Utilisation")

        st.write(f" Number of Processes in the system {r}")

        name_list = []
        c = 0

        for name in node_name_list:
            for edge in edge1_list:
                if name not in name_list and (name == edge["source"] or name == edge["target"]):
                    name_list.append(name)
                    c = c + 1
        st.write(f" Number of Processes performed in the system {c}")

        if r == 0:
            st.write(f"Process Utilisation is 0")
        else:
            x = (c / r) * 100
            st.write(f"Process Utilisation is {x} percentage")

    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        node_name_list = []
        node_name_list1 = []

        for node in node_list:
            if node["type"] == "Product 1":
                node_name_list.append(node["name"])
        # st.write(node_name_list)

        for node in node_list:
            if node["type"] == "Process":
                node_name_list1.append(node["name"])

        with node1_col:
            node13_select = st.selectbox("Select Product",
                                         options=node_name_list,
                                         key="node13_select")
        with node2_col:
            node24_select = st.selectbox("Select Process",
                                         options=node_name_list1,
                                         key="node24_select")
        try:
            shortest_path_for_graph = nx.shortest_path(graph, node13_select, node24_select)
            st.success(f"Based on the input product {node13_select} the following {node24_select} process "
                       f" will be executed"
                       )
            st.write(shortest_path_for_graph)
            subgraph = graph.subgraph(shortest_path_for_graph)
            graphviz_graph = graphviz.Digraph()
            st.write(subgraph.edges)

            for node in subgraph.nodes:
                graphviz_graph.node(str(node))
                # Add edges to the Graphviz object

            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))
            st.graphviz_chart(graphviz_graph)
        except nx.NetworkXNoPath:
            st.error(f"There is no path between {node13_select} and {node24_select}")


def input_product_on_process2(graph: nx.DiGraph):
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge1_list = graph_dict["product 1"]
    edge2_list = graph_dict["product 2"]

    node_list = st.session_state["node_list"]
    node_name_list = []

    tab1, tab2 = st.tabs(
        [
            "Process Utilisation",
            "Reachability"
        ]
    )

    with tab1:
        for node in node_list:
            if node["type"] == "Process":
                node_name_list.append(node["name"])

        r = len(node_name_list)

        st.info("Process Utilisation")

        st.write(f" Number of Processes in the system {r}")

        name_list = []
        c = 0

        for name in node_name_list:
            for edge in edge2_list:
                if name not in name_list and (name == edge["source"] or name == edge["target"]):
                    name_list.append(name)
                    c = c + 1
        st.write(f" Number of Processes performed in the system {c}")

        if r == 0:
            st.write(f"Process Utilisation is 0")
        else:
            x = (c / r) * 100
            st.write(f"Process Utilisation is {x} percentage")

    with tab2:
        import graphviz
        node1_col, node2_col = st.columns(2)

        node_name_list = []
        node_name_list1 = []

        for node in node_list:
            if node["type"] == "Product 2":
                node_name_list.append(node["name"])
        # st.write(node_name_list)

        for node in node_list:
            if node["type"] == "Process":
                node_name_list1.append(node["name"])

        with node1_col:
            node15_select = st.selectbox("Select Product",
                                         options=node_name_list,
                                         key="node15_select")
        with node2_col:
            node25_select = st.selectbox("Select Process",
                                         options=node_name_list1,
                                         key="node25_select")
        try:
            shortest_path_for_graph = nx.shortest_path(graph, node15_select, node25_select)
            st.success(f"Based on the input product {node15_select} the following {node25_select} process "
                       f" will be executed"
                       )
            st.write(shortest_path_for_graph)
            subgraph = graph.subgraph(shortest_path_for_graph)
            graphviz_graph = graphviz.Digraph()
            st.write(subgraph.edges)

            for node in subgraph.nodes:
                graphviz_graph.node(str(node))
                # Add edges to the Graphviz object

            for edge in subgraph.edges:
                graphviz_graph.edge(str(edge[0]), str(edge[1]))
            st.graphviz_chart(graphviz_graph)
        except nx.NetworkXNoPath:
            st.error(f"There is no path between {node15_select} and {node25_select}")
