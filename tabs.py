import streamlit as st  # Import Streamlit library for building web applications
import json  # Import JSON library for handling JSON data
from Model import metamodel_dict  # Import metamodel dictionary from Model module
import uuid  # Import UUID library for generating unique identifiers
import graphviz  # Import Graphviz for graph visualization
from streamlit_agraph import agraph, Node, Edge, Config  # Import streamlit_agraph for rendering graph
import networkx as nx  # Import NetworkX library for graph manipulation
from graph_functions import (output_nodes_and_edges, count_nodes, count_edges, density_graph,
                             check_path, is_empty, is_directed, shortest_path, specific_node,
                             specific_edge, product1_visual, product2_visual, resource_utilization1,
                             resource_utilization2, recurring1, process_on_process1, input_product_on_process1,
                             process_on_process2, input_product_on_process2, recurring2)  # Import custom graph functions
from networkx.algorithms.approximation import (all_pairs_node_connectivity, local_node_connectivity)  # Import algorithms for node connectivity

# Function to upload an existing graph
def upload_graph():
    uploaded_graph = st.file_uploader("upload an existing graph", type="json")  # Upload JSON file
    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)  # Load JSON data
        uploaded_nodes = uploaded_graph_dict["nodes"]  # Extract nodes from the uploaded graph
        uploaded_p1 = uploaded_graph_dict["product 1"]  # Extract product 1 edges
        uploaded_p2 = uploaded_graph_dict["product 2"]  # Extract product 2 edges
        st.json(uploaded_graph_dict, expanded=False)  # Display uploaded graph data
    else:
        st.info("Please upload a graph if available")  # Inform user to upload a graph if not available

    # Button to update the graph via the uploaded file
    update_graph_button = st.button(
        "update graph via the upload",
        use_container_width=True,
        type="primary"
    )
    if update_graph_button and uploaded_graph:
        # Update session state with uploaded graph data
        st.session_state["node_list"] = uploaded_nodes
        st.session_state["p1_list"] = uploaded_p1
        st.session_state["p2_list"] = uploaded_p2

        # Create graph dictionary from uploaded graph data
        graph_dict = {
            "nodes": st.session_state["node_list"],
            "product 1": st.session_state["p1_list"],
            "product 2": st.session_state["p2_list"],
        }
        st.session_state["graph_dict"] = graph_dict  # Update session state with the new graph dictionary

# Function to create a new node
def create_node():
    # Function to save engineering data
    def save_engineering(cost, target_values, mttf, oee, mttr):
        engineering_dict = {
            "Cost": cost,
            "Target Values": target_values,
            "OEE": oee,
            "MTTR": mttr,
            "MTTF": mttf
        }
        return engineering_dict

    # Function to save electrical data
    def save_electrical(current, voltage, power, resistance):
        electrical_dict = {
            "current": current,
            "voltage": voltage,
            "power": power,
            "resistance": resistance,
        }
        return electrical_dict

    # Function to save sustainable data
    def save_sustainable(CO2_footprint, energy_consumption, reusability, repairability):
        sustainable_dict = {
            "CO2 footprint": CO2_footprint,
            "energy consumption": energy_consumption,
            "reusability": reusability,
            "repairability": repairability,
        }
        return sustainable_dict

    # Function to save views
    def save_views(engineering, electrical, sustainable):
        view_dict = {
            "Engineering": engineering,
            "Electrical": electrical,
            "Sustainable": sustainable
        }
        return view_dict

    # Function to save node
    def save_node(name, views, type_n):
        node_dict = {
            "name": name,
            "submodels": views,
            "id": str(uuid.uuid4()),
            "type": type_n
        }
        st.session_state["node_list"].append(node_dict)  # Append node to session state node list

    # Input fields for node creation
    name_node = st.text_input("Type in the name of the node")
    type_node = st.selectbox("Specify the type of the node",
                             ["Product 1", "Product 2", "Process", "Resource"])

    # Tabs for different data categories
    engineering_node, electrical_node, sustainable_node = st.tabs(
        [
            "Engineering Data",
            "Electrical Data",
            "Sustainable Data"
        ]
    )

    with engineering_node:
        # Input fields for engineering data
        cost = st.text_input("COST")
        target_values = st.text_input("Target Value")
        mttf_data = st.text_input("MTTF")
        oee_data = st.text_input("OEE DATA (percentage)")
        mttr_data = st.text_input("MTTR DATA (minutes)")

        engineering_data = save_engineering(cost, target_values, mttf_data, oee_data, mttr_data)

    with electrical_node:
        # Input fields for electrical data
        current = st.text_input("current (amp)")
        voltage = st.text_input("voltage (volts)")
        power = st.text_input("power (watt)")
        resistance = st.text_input("resistance (ohms)")
        electrical_data = save_electrical(current, voltage, power, resistance)

    with sustainable_node:
        # Input fields for sustainable data
        CO2_footprint = st.text_input("CO2 footprint (kilotons)")
        energy_consumption = st.text_input("energy consumption (kWh)")
        reusability = st.text_input("reusability (percentage)")
        repairability = st.text_input("repairability (percentage)")
        sustainable_data = save_sustainable(CO2_footprint, energy_consumption, reusability, repairability)

    # Combine data from different categories
    views_data = save_views(engineering_data, electrical_data, sustainable_data)

    # Button to store the node
    save_node_button = st.button("Store Node", use_container_width=True, type="primary")
    if save_node_button:
        save_node(name_node, views_data, type_node)  # Call save_node function to store the node

    st.json(st.session_state["node_list"], expanded=False)  # Display the stored nodes

def update_node():
    # Retrieve node and edge lists from session state
    node_list = st.session_state["node_list"]
    edge1_list = st.session_state["p1_list"]
    edge2_list = st.session_state["p2_list"]
    # Extract node names from the node list
    node_names = [node["name"] for node in node_list]

    try:
        # Select the node to update
        node_to_update = st.selectbox("Select node to update", options=node_names)

        # Find the index of the selected node in the list
        selected_index = node_names.index(node_to_update)
        selected_node = node_list[selected_index]

        # Display current node properties
        st.write(f"Current properties of node '{node_to_update}':")
        st.write(selected_node)

        # Allow users to update node properties
        custom_node_name = st.text_input("Enter new name for the node", value=selected_node["name"])
        new_type = st.selectbox("Select new type for the node", options=["Product 1", "Product 2", "Process", "Resource"])

        st.write("Attributes to Update")
        tab1, tab2, tab3 = st.tabs(["Engineering Data", "Electrical Data", "Sustainabilty Data"])

        # Engineering Data
        with tab1:
            cost = st.text_input("Cost", value=selected_node["submodels"]["Engineering"]["Cost"])
            target_values = st.text_input("Target Value", value=selected_node["submodels"]["Engineering"]["Target Values"])
            mttf_data = st.text_input("MTTF", value=selected_node["submodels"]["Engineering"]["MTTF"])
            oee_data = st.text_input("OEE DATA (percentage)", value=selected_node["submodels"]["Engineering"]["OEE"])
            mttr_data = st.text_input("MTTR DATA (minutes)", value=selected_node["submodels"]["Engineering"]["MTTR"])

        # Electrical Data
        with tab2:
            current = st.text_input("Current (amp)", value=selected_node["submodels"]["Electrical"]["current"])
            voltage = st.text_input("Voltage (volts)", value=selected_node["submodels"]["Electrical"]["voltage"])
            power = st.text_input("Power (watt)", value=selected_node["submodels"]["Electrical"]["power"])
            resistance = st.text_input("Resistance (ohms)", value=selected_node["submodels"]["Electrical"]["resistance"])

        # Sustainability Data
        with tab3:
            CO2_footprint = st.text_input("CO2 footprint (kilotons)", value=selected_node["submodels"]["Sustainable"]["CO2 footprint"])
            energy_consumption = st.text_input("Energy consumption (kWh)", value=selected_node["submodels"]["Sustainable"]["energy consumption"])
            reusability = st.text_input("Reusability (percentage)", value=selected_node["submodels"]["Sustainable"]["reusability"])
            repairability = st.text_input("Repairability (percentage)", value=selected_node["submodels"]["Sustainable"]["repairability"])

        # Generate a dynamic key based on the selected node
        update_node_button_key = f"update_node_button_{node_to_update}"
        update_node_button = st.button("Update Node", key=update_node_button_key, use_container_width=True, type="primary")

        if update_node_button:
            # Update node properties
            node_list[selected_index]["name"] = custom_node_name
            node_list[selected_index]["type"] = new_type
            node_list[selected_index]["submodels"]["Engineering"]["Cost"] = cost
            node_list[selected_index]["submodels"]["Engineering"]["Target Values"] = target_values
            node_list[selected_index]["submodels"]["Engineering"]["MTTF"] = mttf_data
            node_list[selected_index]["submodels"]["Engineering"]["OEE"] = oee_data
            node_list[selected_index]["submodels"]["Engineering"]["MTTR"] = mttr_data
            node_list[selected_index]["submodels"]["Electrical"]["current"] = current
            node_list[selected_index]["submodels"]["Electrical"]["voltage"] = voltage
            node_list[selected_index]["submodels"]["Electrical"]["power"] = power
            node_list[selected_index]["submodels"]["Electrical"]["resistance"] = resistance
            node_list[selected_index]["submodels"]["Sustainable"]["CO2 footprint"] = CO2_footprint
            node_list[selected_index]["submodels"]["Sustainable"]["energy consumption"] = energy_consumption
            node_list[selected_index]["submodels"]["Sustainable"]["reusability"] = reusability
            node_list[selected_index]["submodels"]["Sustainable"]["repairability"] = repairability

            # Update edges connected to the selected node
            updated_edges1 = []
            for edge in edge1_list:
                if edge["source"] == node_to_update:
                    edge["source"] = custom_node_name
                if edge["target"] == node_to_update:
                    edge["target"] = custom_node_name
                updated_edges1.append(edge)

            updated_edges2 = []
            for edge in edge2_list:
                if edge["source"] == node_to_update:
                    edge["source"] = custom_node_name
                if edge["target"] == node_to_update:
                    edge["target"] = custom_node_name
                updated_edges2.append(edge)

            # Update session state with the modified node and edge lists
            st.session_state["node_list"] = node_list
            st.session_state["p1_list"] = updated_edges1
            st.session_state["p2_list"] = updated_edges2

            st.success(f"Node '{node_to_update}' and connected edges have been updated.")

            st.experimental_rerun()  # Force the UI to update immediately

    except ValueError:
        st.error("There are no nodes added yet. Please create nodes or import a graph")

# Function to delete a node
def delete_node():
    import time
    node_list = st.session_state["node_list"]
    node_names = [node["name"] for node in node_list]

    node_to_delete = st.selectbox("Select node to delete", options=node_names)
    delete_node_button = st.button("Delete Node", key="delete_node_button", use_container_width=True, type="primary")

    if delete_node_button:
        # Remove the node from the node list
        st.session_state["node_list"] = [node for node in node_list if node["name"] != node_to_delete]

        # Remove edges connected to the deleted node from the edge list
        st.session_state["p1_list"] = [edge for edge in st.session_state["p1_list"]
                                         if edge["source"] != node_to_delete and edge["target"] != node_to_delete]

        st.session_state["p2_list"] = [edge for edge in st.session_state["p2_list"]
                                       if edge["source"] != node_to_delete and edge["target"] != node_to_delete]
        st.session_state["deleted_node"] = node_to_delete  # Store the deleted node name

        st.success(f"Node '{node_to_delete}' has been deleted.")
        time.sleep(1)
        st.experimental_rerun()

def create_relation():
    with st.expander("Product 1"):
        product_name = ["Product 2"]
        def save_product1(node1, relation, node2):
            product1_dict = {
                "source": node1,
                "target": node2,
                "type": relation,
                "id": str(uuid.uuid4()),
            }
            st.session_state["p1_list"].append(product1_dict)
        # UI rendering
        node1_col, type1_col, relation_col, node2_col, type2_col = st.columns(5)
        # Logic
        node_list = st.session_state["node_list"]
        node_name_list = []
        node_type_list = []
        for node in node_list:
            if node["type"] not in product_name:
                node_name_list.append(node["name"])
        def callback1():
            for node in node_list:
                if node["name"] == st.session_state["node1_select"]:
                    st.session_state["selected_value"] = node["type"]

        def callback2():
            for node in node_list:
                if node["name"] == st.session_state["node2_select"]:
                    st.session_state["selected_value"] = node["type"]

        with node1_col:
            node1_select = st.selectbox(
                "select the first node",
                options=node_name_list,
                key = "node1_select",
                on_change = callback1
            )
        with type1_col:
            callback1()
            st.write("Type")
            st.info(st.session_state["selected_value"])
        with relation_col:
            # Logic
            relation_list = metamodel_dict["edges"]
            # UI rendering
            relation_name = st.selectbox(
                "Specify the relation",
                options=relation_list
            )
        with node2_col:
            node2_select = st.selectbox(
                "select the second node",
                options=node_name_list,
                key= "node2_select", # can be added
                on_change = callback2
            )
        with type2_col:
            callback2()
            st.write("Type")
            st.info(st.session_state["selected_value"])

        store_edge_button1 = st.button("store relation",
                                       key="store_edge_button1",
                                       use_container_width=True,
                                       type="primary")
        if store_edge_button1:
            save_product1(node1_select, relation_name, node2_select)
        product1_visual()
        #visualization_graph()
        st.write(f"{node1_select} is {relation_name}  {node2_select}")

        st.json(st.session_state["p1_list"],expanded=False)

    with st.expander("Product 2"):
        product_name = ["Product 1"]
        def save_product2(node1, relation, node2):
            product2_dict = {
                "source": node1,
                "target": node2,
                "type": relation,
                "id": str(uuid.uuid4()),
            }
            st.session_state["p2_list"].append(product2_dict)
        # UI rendering
        node1_col, type3_col, relation_col, node2_col, type4_col  = st.columns(5)
        # Logic
        node_list = st.session_state["node_list"]
        node_name_list = []

        for node in node_list:
            if node["type"] not in product_name:
                node_name_list.append(node["name"])

        def callback3():
            for node in node_list:
                if node["name"] == st.session_state["node11_select"]:
                    st.session_state["selected_value11"] = node["type"]
        def callback4():
            for node in node_list:
                if node["name"] == st.session_state["node22_select"]:
                    st.session_state["selected_value22"] = node["type"]

        with node1_col:
            node11_select = st.selectbox(
                "select the first node",
                options=node_name_list,
                key = "node11_select",
                on_change = callback2
            )

        with type3_col:
            callback3()
            st.write("Type")
            st.info(st.session_state["selected_value11"])
        with relation_col:
            # Logic
            relation_list = metamodel_dict["edges"]
            # UI rendering
            relation2_name = st.selectbox(
                "Specify the relation",
                options=relation_list,
                key = "relation2_name"
            )
        with node2_col:
            node22_select = st.selectbox(
                "select the second node",
                options=node_name_list,
                key= "node22_select"  # can be added
            )
        with type4_col:
            callback4()
            st.write("Type")
            st.info(st.session_state["selected_value22"])

        store_edge_button2 = st.button("store relation",
                                       key="store_edge_button2",
                                       use_container_width=True,
                                       type="primary")
        if store_edge_button2:
            save_product2(node11_select, relation2_name, node22_select)
        #visualization_graph()
        product2_visual()
        st.write(f"{node1_select} is {relation2_name}  {node2_select}")

        st.json(st.session_state["p2_list"], expanded=False)

def store_graph():
    with st.expander("show individual lists"):
        st.json(st.session_state["node_list"], expanded=False)
        st.json(st.session_state["p1_list"], expanded=False)
        st.json(st.session_state["p2_list"], expanded=False)

    graph_dict = {
        "nodes": st.session_state["node_list"],
        "product 1": st.session_state["p1_list"],
        "product 2": st.session_state["p2_list"],
    }
    st.session_state["graph_dict"] = graph_dict
    with st.expander("Show graph JSON"):
        st.json(st.session_state["graph_dict"])

def delete_relation():
    import time
    p1_list = st.session_state["p1_list"]
    # UI rendering for Product 1 relations
    with st.expander("Product 1 Relations"):
        relation_names_p1 = [(edge["source"], edge["type"], edge["target"]) for edge in p1_list]
        relation_to_delete_p1 = st.selectbox("Select a relation to delete", options=relation_names_p1,
                                             key="relation_to_delete_p1"
                                             )
        delete_relation_button_p1 = st.button("Delete Relation", key="delete_relation_button_p1",
                                              use_container_width=True, type="primary")

        if delete_relation_button_p1:
            st.session_state["p1_list"] = [edge for edge in p1_list if
                                           (edge["source"], edge["type"], edge["target"]) != relation_to_delete_p1]

            st.success(f"Relation '{relation_to_delete_p1[0]} is {relation_to_delete_p1[1]} {relation_to_delete_p1[2]}' "
                       f"in Product 1 has been deleted.")
            time.sleep(1)
            st.experimental_rerun()

    # UI rendering for Product 2 relations
    p2_list = st.session_state["p2_list"]
    with st.expander("Product 2 Relations"):
        relation_names_p2 = [(edge["source"], edge["type"], edge["target"]) for edge in p2_list]
        relation_to_delete_p2 = st.selectbox("Select a relation to delete", options=relation_names_p2,
                                             key="relation_to_delete_p2")
        delete_relation_button_p2 = st.button("Delete Relation", key="delete_relation_button_p2",
                                              use_container_width=True, type="primary")

        if delete_relation_button_p2:
            st.session_state["p2_list"] = [edge for edge in p2_list if
                                           (edge["source"], edge["type"], edge["target"]) != relation_to_delete_p2]

            st.success(f"Relation '{relation_to_delete_p2[0]} is {relation_to_delete_p2[1]} {relation_to_delete_p2[2]}' "
                       f"in Product 2 has been deleted.")
            time.sleep(1)
            st.experimental_rerun()

def visualization_graph():

    def set_color(node_type):
        color = "Red"
        if node_type == "Product 1":
            color = "Blue"
        elif node_type == "Process":
            color = "Yellow"
        elif node_type == "Resource":
            color = "Green"
        return color

    with st.expander("Visualise the Graph of Product 1"):
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Visualization of PPR for Product 1",
                "Basic Engineering View",
                "Electrical View",
                "Sustainable View"
            ]
        )

        with tab1:
            # Visualization of PPR for Product 1
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

        with tab2:
            # Basic Engineering View of Product 1
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
                graph.node(node_name, node_name,
                           xlabel=str(node["submodels"]["Engineering"]),
                           color=set_color(node["type"]))
            for edge in edge_list:
                source = edge["source"]
                target = edge["target"]
                relation = edge["type"]
                graph.edge(source, target, relation)
            st.graphviz_chart(graph)

        with tab3:
            # Electrical View of Product 1
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
                graph.node(node_name, node_name,
                           xlabel=str(node["submodels"]["Electrical"]),
                           color=set_color(node["type"]))
            for edge in edge_list:
                source = edge["source"]
                target = edge["target"]
                relation = edge["type"]
                graph.edge(source, target, relation)
            st.graphviz_chart(graph)

        with tab4:
            # Sustainable View of Product 1
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
                graph.node(node_name, node_name,
                           xlabel=str(node["submodels"]["Sustainable"]),
                           color=set_color(node["type"]))
            for edge in edge_list:
                source = edge["source"]
                target = edge["target"]
                relation = edge["type"]
                graph.edge(source, target, relation)
            st.graphviz_chart(graph)

    with st.expander("Visualise the Graph of Product 2"):
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Visualization of PPR for Product 2",
                "Basic Engineering View",
                "Electrical View",
                "Sustainable View"
            ]
        )

        with tab1:
            # Visualization of PPR for Product 2
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

        with tab2:
            # Basic Engineering View of Product 2
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
                graph.node(node_name, node_name,
                           xlabel=str(node["submodels"]["Engineering"]),
                           color=set_color(node["type"]))
            for edge in edge_list:
                source = edge["source"]
                target = edge["target"]
                relation = edge["type"]
                graph.edge(source, target, relation)
            st.graphviz_chart(graph)

        with tab3:
            # Electrical View of Product 2
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
                graph.node(node_name, node_name,
                           xlabel=str(node["submodels"]["Electrical"]),
                           color=set_color(node["type"]))
            for edge in edge_list:
                source = edge["source"]
                target = edge["target"]
                relation = edge["type"]
                graph.edge(source, target, relation)
            st.graphviz_chart(graph)

        with tab4:
            # Sustainable View of Product 2
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
                graph.node(node_name, node_name,
                           xlabel=str(node["submodels"]["Sustainable"]),
                           color=set_color(node["type"]))
            for edge in edge_list:
                source = edge["source"]
                target = edge["target"]
                relation = edge["type"]
                graph.edge(source, target, relation)
            st.graphviz_chart(graph)

def basic_analyze_graph():
    G = nx.DiGraph()

    # Retrieve node and edge information from session state
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "product 1": st.session_state["p1_list"],
        "product 2": st.session_state["p2_list"],
    }
    st.session_state["graph_dict"] = graph_dict

    node_list = graph_dict["nodes"]
    p1_list = graph_dict["product 1"]
    p2_list = graph_dict["product 2"]
    node_tuple_list = []
    edge_tuple_list = []

    # Analyze Product 1 Graph
    with st.expander("Product 1 Graph Analysis"):
        # Construct nodes and edges for Product 1
        for node in node_list:
            node_tuple = (node["name"], node)
            node_tuple_list.append(node_tuple)

        for edge in p1_list:
            edge_tuple = (edge["source"], edge["target"], edge)
            edge_tuple_list.append(edge_tuple)

        # Add nodes and edges to the graph
        G.add_nodes_from(node_tuple_list)
        G.add_edges_from(edge_tuple_list)

        # Provide analysis options for Product 1
        select_functions1 = st.selectbox(label="Select Function",
                                         options=["Output Nodes and Edges",
                                                  "Count Nodes",
                                                  "Count Edges",
                                                  "Specific Node",
                                                  "Specific Edge",
                                                  "Density",
                                                  "Shortest Path",
                                                  "Check Path",
                                                  "Check if graph is empty",
                                                  "Is the graph directed"
                                                  ],
                                         key="select_functions1")
        # Perform selected analysis function
        if select_functions1 == "Output Nodes and Edges":
            output_nodes_and_edges(graph=G)
        elif select_functions1 == "Count Nodes":
            count_nodes(G)
        elif select_functions1 == "Count Edges":
            count_edges(G)
        elif select_functions1 == "Specific Node":
            specific_node(G)
        elif select_functions1 == "Specific Edge":
            specific_edge(G)
        elif select_functions1 == "Density":
            density_graph(G)
        elif select_functions1 == "Shortest Path":
            shortest_path(G)
        elif select_functions1 == "Check Path":
            check_path(G)
        elif select_functions1 == "Check if graph is empty":
            is_empty(G)
        elif select_functions1 == "Is the graph directed":
            is_directed(G)

    # Analyze Product 2 Graph
    with st.expander("Product 2 Graph Analysis"):
        # Construct nodes and edges for Product 2
        for node in node_list:
            node_tuple = (node["name"], node)
            node_tuple_list.append(node_tuple)

        for edge in p2_list:
            edge_tuple = (edge["source"], edge["target"], edge)
            edge_tuple_list.append(edge_tuple)

        # Add nodes and edges to the graph
        G.add_nodes_from(node_tuple_list)
        G.add_edges_from(edge_tuple_list)

        # Provide analysis options for Product 2
        select_functions = st.selectbox(label="Select Function",
                                        options=["Output Nodes and Edges",
                                                 "Count Nodes",
                                                 "Count Edges",
                                                 "Specific Node",
                                                 "Specific Edge",
                                                 "Density",
                                                 "Shortest Path",
                                                 "Check Path",
                                                 "Check if graph is empty",
                                                 "Is the graph directed"
                                                 ],
                                        key="select_functions")
        # Perform selected analysis function
        if select_functions == "Output Nodes and Edges":
            output_nodes_and_edges(graph=G)
        elif select_functions == "Count Nodes":
            count_nodes(G)
        elif select_functions == "Count Edges":
            count_edges(G)
        elif select_functions == "Specific Node":
            specific_node(G)
        elif select_functions == "Specific Edge":
            specific_edge(G)
        elif select_functions == "Density":
            density_graph(G)
        elif select_functions == "Shortest Path":
            shortest_path(G)
        elif select_functions == "Check Path":
            check_path(G)
        elif select_functions == "Check if graph is empty":
            is_empty(G)
        elif select_functions == "Is the graph directed":
            is_directed(G)

def export_graph():
    # Retrieve graph data from session state
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "product 1": st.session_state["p1_list"],
        "product 2": st.session_state["p2_list"],
    }
    st.session_state["graph_dict"] = graph_dict

    # Convert graph data to JSON format
    graph_string = json.dumps(st.session_state["graph_dict"])

    # Convert graph data to PPR dictionary format
    ppr_dict = graph_dict_to_ppr_dict()
    ppr_json = json.dumps(ppr_dict)

    # Download button for exporting graph data to JSON
    st.download_button(
        "Export Graph to JSON",
        file_name="graph.json",
        mime="application/json",
        data=graph_string,
        use_container_width=True,
        type="primary"
    )

    # Download button for exporting graph dictionary to PPR dictionary JSON
    st.download_button(
        "Export Graph Dict to PPR Dict",
        file_name="graph_PPR.json",
        mime="application/json",
        data=ppr_json,
        use_container_width=True,
        type="primary"
    )
def graph_dict_to_ppr_dict():
    # Initialize lists to store PPR nodes and edges
    ppr_nodes = []
    ppr_edges1 = []
    ppr_edges2 = []

    # Retrieve graph data from session state
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "product 1": st.session_state["p1_list"],
        "product 2": st.session_state["p2_list"],
    }
    st.session_state["graph_dict"] = graph_dict

    # Extract node information and construct PPR nodes
    for node in graph_dict.get("nodes", []):
        ppr_node = {
            "id": node.get("id", None),
            "type": node.get("type", None),
            "data": {
                "label": node.get("name", None),
                "props": {
                    "views": node.get("submodels", None),
                },
                "style": node.get("ui_data", {}).get("style", None),
            },
            "position": node.get("ui_data", {}).get("position", None),
            "width": node.get("ui_data", {}).get("width", None),
            "height": node.get("ui_data", {}).get("height", None),
        }
        ppr_nodes.append(ppr_node)

    # Extract edge information for product 1 and construct PPR edges
    for edge in graph_dict.get("product 1", []):
        ppr_edge1 = {
            "id": edge.get("id", None),
            "label": edge.get("name", None),
            "source": edge.get("source", None),
            "target": edge.get("target", None),
            "sourceHandle": edge.get("ui_data", {}).get("sourceHandle", None),
            "targetHandle": edge.get("ui_data", {}).get("targetHandle", None),
        }
        ppr_edges1.append(ppr_edge1)

    # Extract edge information for product 2 and construct PPR edges
    for edge in graph_dict.get("product 2", []):
        ppr_edge2 = {
            "id": edge.get("id", None),
            "label": edge.get("name", None),
            "source": edge.get("source", None),
            "target": edge.get("target", None),
            "sourceHandle": edge.get("ui_data", {}).get("sourceHandle", None),
            "targetHandle": edge.get("ui_data", {}).get("targetHandle", None),
        }
        ppr_edges1.append(ppr_edge2)

    # Construct PPR dictionary containing nodes and edges information
    ppr_dict = {
        "nodes": ppr_nodes,
        "edges": ppr_edges1 #+ ppr_edges2
    }

    return ppr_dict

def adv_analyze_graph():
    # Initialize a directed graph
    G = nx.DiGraph()

    # Retrieve graph data from session state
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "product 1": st.session_state["p1_list"],
        "product 2": st.session_state["p2_list"],
    }
    st.session_state["graph_dict"] = graph_dict

    # Extract node and edge lists
    node_list = graph_dict["nodes"]
    p1_list = graph_dict["product 1"]
    p2_list = graph_dict["product 2"]

    # Analyze Product 1 graph
    with st.expander("Product 1 Graph Analysis"):
        node_tuple_list = []
        edge_tuple_list = []

        product_name = ["Product 2"]

        # Extract nodes not related to Product 2
        for node in node_list:
            if node["type"] not in product_name:
                node_tuple = (node["name"], node)
                node_tuple_list.append(node_tuple)

        # Add edges for Product 1
        for edge in p1_list:
            edge_tuple = (edge["source"], edge["target"], edge)
            edge_tuple_list.append(edge_tuple)

        # Add nodes and edges to the graph
        G.add_nodes_from(node_tuple_list)
        G.add_edges_from(edge_tuple_list)

        # Select analysis function for Product 1
        select_functions1 = st.selectbox(label="Select Function",
                                         options=["Impact of Input Product on Process Step",
                                                  "Impact of Process Step on another Process",
                                                  "Impact of Resource on Product",
                                                  "Recurring Components"
                                                  ],
                                         key="select_functions1")
        if select_functions1 == "Impact of Resource on Product":
            resource_utilization1(graph=G)
        elif select_functions1 == "Recurring Components":
            recurring1(G)
        elif select_functions1 == "Impact of Process Step on another Process":
            process_on_process1(G)
        elif select_functions1 == "Impact of Input Product on Process Step":
            input_product_on_process1(G)

        # Clear the graph for the next analysis
        G.clear()

    # Analyze Product 2 graph
    with st.expander("Product 2 Graph Analysis"):
        node_tuple_list = []
        edge_tuple_list = []

        product_name = ["Product 1"]

        # Extract nodes not related to Product 1
        for node in node_list:
            if node["type"] not in product_name:
                node_tuple = (node["name"], node)
                node_tuple_list.append(node_tuple)

        # Add edges for Product 2
        for edge in p2_list:
            edge_tuple = (edge["source"], edge["target"], edge)
            edge_tuple_list.append(edge_tuple)

        # Add nodes and edges to the graph
        G.add_nodes_from(node_tuple_list)
        G.add_edges_from(edge_tuple_list)

        # Select analysis function for Product 2
        select_functions2 = st.selectbox(label="Select Function",
                                         options=["Impact of Input Product on Process Step",
                                                  "Impact of Process Step on another Process",
                                                  "Impact of Resource on Product",
                                                  "Recurring Components"
                                                  ],
                                         key="select_functions2")
        if select_functions2 == "Impact of Resource on Product":
            resource_utilization2(graph=G)
        elif select_functions2 == "Recurring Components":
            recurring2(G)
        elif select_functions2 == "Impact of Process Step on another Process":
            process_on_process2(G)
        elif select_functions2 == "Impact of Input Product on Process Step":
            input_product_on_process2(G)
